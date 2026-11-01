import re
import json
import datetime
from core.database import supabase
from core.whatsapp import whatsapp
from core.ai import ai_client
from models.schemas import WebhookQuestion, WebhookWhatsapp
from core.config import settings

class FreightQuoteAgent:
    def __init__(self):
        self.supplier_number = settings.SUPPLIER_NUMBER
        self.min_order_value_transportadora = 5000.0  # Regra comercial: transportadora apenas >= R$ 5.000

    def _extract_cep(self, text: str) -> str:
        match = re.search(r'\b\d{5}-?\d{3}\b', text)
        return match.group(0) if match else None

    async def _classify_intent(self, question_text: str) -> dict:
        prompt = f"""
        Você é o assistente de vendas e logística da Viditex Distribuidora (laminados sintéticos B2B).
        Analise a pergunta de um comprador no Mercado Livre:
        "{question_text}"

        Regra de logística do fornecedor:
        1. Envio por TRANSPORTADORA terceirizada: apenas para compras de atacado ou rolos fechados com valor igual ou superior a R$ 5.000,00 (mínimo ~3 rolos ou 90+ metros).
        2. Pedidos fracionados (1m, 2m, 5m, 10m) ou pequenas quantidades (1 a 2 rolos avulsos com valor < R$ 5.000): o envio é feito SEMPRE via MERCADO ENVIOS (Correios / Coleta ML). O frete é calculado automaticamente no próprio anúncio do Mercado Livre.

        Responda APENAS um JSON no seguinte formato (sem formatação markdown adicional):
        {{
            "cep": "01310-000",
            "quantidade_rolos": 1,
            "valor_estimado": 350.0,
            "elegivel_transportadora": false,
            "motivo": "Pedido abaixo de R$ 5.000, elegível para Mercado Envios",
            "resposta_automatica_ml": "Olá! Para pedidos fracionados ou rolos avulsos (abaixo de R$ 5.000), o frete e o prazo são calculados automaticamente pelo Mercado Envios diretamente ao lado do botão Comprar. O envio via transportadora rodoviária dedicada é exclusivo para cargas de atacado a partir de R$ 5.000,00. Ficamos à disposição!"
        }}
        """
        try:
            res = ai_client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=prompt
            )
            raw = res.text.strip()
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.startswith("```"):
                raw = raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            return json.loads(raw.strip())
        except Exception as e:
            print(f"Erro ao classificar pergunta com IA: {e}")
            # Fallback seguro
            cep = self._extract_cep(question_text)
            return {
                "cep": cep,
                "quantidade_rolos": 1,
                "valor_estimado": 0.0,
                "elegivel_transportadora": False,
                "motivo": "Fallback sem IA",
                "resposta_automatica_ml": "Olá! Você pode calcular o frete e prazo diretamente pelo simulador do anúncio via Mercado Envios. Envio por transportadora é exclusivo para pedidos de atacado acima de R$ 5.000,00."
            }

    async def handle_marketplace_question(self, question: WebhookQuestion):
        intent = await self._classify_intent(question.text)
        cep = intent.get("cep") or self._extract_cep(question.text)

        if not cep:
            return {"status": "no_cep_found", "message": "Pergunta não continha CEP para cotação."}

        cep_clean = cep.replace("-", "")

        # Se NÃO for elegível para transportadora (< R$ 5.000)
        if not intent.get("elegivel_transportadora", False):
            auto_reply = intent.get("resposta_automatica_ml")
            print(f"[Logística] Pedido < R$ 5.000. Respondendo cliente no ML sem incomodar fornecedor: {auto_reply}")

            # Registra no histórico como respondido automaticamente
            supabase.table("sinteticos_cotacoes_frete").insert({
                "cep_destino": cep_clean,
                "marketplace_question_id": question.question_id,
                "pergunta_original": question.text,
                "status_cotacao": "auto_replied_mercado_envios"
            }).execute()

            return {
                "status": "auto_replied_mercado_envios",
                "reason": intent.get("motivo"),
                "reply_to_marketplace": auto_reply
            }

        # Se for elegível (>= R$ 5.000): verifica cache recente no Supabase
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        recent_quote = supabase.table("sinteticos_cotacoes_frete") \
            .select("*") \
            .eq("cep_destino", cep_clean) \
            .gte("created_at", today) \
            .execute()

        if recent_quote.data:
            quote = recent_quote.data[0]
            val = quote.get('valor_frete_cotado')
            prazo = quote.get('prazo_dias_uteis')
            if val and prazo:
                print(f"[Logística] Respondendo cotação de atacado usando cache: R$ {val} ({prazo} dias)")
                return {"status": "replied_from_cache", "quote": quote}

        # Consulta fornecedor via WhatsApp para o atacado
        qtd_rolos = intent.get("quantidade_rolos") or 3
        msg = (
            f"Olá! Cotação de frete para pedido de atacado B2B (valor >= R$ 5.000):\n"
            f"- Quantidade estimada: {qtd_rolos} rolo(s) fechado(s)\n"
            f"- Destino: CEP {cep}\n"
            f"Poderia informar o valor do frete e o prazo da transportadora?"
        )

        supabase.table("sinteticos_cotacoes_frete").insert({
            "cep_destino": cep_clean,
            "marketplace_question_id": question.question_id,
            "pergunta_original": question.text,
            "status_cotacao": "pending"
        }).execute()

        await whatsapp.send_message(self.supplier_number, msg)
        print(f"[Logística] Cotação de atacado enviada ao fornecedor ({self.supplier_number})")
        return {"status": "quote_requested_supplier", "supplier_message": msg}

    async def handle_supplier_reply(self, message: WebhookWhatsapp):
        prompt = f"""
        Extraia o valor do frete e o prazo de entrega da seguinte mensagem do fornecedor:
        Mensagem: "{message.text}"

        Responda APENAS um JSON no seguinte formato (sem markdown):
        {{
            "valor": 150.50,
            "prazo": 5
        }}
        """

        genai_response = ai_client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )

        try:
            text_resp = genai_response.text.strip()
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:]
            if text_resp.startswith("```"):
                text_resp = text_resp[3:]
            if text_resp.endswith("```"):
                text_resp = text_resp[:-3]
            data = json.loads(text_resp.strip())
        except Exception as e:
            print(f"Erro ao interpretar resposta do fornecedor: {e}")
            return {"status": "error_parsing_reply"}

        valor = data.get("valor")
        prazo = data.get("prazo")

        if not valor or not prazo:
            return {"status": "incomplete_data"}

        pending_quotes = supabase.table("sinteticos_cotacoes_frete") \
            .select("*") \
            .eq("status_cotacao", "pending") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        if pending_quotes.data:
            quote = pending_quotes.data[0]

            supabase.table("sinteticos_cotacoes_frete").update({
                "valor_frete_cotado": valor,
                "prazo_dias_uteis": prazo,
                "status_cotacao": "answered"
            }).eq("id", quote["id"]).execute()

            resposta_ml = f"Olá! O frete para o CEP informado via transportadora rodoviária fica em R$ {valor:.2f} com prazo estimado de {prazo} dias úteis após a expedição."
            print(f"[Logística] Cotação atualizada no BD e enviada ao ML: {resposta_ml}")
            return {"status": "quote_answered", "marketplace_reply": resposta_ml}

        return {"status": "no_pending_quote_found"}

freight_quote_agent = FreightQuoteAgent()
