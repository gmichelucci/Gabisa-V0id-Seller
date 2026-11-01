from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class WebhookQuestion(BaseModel):
    question_id: str
    product_id: str
    text: str
    customer_id: str

class WebhookWhatsapp(BaseModel):
    message_id: str
    number: str
    text: str
    is_group: bool = False

class OrderWebhook(BaseModel):
    order_id: str
    product_id: str
    customer_id: str
    customer_phone: str
    customer_name: str
    quantidade_comprada: int
    metragem_por_unidade: int
    is_rolo_fechado: bool = False
    delivery_details: Dict[str, Any] # CEP, address, etc.
    invoice_details: Optional[Dict[str, Any]] = None
    marketplace_label_url: Optional[str] = None
    status: str

class PostSaleWebhook(BaseModel):
    order_id: str
    customer_id: str
    customer_phone: str
    status: str
