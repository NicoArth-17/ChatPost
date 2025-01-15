# Forçar encontrar a pasta scripts para importação do app e database
import sys
import os
# Adicionar o diretório raiz ao sys.path para encontrar 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts import app, database
from scripts.models import Usuario, Post

# Criar arquivo SQL do banco de dados
with app.app_context():
    database.create_all()