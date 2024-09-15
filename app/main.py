import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.connection import create_connection, close_connection, execute_query
from ui.gui import create_main_window

def initialize_database(conn):
    create_tables_script = """
        -- Criação das tabelas (mantida igual)
    """
    execute_query(conn, create_tables_script)
    print("Banco de dados inicializado.")

def main():
    root = tk.Tk()
    root.title("Centro de Distribuição")
    root.geometry("800x600")
    
    database = {
        'host': 'localhost',
        'user': 'root',
        'password': '52r7v41l*',
        'database': 'centro_distribuicao'
    }

    conn = create_connection(database)

    if conn:
        try:
            initialize_database(conn)
        finally:
            close_connection(conn)

    create_main_window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
