-- CENTRO DE DISTRIBUIÇÃO - TRABALHO 2 DE BANCO DE DADOS 2024.2

create database centro_distribuicao;
use centro_distribuicao;

-- Criação da tabela 'produtos'
CREATE TABLE produtos (
    pid INT AUTO_INCREMENT PRIMARY KEY,  -- Identificador único do produto (chave primária)
    nome VARCHAR(255) NOT NULL,           -- Nome do produto
    categoria VARCHAR(255) NOT NULL,      -- Categoria do produto
    quantidade_minima INT NOT NULL        -- Quantidade mínima permitida no estoque
);

-- Criação da tabela 'estoque'
CREATE TABLE estoque (
    estoque_id INT AUTO_INCREMENT PRIMARY KEY,  -- Identificador único do estoque (chave primária)
    pid INT,                                    -- Relacionamento com a tabela 'produtos'
    quantidade_atual INT NOT NULL,              -- Quantidade atual em estoque
    CONSTRAINT fk_produto FOREIGN KEY (pid) REFERENCES produtos(pid)
);

-- Implementação do Trigger 'before_venda'
DELIMITER $$

CREATE TRIGGER before_venda
BEFORE UPDATE ON estoque
FOR EACH ROW
BEGIN
    DECLARE min_qtd INT;

    -- Obtém a quantidade mínima permitida para o produto
    SELECT quantidade_minima INTO min_qtd FROM produtos WHERE pid = NEW.pid;

    -- Verifica se a quantidade em estoque após a venda será menor que a quantidade mínima permitida
    IF (NEW.quantidade_atual < min_qtd) THEN
        -- Exibe uma mensagem de aviso e permite a venda
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Atenção: A quantidade em estoque ficará abaixo da quantidade mínima permitida.';
    END IF;

    -- Impede a operação se a quantidade for menor que 0
    IF (NEW.quantidade_atual < 0) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Operação inválida: A quantidade em estoque não pode ser menor que 0.';
    END IF;
END$$

DELIMITER ;

CREATE TABLE fornecedores (
    fornecedor_id INT AUTO_INCREMENT PRIMARY KEY,  -- Identificador único do fornecedor (chave primária)
    nome VARCHAR(255) NOT NULL,                    -- Nome do fornecedor
    cnpj VARCHAR(18) NOT NULL,                     -- CNPJ do fornecedor
    contato VARCHAR(255)                           -- Informação de contato do fornecedor
);

CREATE TABLE produtos_fornecedores (
    pid INT,                                      -- Relacionamento com a tabela 'produtos'
    fornecedor_id INT,                            -- Relacionamento com a tabela 'fornecedores'
    preco DECIMAL(10, 2) NOT NULL,                -- Preço do produto fornecido
    PRIMARY KEY (pid, fornecedor_id),             -- Chave primária composta
    CONSTRAINT fk_produto_pf FOREIGN KEY (pid) REFERENCES produtos(pid),
    CONSTRAINT fk_fornecedor_pf FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(fornecedor_id)
);

CREATE TABLE categorias (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único da categoria
    nome_categoria VARCHAR(255) NOT NULL         -- Nome da categoria
);

ALTER TABLE produtos 
ADD COLUMN categoria_id INT,                        -- Adiciona a coluna categoria_id
ADD CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id); -- Chave estrangeira para categorias

CREATE TABLE historico_entrada_saida (
    historico_id INT AUTO_INCREMENT PRIMARY KEY,
    pid INT NOT NULL,
    fornecedor_id INT,
    quantidade INT NOT NULL,
    tipo_operacao ENUM('entrada', 'saída') NOT NULL,
    data_operacao DATE NOT NULL,
    data_pedido DATE,
    data_entrega DATE,
    loja_destino VARCHAR(255),
    peso_total DECIMAL(10, 2),
    FOREIGN KEY (pid) REFERENCES produtos(pid),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(fornecedor_id)
);

-- Trigger para Atualização após Entrada
DELIMITER //

CREATE TRIGGER atualizar_estoque_entrada
AFTER INSERT ON historico_entrada_saida
FOR EACH ROW
BEGIN
    IF NEW.tipo_operacao = 'entrada' THEN
        UPDATE estoque
        SET quantidade_atual = quantidade_atual + NEW.quantidade
        WHERE pid = NEW.pid;
    END IF;
END;

//

DELIMITER ;

-- Trigger para Atualização após Saída
DELIMITER //

CREATE TRIGGER atualizar_estoque_saida
AFTER INSERT ON historico_entrada_saida
FOR EACH ROW
BEGIN
    IF NEW.tipo_operacao = 'saída' THEN
        UPDATE estoque
        SET quantidade_atual = quantidade_atual - NEW.quantidade
        WHERE pid = NEW.pid;
    END IF;
END;

//

DELIMITER ;

ALTER TABLE historico_entrada_saida
ADD COLUMN tipo_entrada ENUM('compra', 'devolução') DEFAULT 'compra';

ALTER TABLE historico_entrada_saida
ADD COLUMN tempo_entrega INT; -- Tempo de entrega em dias

DELIMITER //

CREATE TRIGGER calcular_tempo_entrega
BEFORE INSERT ON historico_entrada_saida
FOR EACH ROW
BEGIN
    IF NEW.tipo_entrada = 'compra' AND NEW.data_pedido IS NOT NULL AND NEW.data_entrega IS NOT NULL THEN
        SET NEW.tempo_entrega = DATEDIFF(NEW.data_entrega, NEW.data_pedido);
    ELSE
        SET NEW.tempo_entrega = NULL; -- Ou outro valor padrão, se necessário
    END IF;
END;

//

DELIMITER ;

ALTER TABLE produtos
ADD COLUMN peso DECIMAL(10, 2); -- Peso do produto com até duas casas decimais

DELIMITER //

CREATE TRIGGER calcular_peso_total
BEFORE INSERT ON historico_entrada_saida
FOR EACH ROW
BEGIN
    DECLARE peso_unitario DECIMAL(10, 2);

    -- Obter o peso unitário do produto
    SELECT peso INTO peso_unitario
    FROM produtos
    WHERE pid = NEW.pid;

    -- Calcular o peso total
    SET NEW.peso_total = peso_unitario * NEW.quantidade;
END;

//

DELIMITER ;

ALTER TABLE estoque
ADD COLUMN abaixo_qtd_minima BOOLEAN DEFAULT FALSE;

DELIMITER //

DELIMITER //

CREATE TRIGGER verificar_qtd_minima
BEFORE UPDATE ON estoque
FOR EACH ROW
BEGIN
    -- Verificar se a quantidade atual está abaixo da quantidade mínima
    IF NEW.quantidade_atual <= (SELECT quantidade_minima FROM produtos WHERE pid = NEW.pid) THEN
        SET NEW.abaixo_qtd_minima = TRUE;
    ELSE
        SET NEW.abaixo_qtd_minima = FALSE;
    END IF;
END;

//

DELIMITER ;

ALTER TABLE historico_entrada_saida
ADD COLUMN transportadora VARCHAR(255);


select * from fornecedores;
select * from categorias;