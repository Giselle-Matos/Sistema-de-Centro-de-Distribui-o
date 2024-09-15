import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.connection import create_connection, close_connection
import pymysql
from app.db.queries import (
    GET_ALL_PRODUCTS,
    GET_PRODUCTS_BY_SUPPLIER,
    GET_SUPPLIERS_BY_PRODUCT,
    GET_PRODUCTS_BY_CATEGORY,
    GET_MONTHLY_REVENUE_BY_STORE,
    GET_YEARLY_REVENUE_BY_STORE,
    GET_REVENUE_BY_DATE_RANGE,
    GET_CARRIERS_USAGE_COUNT,
    GET_CATEGORY_WITH_MOST_ITEMS,
    GET_PRODUCTS_BELOW_MIN_QUANTITY,
    GET_PRODUCT_MOVEMENT_HISTORY,
    GET_PRODUCTS_MORE_THAN_DAYS_IN_STOCK,
    GET_MOST_ACTIVE_SUPPLIERS,
    GET_MOST_SOLD_PRODUCT_IN_PERIOD,
    GET_AVERAGE_DELIVERY_TIME_PER_SUPPLIER,
    GET_TOTAL_PRODUCTS_BY_CARRIER,
    GET_RECENTLY_ADDED_PRODUCTS,
    GET_PRODUCT_WITH_LONGEST_STOCK_DURATION,
    GET_SALES_PERFORMANCE_BY_CATEGORY,
    ADD_PRODUCT_QUERY,
    DELETE_PRODUCT_QUERY
)

def add_categoria(nome_categoria):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO categorias (nome_categoria) VALUES (%s)"
            cursor.execute(query, (nome_categoria,))
            connection.commit()
            print("Categoria added successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding categoria: {e}")
        finally:
            close_connection(connection)

def delete_categoria(categoria_id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM categorias WHERE categoria_id = %s"
            cursor.execute(query, (categoria_id,))
            connection.commit()
            print("Categoria deleted successfully.")
        except pymysql.MySQLError as e:
            print(f"Error deleting categoria: {e}")
        finally:
            close_connection(connection)


def add_fornecedor(nome, cnpj, contato):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO fornecedores (nome, cnpj, contato) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, cnpj, contato))
            connection.commit()
            print("Fornecedor added successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding fornecedor: {e}")
        finally:
            close_connection(connection)

def delete_fornecedor(fornecedor_id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM fornecedores WHERE fornecedor_id = %s"
            cursor.execute(query, (fornecedor_id,))
            connection.commit()
            print("Fornecedor deleted successfully.")
        except pymysql.MySQLError as e:
            print(f"Error deleting fornecedor: {e}")
        finally:
            close_connection(connection)

def get_category_id(category_name):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT categoria_id FROM categorias WHERE nome_categoria = %s"
            cursor.execute(query, (category_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        finally:
            close_connection(connection)
    return None

def add_product(name, category, category_id, quantity, weight):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO produtos (nome, categoria, categoria_id, quantidade_minima, peso) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, category, category_id, quantity, weight))
            connection.commit()
            print("Product added successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding product: {e}")
        finally:
            close_connection(connection)



def delete_product(product_id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(DELETE_PRODUCT_QUERY, (product_id,))
        conn.commit()
        close_connection(conn)

def registrar_saida(pid, quantidade, data_operacao, loja_destino, transportadora):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO historico_entrada_saida 
            (pid, quantidade, tipo_operacao, data_operacao, loja_destino, transportadora) 
            VALUES (%s, %s, 'saída', %s, %s, %s)
            """
            cursor.execute(query, (pid, quantidade, data_operacao, loja_destino, transportadora))
            connection.commit()
            print("Saída registrada com sucesso.")
            return True
        except pymysql.MySQLError as e:
            print(f"Erro ao registrar saída: {e}")
            return False
        finally:
            close_connection(connection)
    return False





def registrar_entrada(pid, fornecedor_id, quantidade, data_operacao, data_pedido, data_entrega):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    connection = create_connection(db_config)
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO historico_entrada_saida 
            (pid, fornecedor_id, quantidade, tipo_operacao, data_operacao, data_pedido, data_entrega) 
            VALUES (%s, %s, %s, 'entrada', %s, %s, %s)
            """
            cursor.execute(query, (pid, fornecedor_id, quantidade, data_operacao, data_pedido, data_entrega))
            connection.commit()
            print("Entrada registrada com sucesso.")
            return True
        except pymysql.MySQLError as e:
            print(f"Erro ao registrar entrada: {e}")
            return False
        finally:
            close_connection(connection)
    return False


def get_all_categorias():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()
        close_connection(conn)
        return categorias


def get_all_fornecedores():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fornecedores")
        fornecedores = cursor.fetchall()
        close_connection(conn)
        return fornecedores


def get_all_products():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_ALL_PRODUCTS)
        products = cursor.fetchall()
        close_connection(conn)
        return products

def get_products_by_supplier(supplier_id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_PRODUCTS_BY_SUPPLIER, (supplier_id,))
        products = cursor.fetchall()
        close_connection(conn)
        return products
    

def get_suppliers_by_product():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT p.nome AS produto, 
               GROUP_CONCAT(CONCAT(f.nome, ' (R$ ', FORMAT(pf.preco, 2), ')') ORDER BY f.nome ASC SEPARATOR ', ') AS fornecedores
        FROM produtos p
        JOIN produtos_fornecedores pf ON p.pid = pf.pid
        JOIN fornecedores f ON f.fornecedor_id = pf.fornecedor_id
        GROUP BY p.pid
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results

def get_products_by_category(category_id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_PRODUCTS_BY_CATEGORY, (category_id,))
        products = cursor.fetchall()
        close_connection(conn)
        return products

def get_monthly_revenue_by_store():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_MONTHLY_REVENUE_BY_STORE)
        revenue = cursor.fetchall()
        close_connection(conn)
        return revenue

def get_yearly_revenue_by_store():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_YEARLY_REVENUE_BY_STORE)
        revenue = cursor.fetchall()
        close_connection(conn)
        return revenue

def get_revenue_by_date_range(start_date, end_date):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
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
            loja_destino, ano, mes
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        close_connection(conn)
        return results

    

def get_carriers_usage_count():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT transportadora, 
               SUM(CASE WHEN tipo_operacao = 'entrada' THEN 1 ELSE 0 END) AS entradas,
               SUM(CASE WHEN tipo_operacao = 'saída' THEN 1 ELSE 0 END) AS saidas
        FROM historico_entrada_saida
        WHERE transportadora IS NOT NULL AND transportadora != ''
        GROUP BY transportadora
        HAVING entradas > 0 OR saidas > 0
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results


def get_most_used_carriers():
    carriers_data = get_carriers_usage_count()
    most_used_entrada = max(carriers_data, key=lambda x: x[1])
    most_used_saida = max(carriers_data, key=lambda x: x[2])
    return most_used_entrada, most_used_saida, carriers_data

def get_category_with_most_items():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT c.nome_categoria, COUNT(p.pid) AS total_produtos
        FROM produtos p
        JOIN categorias c ON p.categoria_id = c.categoria_id
        GROUP BY c.nome_categoria
        ORDER BY total_produtos DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results

def get_categories_item_count():
    categories_data = get_category_with_most_items()
    most_items_category = categories_data[0] if categories_data else None
    return most_items_category, categories_data

    

def get_products_below_min_quantity():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_PRODUCTS_BELOW_MIN_QUANTITY)
        products = cursor.fetchall()
        close_connection(conn)
        return products
    
def get_product_movement_history(product_id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT 
            h.historico_id, 
            p.nome AS produto_nome,
            h.quantidade, 
            h.tipo_operacao, 
            h.data_operacao, 
            h.loja_destino,
            COALESCE(f.nome, 'N/A') AS fornecedor_nome,
            h.transportadora
        FROM 
            historico_entrada_saida h
        JOIN 
            produtos p ON h.pid = p.pid
        LEFT JOIN 
            fornecedores f ON h.fornecedor_id = f.fornecedor_id
        WHERE 
            h.pid = %s
        ORDER BY 
            h.data_operacao DESC
        """
        cursor.execute(query, (product_id,))
        history = cursor.fetchall()
        close_connection(conn)
        return history




def get_products_more_than_days_in_stock(days):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute(GET_PRODUCTS_MORE_THAN_DAYS_IN_STOCK, (days,))
        products = cursor.fetchall()
        close_connection(conn)
        return products
    

def get_most_sold_product_in_period(start_date, end_date):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT p.nome, SUM(hs.quantidade) AS total_vendido, 
               SUM(hs.quantidade * pf.preco) AS faturamento_total
        FROM historico_entrada_saida hs
        JOIN produtos p ON hs.pid = p.pid
        JOIN produtos_fornecedores pf ON p.pid = pf.pid
        WHERE hs.tipo_operacao = 'saída'
        AND hs.data_operacao BETWEEN %s AND %s
        GROUP BY p.nome
        ORDER BY total_vendido DESC
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        close_connection(conn)
        return results
def get_supplier_delivery_details():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT f.nome, AVG(h.tempo_entrega) as avg_delivery_time,
               p.nome as product_name, h.tempo_entrega as delivery_time
        FROM historico_entrada_saida h
        JOIN fornecedores f ON h.fornecedor_id = f.fornecedor_id
        JOIN produtos p ON h.pid = p.pid
        WHERE h.tipo_operacao = 'entrada'
        GROUP BY f.fornecedor_id, f.nome, p.pid, p.nome, h.tempo_entrega
        ORDER BY f.nome, avg_delivery_time ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results


    
def get_total_products_by_carrier():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT 
            transportadora, 
            SUM(quantidade) AS total_quantidade,
            SUM(CASE WHEN tipo_operacao = 'entrada' THEN quantidade ELSE 0 END) AS quantidade_entrada,
            SUM(CASE WHEN tipo_operacao = 'saída' THEN quantidade ELSE 0 END) AS quantidade_saida
        FROM historico_entrada_saida
        GROUP BY transportadora
        ORDER BY total_quantidade DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results
    

def get_recently_added_products():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT p.nome, hs.data_operacao, hs.quantidade
        FROM historico_entrada_saida hs
        JOIN produtos p ON hs.pid = p.pid
        WHERE hs.tipo_operacao = 'entrada'
        ORDER BY hs.data_operacao DESC
        LIMIT 10
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results

def get_product_with_longest_stock_duration():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT p.nome, DATEDIFF(CURDATE(), MIN(hs.data_operacao)) AS tempo_no_estoque
        FROM historico_entrada_saida hs
        JOIN produtos p ON hs.pid = p.pid
        WHERE hs.tipo_operacao = 'entrada'
        GROUP BY p.nome
        ORDER BY tempo_no_estoque DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results

def get_sales_performance_by_category():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT c.nome_categoria, SUM(pf.preco * hs.quantidade) AS total_vendido, COUNT(*) AS qtd_vendas
        FROM historico_entrada_saida hs
        JOIN produtos p ON hs.pid = p.pid
        JOIN categorias c ON p.categoria_id = c.categoria_id
        JOIN produtos_fornecedores pf ON hs.pid = pf.pid
        WHERE hs.tipo_operacao = 'saída'
        GROUP BY c.nome_categoria
        ORDER BY total_vendido DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results



def get_monthly_revenue_by_store(store=None):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
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
        """
        if store:
            query += " AND hs.loja_destino = %s"
            cursor.execute(query, (store,))
        else:
            query += " GROUP BY loja_destino"
            cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results

def get_all_stores():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT loja_destino FROM historico_entrada_saida WHERE tipo_operacao = 'saída'")
        stores = cursor.fetchall()
        close_connection(conn)
        return stores
    
    
def get_most_active_suppliers():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT f.nome, COUNT(pf.pid) AS qtd_produtos
        FROM fornecedores f
        JOIN produtos_fornecedores pf ON f.fornecedor_id = pf.fornecedor_id
        GROUP BY f.nome
        ORDER BY qtd_produtos DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        close_connection(conn)
        return results
    
def get_current_inventory():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }
    conn = create_connection(db_config)
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT e.estoque_id, p.pid, p.nome, c.nome_categoria, e.quantidade_atual, e.abaixo_qtd_minima
        FROM estoque e
        JOIN produtos p ON e.pid = p.pid
        LEFT JOIN categorias c ON p.categoria_id = c.categoria_id
        ORDER BY c.nome_categoria, p.nome
        """
        cursor.execute(query)
        inventory = cursor.fetchall()
        close_connection(conn)
        return inventory
