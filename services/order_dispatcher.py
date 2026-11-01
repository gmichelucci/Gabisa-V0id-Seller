import httpx
from core.database import supabase
from core.whatsapp import whatsapp
from models.schemas import OrderWebhook
from core.config import settings

class OrderDispatcher:
    def __init__(self):
        self.max_metros_dobrado = 5
        self.supplier_number = settings.SUPPLIER_NUMBER

    async def _download_and_upload_label(self, url: str, order_id: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            pdf_bytes = response.content

        file_path = f"labels/{order_id}.pdf"

        supabase.storage.from_("etiquetas").upload(
            file=pdf_bytes,
            path=file_path,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )

        public_url = supabase.storage.from_("etiquetas").get_public_url(file_path)
        return public_url

    async def dispatch_order(self, order: OrderWebhook):
        total_metros = order.quantidade_comprada * order.metragem_por_unidade
        tipo_envio = "rolo_fechado" if order.is_rolo_fechado else "corte"

        label_url = None
        if not order.is_rolo_fechado and order.marketplace_label_url:
            try:
                label_url = await self._download_and_upload_label(order.marketplace_label_url, order.order_id)
            except Exception as e:
                print(f"Error saving label for order {order.order_id}: {e}")

        # Save order into sinteticos_pedidos
        pedido_record = {
            "marketplace": "Mercado Livre",
            "marketplace_order_id": order.order_id,
            "anuncio_id": order.product_id,
            "comprador_nome": order.customer_name,
            "comprador_telefone": order.customer_phone,
            "quantidade_comprada": order.quantidade_comprada,
            "metragem_total_cortar": total_metros,
            "tipo_envio": tipo_envio,
            "dados_entrega_rolo": order.delivery_details if order.is_rolo_fechado else None,
            "url_etiqueta_pdf": label_url,
            "status_pedido": order.status
        }
        supabase.table("sinteticos_pedidos").insert(pedido_record).execute()

        if order.is_rolo_fechado:
            msg = f"""
*NOVO PEDIDO - ROLO FECHADO (VIDITEX DISTRIBUIDORA)*
Pedido ID: {order.order_id}
Produto ID: {order.product_id}
Quantidade: {order.quantidade_comprada} rolo(s)
Cliente: {order.customer_name}

*Dados de Entrega:*
{order.delivery_details}

*Dados para NF:*
{order.invoice_details}

Por favor, despachar via transportadora.
            """
            await whatsapp.send_message(self.supplier_number, msg)
            return {"status": "dispatched_rolo_fechado"}

        else:
            if total_metros > self.max_metros_dobrado:
                print(f"Warning: Order {order.order_id} exceeds max_metros_dobrado ({total_metros}m > {self.max_metros_dobrado}m)")

            msg = f"""
*ORDEM DE CORTE - VIDITEX DISTRIBUIDORA*
Pedido ID: {order.order_id}
Produto ID: {order.product_id}
Metragem Total sem emenda: {total_metros} metros

Por favor, preparar o corte para envio dobrado (Etiqueta Mercado Envios em anexo).
            """
            if label_url:
                await whatsapp.send_media(self.supplier_number, msg, label_url)
            else:
                await whatsapp.send_message(self.supplier_number, msg)

            return {"status": "dispatched_corte"}

order_dispatcher = OrderDispatcher()
