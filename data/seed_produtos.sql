-- ====================================================================
-- Schema e Seed para sinteticos_produtos_base no Supabase
-- Cria a tabela de produtos base com especificações de custo e frete
-- ====================================================================

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

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1008', 'CLASSECOR', 'Laminado Sintético em PVC Extrusado', 'Moveleiro', 'Laminado Sintético em PVC Extrusado. Aplicações: Móveis em geral, sofás, poltronas, cadeiras, pufes, cabeceiras, brindes. Largura: 1.4m.', ARRAY['Tecido Sintético', 'Corino', 'Corano', 'Laminado Sintético'],
    1.4, 0.5, 50, 25.0, 8.8, 440.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1030', 'DUNE 0.9', 'Laminado Sintético em PVC Espalmado 0.9mm', 'Moveleiro / Bolsas', 'Laminado Sintético em PVC Espalmado 0.9mm. Aplicações: Móveis decorativos, estofados, bolsas, nécessaires, brindes de luxo. Largura: 1.4m.', ARRAY['Tecido Sintético', 'Courvin', 'Dune', 'Facto'],
    1.4, 0.78, 30, 23.4, 16.5, 495.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1018', 'NEW AUTOMOTIVO 1.0', 'Laminado Sintético em PVC Espalmado 1.0mm', 'Automotivo', 'Laminado Sintético em PVC Espalmado 1.0mm. Aplicações: Bancos de carros, capotaria automotiva, capas de banco, laterais de portas, volantes, móveis de alta resistência. Largura: 1.4m.', ARRAY['Tecido Sintético', 'Courvin Automotivo', 'Courvin Uruguaio', 'Couro Sintético Automotivo'],
    1.4, 1.022, 30, 30.66, 14.5, 435.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1057', 'BERGAMO 1.0', 'Laminado Sintético em PVC Espalmado 1.0mm (Anti-UV, Anti-Chama, Bactericida, Fungicida)', 'Náutico / Garden', 'Laminado Sintético em PVC Espalmado 1.0mm (Anti-UV, Anti-Chama, Bactericida, Fungicida). Aplicações: Barcos, lanchas, iates, jet ski, móveis para área externa, varandas, piscinas, estofados hospitalares. Largura: 1.4m.', ARRAY['Courvin Náutico', 'Tecido Náutico', 'Courvin Marino', 'Courvin Área Externa'],
    1.4, 1.022, 30, 30.66, 18.5, 555.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1003', 'HONDA', 'Laminado Sintético em PVC Espalmado para Moto', 'Duas Rodas / Motos', 'Laminado Sintético em PVC Espalmado para Moto. Aplicações: Bancos de motos (linha Honda), capas de selim, reformas de bancos de moto. Largura: 1.4m.', ARRAY['Courvin Honda', 'Capa Banco Moto', 'Tecido Sintético Honda'],
    1.4, 0.67, 40, 26.8, 13.5, 540.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1010', 'CEDROMOV', 'Laminado Sintético em PVC Espalmado Liso', 'Duas Rodas / Brindes', 'Laminado Sintético em PVC Espalmado Liso. Aplicações: Bancos de motos acabamento liso, capas, brindes promocionais, pequenos estofados. Largura: 1.4m.', ARRAY['Courvin Liso', 'Courvin para Moto', 'Cedromov'],
    1.4, 0.67, 40, 26.8, 13.5, 540.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1035', 'FAVO CAR', 'Laminado Sintético em PVC Espalmado Gravação Favo/Disco', 'Duas Rodas / Automotivo', 'Laminado Sintético em PVC Espalmado Gravação Favo/Disco. Aplicações: Bancos de motos antiderrapante / favo, detalhes de bancos automotivos, capas e brindes. Largura: 1.4m.', ARRAY['Courvin Favo', 'Courvin Disco', 'Courvin Antiderrapante Moto'],
    1.4, 0.67, 40, 26.8, 14.5, 580.0
);

INSERT INTO sinteticos_produtos_base (
    cod_gabisa, nome, nome_tecnico, nicho_principal, descricao, termos_mercado,
    largura_m, peso_metro_linear_kg, quantidade_rolo_m, peso_rolo_fechado_kg, preco_custo_metro, preco_custo_rolo_fechado
) VALUES (
    '1040', 'HBROS', 'Laminado Sintético em PVC Espalmado Especial Honda Bros', 'Duas Rodas / Motos', 'Laminado Sintético em PVC Espalmado Especial Honda Bros. Aplicações: Bancos de motos linha Honda Bros e trail, capas esportivas, capas sob medida. Largura: 1.4m.', ARRAY['Courvin Honda Bros', 'Capa Banco Bros', 'Courvin Linha Bros'],
    1.4, 0.67, 40, 26.8, 14.5, 580.0
);
