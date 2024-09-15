import re
from datetime import datetime

def validate_product_data(data):
    """
    Valida os dados do produto.
    
    :param data: dicionário contendo informações do produto. Espera-se que tenha as chaves:
                 'product_id', 'name', 'category_id', 'supplier_id', 'quantity', 'price', 'date_added'.
    :return: Uma lista de mensagens de erro. Se a lista estiver vazia, os dados são considerados válidos.
    """
    errors = []

    # Verificar se todos os campos obrigatórios estão presentes
    required_fields = ['product_id', 'name', 'category_id', 'supplier_id', 'quantity', 'price', 'date_added']
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo obrigatório '{field}' não encontrado.")
    
    # Validar ID do produto
    if 'product_id' in data:
        if not isinstance(data['product_id'], int) or data['product_id'] <= 0:
            errors.append("ID do produto deve ser um número inteiro positivo.")
    
    # Validar nome do produto
    if 'name' in data:
        if not isinstance(data['name'], str) or len(data['name']) == 0:
            errors.append("O nome do produto deve ser uma string não vazia.")
    
    # Validar ID da categoria
    if 'category_id' in data:
        if not isinstance(data['category_id'], int) or data['category_id'] <= 0:
            errors.append("ID da categoria deve ser um número inteiro positivo.")
    
    # Validar ID do fornecedor
    if 'supplier_id' in data:
        if not isinstance(data['supplier_id'], int) or data['supplier_id'] <= 0:
            errors.append("ID do fornecedor deve ser um número inteiro positivo.")
    
    # Validar quantidade
    if 'quantity' in data:
        if not isinstance(data['quantity'], int) or data['quantity'] < 0:
            errors.append("A quantidade deve ser um número inteiro não negativo.")
    
    # Validar preço
    if 'price' in data:
        if not isinstance(data['price'], (int, float)) or data['price'] < 0:
            errors.append("O preço deve ser um número não negativo.")
    
    # Validar data de adição
    if 'date_added' in data:
        try:
            datetime.strptime(data['date_added'], '%Y-%m-%d')
        except ValueError:
            errors.append("A data de adição deve estar no formato YYYY-MM-DD.")

    return errors

def validate_supplier_data(data):
    """
    Valida os dados do fornecedor.
    
    :param data: dicionário contendo informações do fornecedor. Espera-se que tenha as chaves:
                 'supplier_id', 'name', 'contact_info'.
    :return: Uma lista de mensagens de erro. Se a lista estiver vazia, os dados são considerados válidos.
    """
    errors = []

    # Verificar se todos os campos obrigatórios estão presentes
    required_fields = ['supplier_id', 'name', 'contact_info']
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo obrigatório '{field}' não encontrado.")
    
    # Validar ID do fornecedor
    if 'supplier_id' in data:
        if not isinstance(data['supplier_id'], int) or data['supplier_id'] <= 0:
            errors.append("ID do fornecedor deve ser um número inteiro positivo.")
    
    # Validar nome do fornecedor
    if 'name' in data:
        if not isinstance(data['name'], str) or len(data['name']) == 0:
            errors.append("O nome do fornecedor deve ser uma string não vazia.")
    
    # Validar informações de contato
    if 'contact_info' in data:
        if not isinstance(data['contact_info'], str) or len(data['contact_info']) == 0:
            errors.append("As informações de contato devem ser uma string não vazia.")

    return errors

# Adicione funções de validação para outras entidades, se necessário
