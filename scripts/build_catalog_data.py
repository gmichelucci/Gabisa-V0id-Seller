import json
import csv
import os

os.makedirs('data', exist_ok=True)

produtos = [
    {
        'cod_gabisa': '1008',
        'nome': 'CLASSECOR',
        'nome_tecnico': 'Laminado Sintético em PVC Extrusado',
        'termos_mercado': ['Tecido Sintético', 'Corino', 'Corano', 'Laminado Sintético'],
        'nicho_principal': 'Moveleiro',
        'aplicacoes': 'Móveis em geral, sofás, poltronas, cadeiras, pufes, cabeceiras, brindes',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 0.500,
        'quantidade_rolo_m': 50,
        'preco_custo_metro': 8.80,
    },
    {
        'cod_gabisa': '1030',
        'nome': 'DUNE 0.9',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado 0.9mm',
        'termos_mercado': ['Tecido Sintético', 'Courvin', 'Dune', 'Facto'],
        'nicho_principal': 'Moveleiro / Bolsas',
        'aplicacoes': 'Móveis decorativos, estofados, bolsas, nécessaires, brindes de luxo',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 0.780,
        'quantidade_rolo_m': 30,
        'preco_custo_metro': 16.50,
    },
    {
        'cod_gabisa': '1018',
        'nome': 'NEW AUTOMOTIVO 1.0',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado 1.0mm',
        'termos_mercado': ['Tecido Sintético', 'Courvin Automotivo', 'Courvin Uruguaio', 'Couro Sintético Automotivo'],
        'nicho_principal': 'Automotivo',
        'aplicacoes': 'Bancos de carros, capotaria automotiva, capas de banco, laterais de portas, volantes, móveis de alta resistência',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 1.022,
        'quantidade_rolo_m': 30,
        'preco_custo_metro': 14.50,
    },
    {
        'cod_gabisa': '1057',
        'nome': 'BERGAMO 1.0',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado 1.0mm (Anti-UV, Anti-Chama, Bactericida, Fungicida)',
        'termos_mercado': ['Courvin Náutico', 'Tecido Náutico', 'Courvin Marino', 'Courvin Área Externa'],
        'nicho_principal': 'Náutico / Garden',
        'aplicacoes': 'Barcos, lanchas, iates, jet ski, móveis para área externa, varandas, piscinas, estofados hospitalares',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 1.022,
        'quantidade_rolo_m': 30,
        'preco_custo_metro': 18.50,
    },
    {
        'cod_gabisa': '1003',
        'nome': 'HONDA',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado para Moto',
        'termos_mercado': ['Courvin Honda', 'Capa Banco Moto', 'Tecido Sintético Honda'],
        'nicho_principal': 'Duas Rodas / Motos',
        'aplicacoes': 'Bancos de motos (linha Honda), capas de selim, reformas de bancos de moto',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 0.670,
        'quantidade_rolo_m': 40,
        'preco_custo_metro': 13.50,
    },
    {
        'cod_gabisa': '1010',
        'nome': 'CEDROMOV',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado Liso',
        'termos_mercado': ['Courvin Liso', 'Courvin para Moto', 'Cedromov'],
        'nicho_principal': 'Duas Rodas / Brindes',
        'aplicacoes': 'Bancos de motos acabamento liso, capas, brindes promocionais, pequenos estofados',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 0.670,
        'quantidade_rolo_m': 40,
        'preco_custo_metro': 13.50,
    },
    {
        'cod_gabisa': '1035',
        'nome': 'FAVO CAR',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado Gravação Favo/Disco',
        'termos_mercado': ['Courvin Favo', 'Courvin Disco', 'Courvin Antiderrapante Moto'],
        'nicho_principal': 'Duas Rodas / Automotivo',
        'aplicacoes': 'Bancos de motos antiderrapante / favo, detalhes de bancos automotivos, capas e brindes',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 0.670,
        'quantidade_rolo_m': 40,
        'preco_custo_metro': 14.50,
    },
    {
        'cod_gabisa': '1040',
        'nome': 'HBROS',
        'nome_tecnico': 'Laminado Sintético em PVC Espalmado Especial Honda Bros',
        'termos_mercado': ['Courvin Honda Bros', 'Capa Banco Bros', 'Courvin Linha Bros'],
        'nicho_principal': 'Duas Rodas / Motos',
        'aplicacoes': 'Bancos de motos linha Honda Bros e trail, capas esportivas, capas sob medida',
        'largura_m': 1.40,
        'peso_metro_linear_kg': 0.670,
        'quantidade_rolo_m': 40,
        'preco_custo_metro': 14.50,
    }
]

# Computed properties
for p in produtos:
    p['peso_rolo_fechado_kg'] = round(p['peso_metro_linear_kg'] * p['quantidade_rolo_m'], 2)
    p['preco_custo_rolo_fechado'] = round(p['preco_custo_metro'] * p['quantidade_rolo_m'], 2)

# 1. Save JSON
with open('data/produtos_fornecedor.json', 'w', encoding='utf-8') as f:
    json.dump(produtos, f, indent=2, ensure_ascii=False)

# 2. Save CSV
with open('data/tabela_fornecedor.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow([
        'COD_GABISA', 'PRODUTO', 'NOME_TECNICO', 'TERMOS_MERCADO_SEO', 'NICHO_PRINCIPAL',
        'APLICACOES', 'LARGURA_M', 'PESO_METRO_KG', 'METROS_ROLO',
        'PESO_ROLO_KG', 'CUSTO_METRO_RS', 'CUSTO_ROLO_RS'
    ])
    for p in produtos:
        writer.writerow([
            p['cod_gabisa'],
            p['nome'],
            p['nome_tecnico'],
            ', '.join(p['termos_mercado']),
            p['nicho_principal'],
            p['aplicacoes'],
            p['largura_m'],
            p['peso_metro_linear_kg'],
            p['quantidade_rolo_m'],
            p['peso_rolo_fechado_kg'],
            f"{p['preco_custo_metro']:.2f}",
            f"{p['preco_custo_rolo_fechado']:.2f}"
        ])

# 3. Save SQL Schema & Seed
sql_lines = [
    '-- ====================================================================',
    '-- Schema e Seed para sinteticos_produtos_base no Supabase',
    '-- Cria a tabela de produtos base com especificações de custo e frete',
    '-- ====================================================================\n',
    'CREATE TABLE IF NOT EXISTS sinteticos_produtos_base (',
    '    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),',
    '    cod_gabisa VARCHAR(50) NOT NULL,',
    '    nome VARCHAR(100) NOT NULL,',
    '    nome_tecnico VARCHAR(255),',
    '    nicho_principal VARCHAR(100),',
    '    descricao TEXT,',
    '    termos_mercado TEXT[],',
    '    largura_m NUMERIC(4,2) DEFAULT 1.40,',
    '    peso_metro_linear_kg NUMERIC(6,3) NOT NULL,',
    '    quantidade_rolo_m INTEGER NOT NULL,',
    '    peso_rolo_fechado_kg NUMERIC(6,2) NOT NULL,',
    '    preco_custo_metro NUMERIC(10,2) NOT NULL,',
    '    preco_custo_rolo_fechado NUMERIC(10,2) NOT NULL,',
    '    ativo BOOLEAN DEFAULT TRUE,',
    '    created_at TIMESTAMPTZ DEFAULT NOW(),',
    '    updated_at TIMESTAMPTZ DEFAULT NOW()',
    ');\n'
]

for p in produtos:
    termos_sql = 'ARRAY[' + ', '.join([f"'{t}'" for t in p['termos_mercado']]) + ']'
    desc = f"{p['nome_tecnico']}. Aplicações: {p['aplicacoes']}. Largura: {p['largura_m']}m."
    sql_lines.append("INSERT INTO sinteticos_produtos_base (")
    sql_lines.append("    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,")
    sql_lines.append("    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado")
    sql_lines.append(") VALUES (")
    sql_lines.append(f"    '{p['cod_gabisa']}', '{p['nome']}', '{p['nome_tecnico']}', '{p['nicho_principal']}', '{desc}', {termos_sql},")
    sql_lines.append(f"    {p['largura_m']}, {p['peso_metro_linear_kg']}, {p['quantidade_rolo_m']}, {p['peso_rolo_fechado_kg']}, {p['preco_custo_metro']}, {p['preco_custo_rolo_fechado']}")
    sql_lines.append(");\n")

with open('data/seed_produtos.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines))

# 4. Save TABELA_CUSTOS_PRODUTOS.md
md_lines = [
    '# Tabela de Custos e Ficha Técnica - Gabisa Laminados\n',
    '> Dados oficiais consolidados a partir da tabela do fornecedor (Gabisa Laminados). Contém preços de custo por metro, custos e pesos de rolos fechados para frete e nichos de mercado para alimentar os agentes de anúncios, cotação de frete e vendas B2B.\n',
    '## 1. Tabela Resumo de Produtos e Custos\n',
    '| Cód. | Produto | Nicho Principal | Custo/Metro | Metros/Rolo | Custo Rolo Fechado | Peso/Metro | Peso Rolo Fechado |',
    '| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |'
]

for p in produtos:
    md_lines.append(
        f"| **{p['cod_gabisa']}** | **{p['nome']}** | {p['nicho_principal']} | **R$ {p['preco_custo_metro']:.2f}** | {p['quantidade_rolo_m']}m | **R$ {p['preco_custo_rolo_fechado']:.2f}** | {p['peso_metro_linear_kg']:.3f} kg | {p['peso_rolo_fechado_kg']:.1f} kg |"
    )

md_lines.extend([
    '\n## 2. Detalhamento Técnico e Termos de Busca (SEO / Marketplace)\n'
])

for p in produtos:
    termos_formatados = ', '.join(f'`{t}`' for t in p['termos_mercado'])
    md_lines.append(f"### {p['nome']} (Cód. Gabisa: {p['cod_gabisa']})")
    md_lines.append(f"* **Nome Técnico:** {p['nome_tecnico']}")
    md_lines.append(f"* **Sinônimos e Buscas no Mercado:** {termos_formatados}")
    md_lines.append(f"* **Nicho e Usos Recomendados:** {p['aplicacoes']}")
    md_lines.append(f"* **Dimensões e Logística:** Largura de {p['largura_m']}m | Rolo padrão com {p['quantidade_rolo_m']} metros")
    md_lines.append(f"* **Preço de Custo:** R$ {p['preco_custo_metro']:.2f} / metro (Rolo fechado de {p['quantidade_rolo_m']}m = **R$ {p['preco_custo_rolo_fechado']:.2f}**)")
    md_lines.append(f"* **Cálculo de Frete:** {p['peso_metro_linear_kg']:.3f} kg / metro (Rolo fechado para transportadora = **{p['peso_rolo_fechado_kg']:.1f} kg**)\n")

md_lines.extend([
    '## 3. Como os Serviços do Backend Utilizam esses Dados\n',
    '1. **`AdGeneratorService`:** Utiliza o nome comercial e os termos de mercado (`Corino`, `Facto`, `Courvin Náutico`, `Anti-UV`) para gerar anúncios com excelente posicionamento orgânico e conversão nos nichos automotivo, moveleiro e náutico.',
    '2. **`FreightQuoteAgent`:** Utiliza o `peso_rolo_fechado_kg` e a metragem do rolo para orçar frete fracionado com transportadoras e responder perguntas no Mercado Livre.',
    '3. **`OrderDispatcher`:** Controla se o pedido é corte dobrado (peso proporcional à metragem, máx 5m) ou rolo fechado despachado diretamente pela fábrica.',
    '4. **`PostSalesB2B`:** Base de precificação para oferecer condições especiais de atacado (margem calculada sobre o custo do rolo fechado) para profissionais qualificados (tapeceiros e estofadores).'
])

with open('data/TABELA_CUSTOS_PRODUTOS.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print('All 4 files created successfully!')
