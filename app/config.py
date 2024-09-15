import os

class Config:
    """Classe base para configuração do aplicativo."""

    # Caminho para o banco de dados
    DATABASE = 'centro_distribuicao.db'

    # Outras configurações padrão podem ser adicionadas aqui
    DEBUG = False
    SECRET_KEY = 'your_secret_key'  # Use uma chave secreta segura para segurança

class DevelopmentConfig(Config):
    """Configurações específicas para o ambiente de desenvolvimento."""
    
    DEBUG = True

class TestingConfig(Config):
    """Configurações específicas para o ambiente de testes."""
    
    DATABASE = ':memory:'  # Usar banco de dados em memória para testes
    DEBUG = True

class ProductionConfig(Config):
    """Configurações específicas para o ambiente de produção."""

    DEBUG = False

def get_config(environment='development'):
    """
    Retorna a configuração apropriada com base no ambiente especificado.

    :param environment: O ambiente para o qual carregar a configuração (e.g., 'development', 'testing', 'production').
    :return: Classe de configuração apropriada.
    """
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    
    return configs.get(environment, Config)
