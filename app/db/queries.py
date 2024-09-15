# app/db/queries.py

# Consultas para Produtos

# Ajuste a query SQL no código para corresponder às colunas da tabela
ADD_PRODUCT_QUERY = """
INSERT INTO produtos (nome, categoria, quantidade_minima, categoria_id, peso)
VALUES (%s, %s, %s, %s, %s)
"""


DELETE_PRODUCT_QUERY = """
DELETE FROM produtos WHERE pid = %s
"""


GET_ALL_PRODUCTS = """
SELECT * FROM produtos;
"""

GET_PRODUCTS_BY_SUPPLIER = """
SELECT p.nome AS produto, pf.preco AS preco
FROM produtos p
JOIN produtos_fornecedores pf ON p.pid = pf.pid
WHERE pf.fornecedor_id = %s;
"""

GET_PRODUCTS_BY_CATEGORY = """
SELECT p.nome 
FROM produtos p
JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE p.categoria_id = %s;
"""

GET_PRODUCTS_BELOW_MIN_QUANTITY = """
SELECT p.pid, p.nome, e.quantidade_atual, p.quantidade_minima
FROM produtos p
JOIN estoque e ON p.pid = e.pid
WHERE e.abaixo_qtd_minima = TRUE
"""


# Consultas para Fornecedores
GET_SUPPLIERS_BY_PRODUCT = """
SELECT f.nome AS fornecedor, pf.preco AS preco
FROM fornecedores f
JOIN produtos_fornecedores pf ON f.fornecedor_id = pf.fornecedor_id
JOIN produtos p ON p.pid = pf.pid
WHERE p.pid = %s;
"""

GET_PRODUCTS_BY_EACH_SUPPLIER = """
SELECT f.nome AS fornecedor, GROUP_CONCAT(p.nome ORDER BY p.nome ASC SEPARATOR ', ') AS produtos
FROM fornecedores f
JOIN produtos_fornecedores pf ON f.fornecedor_id = pf.fornecedor_id
JOIN produtos p ON p.pid = pf.pid
GROUP BY f.fornecedor_id;
"""

GET_SUPPLIERS_BY_EACH_PRODUCT = """
SELECT p.nome AS produto, GROUP_CONCAT(f.nome ORDER BY f.nome ASC SEPARATOR ', ') AS fornecedores
FROM produtos p
JOIN produtos_fornecedores pf ON p.pid = pf.pid
JOIN fornecedores f ON f.fornecedor_id = pf.fornecedor_id
GROUP BY p.pid;
"""

# Consultas para Histórico de Entrada e Saída
GET_MONTHLY_REVENUE_BY_STORE = """
SELECT 
    loja_destino,
    SUM(pf.preco * hs.quantidade) AS faturamento
FROM 
    historico_entrada_saida hs
JOIN 
    produtos_fornecedores pf ON hs.pid = pf.pid
WHERE 
    hs.tipo_operacao = 'saída'
    AND YEAR(hs.data_operacao) = YEAR(CURDATE())
    AND MONTH(hs.data_operacao) = MONTH(CURDATE())
GROUP BY 
    loja_destino;
"""

GET_YEARLY_REVENUE_BY_STORE = """
SELECT 
    loja_destino,
    MONTH(hs.data_operacao) AS mes,
    SUM(pf.preco * hs.quantidade) AS faturamento
FROM 
    historico_entrada_saida hs
JOIN 
    produtos_fornecedores pf ON hs.pid = pf.pid
WHERE 
    hs.tipo_operacao = 'saída'
    AND YEAR(hs.data_operacao) = YEAR(CURDATE())
GROUP BY 
    loja_destino, mes
ORDER BY 
    loja_destino, mes;
"""

GET_REVENUE_BY_DATE_RANGE = """
SELECT 
    loja_destino,
    MONTH(hs.data_operacao) AS mes,
    YEAR(hs.data_operacao) AS ano,
    SUM(pf.preco * hs.quantidade) AS faturamento
FROM 
    historico_entrada_saida hs
JOIN 
    produtos_fornecedores pf ON hs.pid = pf.pid
WHERE 
    hs.tipo_operacao = 'saída'
    AND hs.data_operacao BETWEEN %s AND %s
GROUP BY 
    loja_destino, ano, mes
ORDER BY 
    loja_destino, ano, mes;
"""

GET_TRANSPORTER_USAGE = """
SELECT 
    transportadora,
    COUNT(*) AS qtd_utilizacao
FROM 
    historico_entrada_saida
WHERE 
    tipo_operacao = 'saída'
GROUP BY 
    transportadora
ORDER BY 
    qtd_utilizacao DESC;
"""

GET_CATEGORY_WITH_MOST_ITEMS = """
SELECT 
    c.nome_categoria, 
    COUNT(p.pid) AS total_produtos
FROM 
    produtos p
JOIN 
    categorias c ON p.categoria_id = c.categoria_id
GROUP BY 
    c.nome_categoria
ORDER BY 
    total_produtos DESC
LIMIT 1;
"""

# Consultas Adicionais
GET_PRODUCT_MOVEMENT_HISTORY = """
SELECT * 
FROM historico_entrada_saida
WHERE pid = %s;
"""

GET_PRODUCTS_MORE_THAN_DAYS_IN_STOCK = """
SELECT p.nome, DATEDIFF(CURDATE(), hs.data_operacao) AS dias_no_estoque
FROM historico_entrada_saida hs
JOIN produtos p ON hs.pid = p.pid
WHERE hs.tipo_operacao = 'entrada'
AND DATEDIFF(CURDATE(), hs.data_operacao) > %s;
"""

GET_MOST_ACTIVE_SUPPLIERS = """
SELECT f.nome_fornecedor, COUNT(pf.pid) AS qtd_produtos
FROM fornecedores f
JOIN produtos_fornecedores pf ON f.fornecedor_id = pf.fornecedor_id
GROUP BY f.nome_fornecedor
ORDER BY qtd_produtos DESC;
"""

GET_MOST_SOLD_PRODUCT_IN_PERIOD = """
SELECT p.nome, SUM(hs.quantidade) AS total_vendido
FROM historico_entrada_saida hs
JOIN produtos p ON hs.pid = p.pid
WHERE hs.tipo_operacao = 'saída'
AND hs.data_operacao BETWEEN %s AND %s
GROUP BY p.nome
ORDER BY total_vendido DESC
LIMIT 1;
"""

GET_AVERAGE_DELIVERY_TIME_PER_SUPPLIER = """
SELECT f.nome_fornecedor, AVG(DATEDIFF(hs.data_entrega, hs.data_pedido)) AS media_dias
FROM historico_entrada_saida hs
JOIN fornecedores f ON hs.fornecedor_id = f.fornecedor_id
WHERE hs.tipo_operacao = 'entrada'
GROUP BY f.nome_fornecedor;
"""

GET_TOTAL_PRODUCTS_BY_TRANSPORTER = """
SELECT transportadora, SUM(quantidade) AS total_quantidade
FROM historico_entrada_saida
WHERE tipo_operacao = 'saída'
GROUP BY transportadora;
"""

GET_RECENTLY_ADDED_PRODUCTS = """
SELECT p.nome, hs.data_operacao
FROM historico_entrada_saida hs
JOIN produtos p ON hs.pid = p.pid
WHERE hs.tipo_operacao = 'entrada'
ORDER BY hs.data_operacao DESC;
"""

GET_PRODUCT_WITH_LONGEST_STAY_IN_STOCK = """
SELECT p.nome, DATEDIFF(CURDATE(), MIN(hs.data_operacao)) AS tempo_no_estoque
FROM historico_entrada_saida hs
JOIN produtos p ON hs.pid = p.pid
WHERE hs.tipo_operacao = 'entrada'
GROUP BY p.nome
ORDER BY tempo_no_estoque DESC
LIMIT 1;
"""

GET_SALES_PER_CATEGORY = """
SELECT c.nome_categoria, SUM(pf.preco * hs.quantidade) AS total_vendido, COUNT(*) AS qtd_vendas
FROM historico_entrada_saida hs
JOIN produtos p ON hs.pid = p.pid
JOIN categorias c ON p.categoria_id = c.categoria_id
JOIN produtos_fornecedores pf ON hs.pid = pf.pid
WHERE hs.tipo_operacao = 'saída'
GROUP BY c.nome_categoria
ORDER BY total_vendido DESC;
"""

# Consulta para Contar o Uso de Transportadoras
GET_CARRIERS_USAGE_COUNT = """
SELECT 
    transportadora,
    COUNT(*) AS qtd_utilizacao
FROM 
    historico_entrada_saida
WHERE 
    tipo_operacao = 'saída'
GROUP BY 
    transportadora
ORDER BY 
    qtd_utilizacao DESC;
"""

# Consulta para Obter o Total de Produtos por Transportadora
GET_TOTAL_PRODUCTS_BY_CARRIER = """
SELECT 
    transportadora,
    SUM(quantidade) AS total_quantidade
FROM 
    historico_entrada_saida
WHERE 
    tipo_operacao = 'saída'
GROUP BY 
    transportadora;
"""

# Consulta para Obter o Produto com a Maior Duração no Estoque
GET_PRODUCT_WITH_LONGEST_STOCK_DURATION = """
SELECT 
    p.nome,
    DATEDIFF(CURDATE(), MIN(hs.data_operacao)) AS tempo_no_estoque
FROM 
    historico_entrada_saida hs
JOIN 
    produtos p ON hs.pid = p.pid
WHERE 
    hs.tipo_operacao = 'entrada'
GROUP BY 
    p.nome
ORDER BY 
    tempo_no_estoque DESC
LIMIT 1;
"""

# Consulta para Obter o Desempenho de Vendas por Categoria
GET_SALES_PERFORMANCE_BY_CATEGORY = """
SELECT 
    c.nome_categoria,
    SUM(pf.preco * hs.quantidade) AS total_vendido,
    COUNT(*) AS qtd_vendas
FROM 
    historico_entrada_saida hs
JOIN 
    produtos p ON hs.pid = p.pid
JOIN 
    categorias c ON p.categoria_id = c.categoria_id
JOIN 
    produtos_fornecedores pf ON hs.pid = pf.pid
WHERE 
    hs.tipo_operacao = 'saída'
GROUP BY 
    c.nome_categoria
ORDER BY 
    total_vendido DESC;
"""
