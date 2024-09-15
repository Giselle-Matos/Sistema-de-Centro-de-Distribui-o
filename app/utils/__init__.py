"""
Módulo utilitário para o projeto de controle de estoque.

Este módulo agrupa funções auxiliares e de validação que são usadas em
diferentes partes do projeto.
"""

# Importa funções de formatação
from .helpers import (
    format_currency,
    format_date,
    format_product_list,
    format_supplier_list
)

# Importa funções de validação
from .validators import (
    validate_product_data,
    validate_supplier_data
)

def init():
    """
    Inicializa o módulo de utilitários.

    Este método pode ser usado para realizar qualquer configuração
    necessária quando o módulo 'utils' é importado.
    """
    print("Módulo de utilitários inicializado.")
