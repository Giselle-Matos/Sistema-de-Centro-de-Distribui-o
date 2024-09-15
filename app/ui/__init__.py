# Importa as interfaces CLI e GUI para que possam ser acessadas diretamente através do pacote `ui`
from .cli import cli
from .gui import show_products

# Opcional: Você pode definir uma função de inicialização para configurar ou iniciar a interface
def init_ui(mode='cli'):
    """
    Inicializa a interface de usuário.

    :param mode: Modo de interface ('cli' ou 'gui').
    """
    if mode == 'cli':
        cli()
    elif mode == 'gui':
        show_products()
    else:
        raise ValueError("Modo de interface inválido. Use 'cli' ou 'gui'.")
