from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


# Criar aplicação Flask
app = Flask(__name__)
#  Flask(__name__) -> Permite a biblioteca integrar páginas html, css, arquivos, etc...

# Gerar token pra criptografia
app.config['SECRET_KEY'] = '81ac584e72fc1dd6bcb2043af796889a'

#  Definir criptografia
bcrypt = Bcrypt(app)

# Configurando local e nome do arquivo do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'comunidade.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path
# app.config['SQLALCHEMY_DATABASE_URI'] -> define onde o banco de dados vai se encontrar localmente
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False -> pesquisar no GPT para entender

# Criando banco de dados
database = SQLAlchemy(app)
# SQLAlchemy() -> biblioteca destinada a estruturar o banco de dados (arquivo models.py)

# Criar gerenciador de login: Controla o acesso do login, mantém o usuário logado, etc.
# LoginManager é usado em conjunto com a biblioteca UserMixin no arquivo models.py
login_manager = LoginManager(app)

# Definir a página que o usuário será redirecionado quando tentar entrar em uma rota que exija o login (@login_required) o mesmo não tiver sido efetuado.
login_manager.login_view = 'acesso'
# .login_view = 'nome da função da rota' -> além de definir a página de redirecionamento, gera uma mensagem na página quando é tentado acessar um elemento que exige login sem estar logado

# Personalizar menagem do login_view
login_manager.login_message_category = 'alert-info'

# O arquivo main.py, necessita apenas da importação do app para ser executado, que por sua vez já está vinculado ao Flask e ao SQLAlchemy (configuração do banco de dados). Porém dessa forma as rotas não serão exibidas pois não se encontram neste arquivo.
# Com isso, logo abaixo do código importamos o arquivo de rotas, pois o app não precisa das rotas para executar e as rotas precisão ser executadas após a criação do app.
# No arquivo de rotas, além dos links das páginas, está vinculado os arquivos de formulário e da estrutura do banco de dados.
# Esse processo é chamado de importação circular
from scripts import routes