def format_currency(amount):
    """
    Formata um valor monetário para o formato de moeda.
    
    :param amount: Valor a ser formatado (deve ser um número).
    :return: Valor formatado como string no formato de moeda (ex: $1,234.56).
    """
    return f"${amount:,.2f}"

def format_date(date_str):
    """
    Formata uma data para o formato legível (dia/mês/ano).
    
    :param date_str: Data no formato YYYY-MM-DD.
    :return: Data formatada como string (ex: 17/08/2024).
    """
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except ValueError:
        return "Data inválida"

def format_product_list(products):
    """
    Formata uma lista de produtos para exibição.
    
    :param products: Lista de dicionários contendo informações de produtos. Cada dicionário deve ter as chaves:
                     'product_id', 'name', 'category_id', 'quantity', 'price', 'date_added'.
    :return: Lista de strings formatadas para exibição.
    """
    formatted_products = []
    for product in products:
        product_str = (
            f"ID: {product.get('product_id', 'N/A')}, "
            f"Nome: {product.get('name', 'N/A')}, "
            f"Categoria: {product.get('category_id', 'N/A')}, "
            f"Quantidade: {product.get('quantity', 0)}, "
            f"Preço: {format_currency(product.get('price', 0))}, "
            f"Data Adição: {format_date(product.get('date_added', 'N/A'))}"
        )
        formatted_products.append(product_str)
    return formatted_products

def format_supplier_list(suppliers):
    """
    Formata uma lista de fornecedores para exibição.
    
    :param suppliers: Lista de dicionários contendo informações de fornecedores. Cada dicionário deve ter as chaves:
                      'supplier_id', 'name', 'contact_info'.
    :return: Lista de strings formatadas para exibição.
    """
    formatted_suppliers = []
    for supplier in suppliers:
        supplier_str = (
            f"ID: {supplier.get('supplier_id', 'N/A')}, "
            f"Nome: {supplier.get('name', 'N/A')}, "
            f"Contato: {supplier.get('contact_info', 'N/A')}"
        )
        formatted_suppliers.append(supplier_str)
    return formatted_suppliers
