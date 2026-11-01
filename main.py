from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from models.schemas import WebhookQuestion, WebhookWhatsapp, OrderWebhook, PostSaleWebhook
from services.ad_generator_service import ad_generator_service
from services.freight_quote_agent import freight_quote_agent
from services.order_dispatcher import order_dispatcher
from services.post_sales_b2b import post_sales_b2b

app = FastAPI(title="Viditex Distribuidora - Backend B2B")

router = APIRouter()

@router.post("/ads/generate/{product_id}")
async def generate_ads(product_id: str):
    try:
        ads = await ad_generator_service.generate_ads_for_product(product_id)
        return {"status": "success", "generated_ads": ads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhooks/marketplace/question")
async def marketplace_question_webhook(question: WebhookQuestion):
    try:
        result = await freight_quote_agent.handle_marketplace_question(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhooks/whatsapp/supplier")
async def whatsapp_supplier_webhook(message: WebhookWhatsapp):
    try:
        result = await freight_quote_agent.handle_supplier_reply(message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhooks/whatsapp/customer")
async def whatsapp_customer_webhook(message: WebhookWhatsapp):
    try:
        result = await post_sales_b2b.handle_customer_reply(message.number, message.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhooks/marketplace/order")
async def marketplace_order_webhook(order: OrderWebhook):
    try:
        result = await order_dispatcher.dispatch_order(order)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhooks/marketplace/post-sale")
async def marketplace_post_sale_webhook(event: PostSaleWebhook, background_tasks: BackgroundTasks):
    try:
        # Assuming this is called 24h after delivery
        background_tasks.add_task(post_sales_b2b.process_post_sale, event)
        return {"status": "processing_post_sale_background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
