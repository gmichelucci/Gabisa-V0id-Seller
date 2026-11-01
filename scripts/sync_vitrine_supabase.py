import os
import sys
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.database import supabase

def sync_vitrine():
    vitrine_dir = r"c:\Gabisa-V0id-Seller\IMG_VITRINE"
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(vitrine_dir, "**", ext), recursive=True))

    if not files:
        print("Nenhuma imagem encontrada em IMG_VITRINE ainda.")
        return

    print(f"Encontradas {len(files)} imagens de vitrine. Iniciando upload para bucket 'vitrine'...")
    uploaded = 0
    for f in sorted(files):
        rel_path = os.path.relpath(f, vitrine_dir).replace("\\", "/")
        filename = os.path.basename(f)
        try:
            with open(f, "rb") as img_file:
                content = img_file.read()

            content_type = "image/jpeg"
            if f.lower().endswith(".png"):
                content_type = "image/png"
            elif f.lower().endswith(".webp"):
                content_type = "image/webp"

            supabase.storage.from_("vitrine").upload(
                path=rel_path,
                file=content,
                file_options={"content-type": content_type, "upsert": "true"}
            )
            public_url = supabase.storage.from_("vitrine").get_public_url(rel_path)
            print(f"✓ Upload: {rel_path} -> {public_url}")
            uploaded += 1
        except Exception as e:
            print(f"✗ Erro no upload de {rel_path}: {e}")

    print(f"\nFinalizado! {uploaded} fotos de vitrine sincronizadas com o Supabase Storage.")

if __name__ == "__main__":
    sync_vitrine()
