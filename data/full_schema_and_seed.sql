-- ====================================================================
-- BANCO DE DADOS SINTÉTICOS B2B - GABISA LAMINADOS
-- Schema completo e dados iniciais para o Supabase
-- ====================================================================

-- 1. Tabela de Produtos Base
CREATE TABLE IF NOT EXISTS sinteticos_produtos_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cod_gabisa VARCHAR(50) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    nome_tecnico VARCHAR(255),
    nicho_principal VARCHAR(100),
    descricao TEXT,
    termos_mercado TEXT[],
    largura_m NUMERIC(4,2) DEFAULT 1.40,
    peso_metro_linear_kg NUMERIC(6,3) NOT NULL,
    quantidade_rolo_m INTEGER NOT NULL,
    peso_rolo_fechado_kg NUMERIC(6,2) NOT NULL,
    preco_custo_metro NUMERIC(10,2) NOT NULL,
    preco_custo_rolo_fechado NUMERIC(10,2) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabela de Anúncios Gerados
CREATE TABLE IF NOT EXISTS sinteticos_anuncios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    produto_base_id UUID REFERENCES sinteticos_produtos_base(id) ON DELETE CASCADE,
    nicho VARCHAR(100) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL, -- 'corte' ou 'rolo'
    metragem NUMERIC(6,2) NOT NULL,
    modalidade VARCHAR(100) NOT NULL, -- 'etiqueta_marketplace' ou 'frete_fornecedor'
    status VARCHAR(50) DEFAULT 'draft',
    marketplace_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Tabela de Cotações de Frete
CREATE TABLE IF NOT EXISTS sinteticos_cotacoes_frete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cep VARCHAR(10) NOT NULL,
    question_id VARCHAR(100),
    valor NUMERIC(10,2),
    prazo INTEGER, -- dias úteis
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'completed'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tabela de Pedidos
CREATE TABLE IF NOT EXISTS sinteticos_pedidos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id VARCHAR(100) UNIQUE NOT NULL,
    product_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100),
    customer_name VARCHAR(255),
    customer_phone VARCHAR(50),
    quantidade_comprada INTEGER NOT NULL,
    metragem_por_unidade INTEGER NOT NULL,
    is_rolo_fechado BOOLEAN DEFAULT FALSE,
    delivery_details JSONB,
    invoice_details JSONB,
    marketplace_label_url TEXT,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Tabela de Leads B2B (Pós-Venda)
CREATE TABLE IF NOT EXISTS sinteticos_leads_b2b (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    profession VARCHAR(100),
    status VARCHAR(50) DEFAULT 'new', -- 'new', 'contacted', 'converted', 'b2c'
    source VARCHAR(100) DEFAULT 'post_sale_classification',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_cotacoes_cep_date ON sinteticos_cotacoes_frete (cep, created_at);
CREATE INDEX IF NOT EXISTS idx_cotacoes_status ON sinteticos_cotacoes_frete (status);
CREATE INDEX IF NOT EXISTS idx_pedidos_order_id ON sinteticos_pedidos (order_id);
CREATE INDEX IF NOT EXISTS idx_leads_phone ON sinteticos_leads_b2b (phone);

-- Storage: Bucket de etiquetas
INSERT INTO storage.buckets (id, name, public) 
VALUES ('etiquetas', 'etiquetas', true)
ON CONFLICT (id) DO NOTHING;

-- Seed inicial de produtos
INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES 
(
    '1008', 'CLASSECOR', 'Laminado Sintético em PVC Extrusado', 'Moveleiro',
    'Laminado Sintético em PVC Extrusado. Aplicações: Móveis em geral, sofás, poltronas, cadeiras, pufes, cabeceiras, brindes. Largura: 1.4m.',
    ARRAY['Tecido Sintético', 'Corino', 'Corano', 'Laminado Sintético'],
    1.40, 0.500, 50, 25.00, 8.80, 440.00
),
(
    '1030', 'DUNE 0.9', 'Laminado Sintético em PVC Espalmado 0.9mm', 'Moveleiro / Bolsas',
    'Laminado Sintético em PVC Espalmado 0.9mm. Aplicações: Móveis decorativos, estofados, bolsas, nécessaires, brindes de luxo. Largura: 1.4m.',
    ARRAY['Tecido Sintético', 'Courvin', 'Dune', 'Facto'],
    1.40, 0.780, 30, 23.40, 16.50, 495.00
),
(
    '1018', 'NEW AUTOMOTIVO 1.0', 'Laminado Sintético em PVC Espalmado 1.0mm', 'Automotivo',
    'Laminado Sintético em PVC Espalmado 1.0mm. Aplicações: Bancos de carros, capotaria automotiva, capas de banco, laterais de portas, volantes, móveis de alta resistência. Largura: 1.4m.',
    ARRAY['Tecido Sintético', 'Courvin Automotivo', 'Courvin Uruguaio', 'Couro Sintético Automotivo'],
    1.40, 1.022, 30, 30.66, 14.50, 435.00
),
(
    '1057', 'BERGAMO 1.0', 'Laminado Sintético em PVC Espalmado 1.0mm (Anti-UV, Anti-Chama, Bactericida, Fungicida)', 'Náutico / Garden',
    'Laminado Sintético em PVC Espalmado 1.0mm. Aplicações: Barcos, lanchas, iates, jet ski, móveis para área externa, varandas, piscinas, estofados hospitalares. Largura: 1.4m.',
    ARRAY['Courvin Náutico', 'Tecido Náutico', 'Courvin Marino', 'Courvin Área Externa'],
    1.40, 1.022, 30, 30.66, 18.50, 555.00
),
(
    '1003', 'HONDA', 'Laminado Sintético em PVC Espalmado para Moto', 'Duas Rodas / Motos',
    'Laminado Sintético em PVC Espalmado para Moto. Aplicações: Bancos de motos (linha Honda), capas de selim, reformas de bancos de moto. Largura: 1.4m.',
    ARRAY['Courvin Honda', 'Capa Banco Moto', 'Tecido Sintético Honda'],
    1.40, 0.670, 40, 26.80, 13.50, 540.00
),
(
    '1010', 'CEDROMOV', 'Laminado Sintético em PVC Espalmado Liso', 'Duas Rodas / Brindes',
    'Laminado Sintético em PVC Espalmado Liso. Aplicações: Bancos de motos acabamento liso, capas, brindes promocionais, pequenos estofados. Largura: 1.4m.',
    ARRAY['Courvin Liso', 'Courvin para Moto', 'Cedromov'],
    1.40, 0.670, 40, 26.80, 13.50, 540.00
),
(
    '1035', 'FAVO CAR', 'Laminado Sintético em PVC Espalmado Gravação Favo/Disco', 'Duas Rodas / Automotivo',
    'Laminado Sintético em PVC Espalmado Gravação Favo/Disco. Aplicações: Bancos de motos antiderrapante / favo, detalhes de bancos automotivos, capas e brindes. Largura: 1.4m.',
    ARRAY['Courvin Favo', 'Courvin Disco', 'Courvin Antiderrapante Moto'],
    1.40, 0.670, 40, 26.80, 14.50, 580.00
),
(
    '1040', 'HBROS', 'Laminado Sintético em PVC Espalmado Especial Honda Bros', 'Duas Rodas / Motos',
    'Laminado Sintético em PVC Espalmado Especial Honda Bros. Aplicações: Bancos de motos linha Honda Bros e trail, capas esportivas, capas sob medida. Largura: 1.4m.',
    ARRAY['Courvin Honda Bros', 'Capa Banco Bros', 'Courvin Linha Bros'],
    1.40, 0.670, 40, 26.80, 14.50, 580.00
);
