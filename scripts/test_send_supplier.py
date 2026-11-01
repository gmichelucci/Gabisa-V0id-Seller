import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from core.whatsapp import whatsapp
from core.config import settings

async def main():
    target_number = sys.argv[1] if len(sys.argv) > 1 else settings.SUPPLIER_NUMBER
    print(f"Enviando mensagem de teste para: {target_number}")

    # Mensagem de teste de alinhamento
    msg_test = (
        "*[VIDITEX DISTRIBUIDORA]*\n"
        "Mensagem de teste do sistema de automação e integração de pedidos e cotações. "
        "Serviço operando normalmente."
    )
    res = await whatsapp.send_message(target_number, msg_test)
    print("Resultado do envio:", res)

if __name__ == "__main__":
    asyncio.run(main())
