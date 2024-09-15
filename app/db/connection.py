import pymysql

def create_connection(db_config):
    """
    Cria uma conexão com o banco de dados MySQL especificado.
    
    :param db_config: Dicionário com as configurações de conexão MySQL.
    :return: Conexão ao banco de dados ou None em caso de falha.
    """
    conn = None
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        print(f"Conexão estabelecida com o banco de dados {db_config['database']}.")
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def close_connection(conn):
    """
    Fecha a conexão com o banco de dados.
    
    :param conn: Conexão ao banco de dados.
    """
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada.")


def execute_query(conn, query, params=()):
    """
    Executa uma consulta SQL no banco de dados.
    
    :param conn: Conexão ao banco de dados.
    :param query: Consulta SQL a ser executada.
    :param params: Parâmetros da consulta SQL.
    :return: Resultado da consulta.
    """
    cur = conn.cursor()
    try:
        for statement in query.split(';'):
            if statement.strip():
                cur.execute(statement.strip(), params)
                cur.fetchall()  # Consume any results
        conn.commit()
        print("Query executed successfully.")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        cur.close()

# Funções para manipulação de dados
def add_product(name, category, quantity):
    conn = create_connection({'host': 'localhost', 'user': 'root', 'password': '52r7v41l*', 'database': 'centro_distribuicao'})
    if conn:
        query = "INSERT INTO produtos (nome, categoria, quantidade) VALUES (%s, %s, %s)"
        execute_query(conn, query, (name, category, quantity))
        close_connection(conn)

def delete_product(product_id):
    conn = create_connection({'host': 'localhost', 'user': 'root', 'password': '52r7v41l*', 'database': 'centro_distribuicao'})
    if conn:
        query = "DELETE FROM produtos WHERE pid = %s"
        execute_query(conn, query, (product_id,))
        close_connection(conn)

def add_category(name):
    conn = create_connection({'host': 'localhost', 'user': 'root', 'password': '52r7v41l*', 'database': 'centro_distribuicao'})
    if conn:
        query = "INSERT INTO categorias (nome) VALUES (%s)"
        execute_query(conn, query, (name,))
        close_connection(conn)

def delete_category(category_id):
    conn = create_connection({'host': 'localhost', 'user': 'root', 'password': '52r7v41l*', 'database': 'centro_distribuicao'})
    if conn:
        query = "DELETE FROM categorias WHERE cid = %s"
        execute_query(conn, query, (category_id,))
        close_connection(conn)

def add_supplier(name):
    conn = create_connection({'host': 'localhost', 'user': 'root', 'password': '52r7v41l*', 'database': 'centro_distribuicao'})
    if conn:
        query = "INSERT INTO fornecedores (nome) VALUES (%s)"
        execute_query(conn, query, (name,))
        close_connection(conn)

def delete_supplier(supplier_id):
    conn = create_connection({'host': 'localhost', 'user': 'root', 'password': '52r7v41l*', 'database': 'centro_distribuicao'})
    if conn:
        query = "DELETE FROM fornecedores WHERE fid = %s"
        execute_query(conn, query, (supplier_id,))
        close_connection(conn)
