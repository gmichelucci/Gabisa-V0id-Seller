import json
from core.database import supabase
from core.whatsapp import whatsapp
from core.ai import ai_client
from models.schemas import PostSaleWebhook

class PostSalesB2B:
    async def process_post_sale(self, event: PostSaleWebhook):
        msg = f"Olá! Aqui é da Viditex Distribuidora. Vimos que o seu pedido {event.order_id} de laminado sintético foi entregue. Deu tudo certo com o material? Você trabalha com estofados, tapeçaria, marcenaria ou capotaria?"
        await whatsapp.send_message(event.customer_phone, msg)
        return {"status": "message_sent"}

    async def handle_customer_reply(self, phone: str, text: str):
        prompt = f"""
        Analise a seguinte resposta de um cliente que comprou laminado sintético.
        O objetivo é descobrir se ele é um profissional da área (B2B) como:
        tapeceiro, capoteiro, estofador, fabricante de móveis, etc.
        Ou se é apenas um consumidor final (B2C) fazendo um reparo próprio.

        Mensagem do cliente: "{text}"

        Responda APENAS um JSON no seguinte formato (sem markdown):
        {{
            "is_professional": true,
            "profession": "Tapeceiro / Estofador / etc",
            "confidence": 85
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
            print(f"Error parsing Gemini classification: {e}")
            return {"status": "error"}

        is_prof = data.get("is_professional", False)
        confidence = data.get("confidence", 0)
        profession = data.get("profession", "Tapeçaria / Estofados")

        if is_prof and confidence > 70:
            lead_data = {
                "whatsapp": phone,
                "ramo_atividade": profession,
                "eh_profissional_recorrente": True,
                "interesse_bobina_fechada": True,
                "status_abordagem": "qualificado_b2b",
                "historico_conversa": f"Cliente: {text}"
            }
            supabase.table("sinteticos_leads_b2b").upsert(lead_data, on_conflict="whatsapp").execute()

            followup_msg = f"Excelente! Como você atua com {profession}, a Viditex Distribuidora tem tabela diferenciada para profissionais e atacado direto da fábrica. Gostaria de receber nosso catálogo com preços especiais?"
            await whatsapp.send_message(phone, followup_msg)

            return {"status": "classified_b2b", "profession": profession}

        return {"status": "classified_b2c"}

post_sales_b2b = PostSalesB2B()
