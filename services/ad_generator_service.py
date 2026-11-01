import json
from typing import Dict, Any, List
from core.database import supabase
from core.ai import ai_client

class AdGeneratorService:
    def __init__(self):
        self.max_metros_dobrado = 5 # default 5m

    async def generate_ads_for_product(self, product_id: str):
        # 1. Fetch product from sinteticos_produtos_base
        response = supabase.table("sinteticos_produtos_base").select("*").eq("id", product_id).execute()

        if not response.data:
            raise ValueError(f"Product with id {product_id} not found")

        product = response.data[0]
        nome = product.get('nome_tecnico', product.get('nome', ''))
        cor = product.get('cor', '')
        sku = product.get('sku_fornecedor', '')
        metros_rolo = int(product.get('metros_por_rolo', 30))
        custo_metro = float(product.get('custo_metro_fornecedor', 10.0))
        custo_rolo = float(product.get('custo_rolo_fechado', custo_metro * metros_rolo))

        # 2. Use Gemini to generate segmented ads
        prompt = f"""
        Você é o especialista em marketing e vendas de marketplace da Viditex Distribuidora.
        Preciso que você crie anúncios de alta conversão para o seguinte produto (laminado sintético / courvin):

        Produto: {nome}
        SKU / Código: {sku}
        Cor: {cor}
        Metros no Rolo Fechado: {metros_rolo}m
        Marca da Loja: Viditex Distribuidora

        Crie anúncios segmentados para os seguintes nichos: Automotivo, Moveleiro, e Náutico.

        Para cada nicho, crie as variações:
        1. Cortes e Kits (envio dobrado): 1m, 2m, 3m e 5m lineares x 1,40m.
        2. Rolo Fechado: {metros_rolo}m.

        Retorne os resultados EXATAMENTE no seguinte formato JSON (sem markdown, apenas o JSON puro):
        {{
            "ads": [
                {{
                    "nicho": "Automotivo",
                    "titulo": "Courvin Automotivo {nome} {cor} 1m x 1,40m Envio Dobrado",
                    "tipo": "corte",
                    "metragem": 1,
                    "modalidade": "etiqueta_marketplace"
                }},
                {{
                    "nicho": "Moveleiro",
                    "titulo": "Rolo Courvin {nome} {cor} {metros_rolo}m Atacado Fábrica",
                    "tipo": "rolo",
                    "metragem": {metros_rolo},
                    "modalidade": "frete_fornecedor"
                }}
            ]
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
            text_resp = text_resp.strip()

            generated_ads_data = json.loads(text_resp)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            raise

        # 3. Save the generated ads to sinteticos_anuncios matching real columns and required fields
        created_ads = []
        for ad in generated_ads_data.get("ads", []):
            tipo = ad.get("tipo", "corte")
            metragem = float(ad.get("metragem", 1))

            if tipo == "rolo":
                # Margem de atacado (~35% sobre custo do rolo)
                preco_venda = round(custo_rolo * 1.35, 2)
            else:
                # Margem para cortes fracionados (markup ~2.2x para absorver taxas ML e embalagem)
                preco_venda = max(29.90, round(custo_metro * metragem * 2.2, 2))

            ad_record = {
                "produto_base_id": product_id,
                "nicho_alvo": ad.get("nicho", "Geral"),
                "titulo_anuncio": ad.get("titulo", f"{nome} {cor}"),
                "tipo_venda": tipo,
                "metragem_por_unidade": int(metragem),
                "modalidade_frete": ad.get("modalidade", "etiqueta_marketplace"),
                "preco_venda": preco_venda,
                "status": "rascunho",
                "marketplace": "Mercado Livre"
            }
            insert_response = supabase.table("sinteticos_anuncios").insert(ad_record).execute()
            created_ads.extend(insert_response.data)

        return created_ads

ad_generator_service = AdGeneratorService()
