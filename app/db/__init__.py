from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def init_db(app):
    # Cria o engine de conexão com o banco de dados
    engine = create_engine(app.config['DATABASE_URI'])
    
    # Cria todas as tabelas no banco de dados
    Base.metadata.create_all(engine)
    
    # Inicializa o sessionmaker para criar sessões de banco de dados
    Session = sessionmaker(bind=engine)
    
    # Configura o objeto de sessão no app (se necessário)
    app.config['db_session'] = Session()

    return Session

# Opcional: Se houver necessidade de configuração adicional ou inicialização
def configure_db(app):
    # Configure ou inicialize o banco de dados conforme necessário
    pass
