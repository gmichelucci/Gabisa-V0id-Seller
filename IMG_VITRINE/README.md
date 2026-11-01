# 📸 Acervo de Imagens de Vitrine (Marketplace)

Este diretório foi estruturado para receber as imagens finais tratadas e comerciais que serão enviadas para as vitrines dos anúncios (Mercado Livre, Shopee, etc.).

---

## 🗂️ Estrutura de Pastas

Organize suas fotos colocando cada arquivo dentro da pasta correspondente à linha do produto:

* 📁 `IMG_VITRINE/CLASSECOR/`
* 📁 `IMG_VITRINE/NEW AUTOMOTIVO 1.0/`
* 📁 `IMG_VITRINE/DUNE 0.9/`
* 📁 `IMG_VITRINE/BERGAMO 1.0/`
* 📁 `IMG_VITRINE/HONDA/`
* 📁 `IMG_VITRINE/CEDROMOV/`
* 📁 `IMG_VITRINE/FAVO CAR/`
* 📁 `IMG_VITRINE/HBROS/`

---

## 🏷️ Padrão Obrigatório de Nomenclatura

Nomeie cada imagem seguindo exatamente o formato:
```
Produto-Cor-Ordem.extensao
```

### Exemplos práticos:
* `CLASSECOR-Branco-1.jpg` *(Foto 1: Capa / Principal)*
* `CLASSECOR-Branco-2.jpg` *(Foto 2: Detalhe da Textura)*
* `CLASSECOR-Branco-3.jpg` *(Foto 3: Aplicação em Móvel/Sofá)*
* `CLASSECOR-Branco-4.jpg` *(Foto 4: Ficha Técnica / Rolo)*
* `DUNE 0.9-Sepia-1.jpg`
* `DUNE 0.9-Sepia-2.jpg`
* `NEW AUTOMOTIVO 1.0-Preto-1.jpg`

---

## ⭐ Guia de Ordem Recomendada (Mercado Livre)

1. **Foto 1 (Ordem 1 — Capa Principal):**
   * **Fundo 100% Branco Puro** (obrigatório pelo Mercado Livre para não perder relevância).
   * Sem bordas, sem logos, sem textos sobre a imagem.
   * Amostra ou rolo centralizado ocupando ~80% do quadro.
2. **Foto 2 (Ordem 2 — Macro / Textura):**
   * Foto em ângulo mostrando a gravação do sintético, brilho e espessura do material.
3. **Foto 3 (Ordem 3 — Aplicação Real / Ambientação):**
   * Foto de sofá, poltrona, banco de carro ou barco utilizando o material aplicado.
4. **Foto 4 (Ordem 4 — Ficha Técnica / Dimensões):**
   * Imagem ilustrando as medidas (Largura padrão 1,40m, cortes de 1m a 5m ou rolo fechado).

---

## 🚀 Sincronização Automática com Supabase

Assim que você colocar suas fotos aqui, executaremos o script:
```bash
python scripts/sync_vitrine_supabase.py
```
Esse script subirá as fotos automaticamente para o bucket `vitrine` no Supabase Storage e associará as URLs públicas diretamente aos anúncios gerados.
