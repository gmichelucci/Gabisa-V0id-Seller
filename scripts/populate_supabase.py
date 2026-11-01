import os
import sys
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.database import supabase

# 1. Base product specifications from supplier spreadsheet
SPECS = {
    'CLASSECOR': {
        'cod': '1008',
        'espessura_mm': 0.5,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 50,
        'custo_metro_fornecedor': 8.80,
        'custo_rolo_fechado': 440.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5
    },
    'DUNE': {
        'cod': '1030',
        'espessura_mm': 0.9,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 30,
        'custo_metro_fornecedor': 16.50,
        'custo_rolo_fechado': 495.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5
    },
    'NEW AUTOMOTIVO 1.0': {
        'cod': '1018',
        'espessura_mm': 1.0,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 30,
        'custo_metro_fornecedor': 14.50,
        'custo_rolo_fechado': 435.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5
    }
}

OTHER_PRODUCTS = [
    {
        'sku_fornecedor': '1057-PADRAO',
        'nome_tecnico': 'BERGAMO 1.0 (Náutico / Garden)',
        'cor': 'Padrão / Sob Consulta',
        'espessura_mm': 1.0,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 30,
        'custo_metro_fornecedor': 18.50,
        'custo_rolo_fechado': 555.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5,
        'estoque_disponivel': True
    },
    {
        'sku_fornecedor': '1003-PADRAO',
        'nome_tecnico': 'HONDA (Banco de Moto)',
        'cor': 'Preto / Padrão',
        'espessura_mm': 0.67,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 40,
        'custo_metro_fornecedor': 13.50,
        'custo_rolo_fechado': 540.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5,
        'estoque_disponivel': True
    },
    {
        'sku_fornecedor': '1010-PADRAO',
        'nome_tecnico': 'CEDROMOV (Banco Liso)',
        'cor': 'Preto / Padrão',
        'espessura_mm': 0.67,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 40,
        'custo_metro_fornecedor': 13.50,
        'custo_rolo_fechado': 540.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5,
        'estoque_disponivel': True
    },
    {
        'sku_fornecedor': '1035-PADRAO',
        'nome_tecnico': 'FAVO CAR (Antiderrapante)',
        'cor': 'Preto / Padrão',
        'espessura_mm': 0.67,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 40,
        'custo_metro_fornecedor': 14.50,
        'custo_rolo_fechado': 580.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5,
        'estoque_disponivel': True
    },
    {
        'sku_fornecedor': '1040-PADRAO',
        'nome_tecnico': 'HBROS (Honda Bros)',
        'cor': 'Preto / Padrão',
        'espessura_mm': 0.67,
        'largura_padrao_m': 1.40,
        'metros_por_rolo': 40,
        'custo_metro_fornecedor': 14.50,
        'custo_rolo_fechado': 580.00,
        'permite_envio_dobrado': True,
        'max_metros_dobrado': 5,
        'estoque_disponivel': True
    }
]

def upload_images():
    print("Uploading sample images to Supabase Storage 'amostras' bucket...")
    img_dir = r"c:\Gabisa-V0id-Seller\IMG"
    jpg_files = glob.glob(os.path.join(img_dir, "**", "*.jpg"), recursive=True)
    
    for file_path in jpg_files:
        rel_path = os.path.relpath(file_path, img_dir).replace("\\", "/")
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            supabase.storage.from_("amostras").upload(
                path=rel_path,
                file=content,
                file_options={"content-type": "image/jpeg", "upsert": "true"}
            )
            print(f"Uploaded: {rel_path}")
        except Exception as e:
            print(f"Error uploading {rel_path}: {e}")

def populate_products():
    print("Populating sinteticos_produtos_base in Supabase...")
    # Clean existing rows if any
    supabase.table("sinteticos_produtos_base").delete().neq("sku_fornecedor", "DUMMY_NEQ").execute()

    img_dir = r"c:\Gabisa-V0id-Seller\IMG"
    rows_to_insert = []

    for produto_nome, spec in SPECS.items():
        folder = os.path.join(img_dir, produto_nome)
        if not os.path.exists(folder):
            continue
        
        dng_files = sorted(glob.glob(os.path.join(folder, "*.DNG")))
        for f in dng_files:
            basename = os.path.splitext(os.path.basename(f))[0]
            # Structure: "{Produto} - {Cor} - {Codigo}"
            parts = [p.strip() for p in basename.split(" - ")]
            cor = parts[1] if len(parts) > 1 else "Padrão"
            cod_cor = parts[2] if len(parts) > 2 else ""
            clean_sku = f"{spec['cod']}-{cod_cor}".replace(" ", "")

            row = {
                'sku_fornecedor': clean_sku,
                'nome_tecnico': produto_nome,
                'cor': cor,
                'espessura_mm': spec['espessura_mm'],
                'largura_padrao_m': spec['largura_padrao_m'],
                'metros_por_rolo': spec['metros_por_rolo'],
                'custo_metro_fornecedor': spec['custo_metro_fornecedor'],
                'custo_rolo_fechado': spec['custo_rolo_fechado'],
                'permite_envio_dobrado': spec['permite_envio_dobrado'],
                'max_metros_dobrado': spec['max_metros_dobrado'],
                'estoque_disponivel': True
            }
            rows_to_insert.append(row)

    # Add other products from father's catalog
    rows_to_insert.extend(OTHER_PRODUCTS)

    # Insert in batches of 20
    batch_size = 20
    for i in range(0, len(rows_to_insert), batch_size):
        batch = rows_to_insert[i:i+batch_size]
        res = supabase.table("sinteticos_produtos_base").insert(batch).execute()
        print(f"Inserted batch {i//batch_size + 1}: {len(res.data)} items")

    print(f"Total inserted: {len(rows_to_insert)} products into sinteticos_produtos_base!")

if __name__ == "__main__":
    upload_images()
    populate_products()
