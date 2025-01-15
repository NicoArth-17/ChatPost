from scripts import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

# O LoginManager precisa que seja criada uma função para encontrar o usuário a partir dos dados inseridos no login
# Para que o LoginManager reconheça essa função, é inserdo logo acima dela o decorator "@login_manager.user_loader"
@login_manager.user_loader
def load_usuario(id_usuario):

    # Encontrar usuário
    return Usuario.query.get(int(id_usuario))
    # .query.get(deve ser um valor inteiro) -> induz que a busca seja realizada pela PrimaryKey da classe


class Usuario(database.Model, UserMixin):
# UserMixin -> insere na classe as características necessárias para o gerenciamento de login com o LoginManager
    id = database.Column(database.Integer, primary_key=True)
    # primary_key=True -> chave primária com preenchimento automático
    username = database.Column(database.String, nullable=False)
    # nullable=False -> não pode ser nulo
    email = database.Column(database.String, nullable=False, unique=True)
    # unique=True -> informação deve ser única
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    cursos = database.Column(database.String, nullable=False, default='Não informado')
    posts = database.relationship('Post', backref='autor', lazy=True)
    # database.relationship(outra tabela, item relacionado nesta tabela, carrega junto as demais informações referente ao item relacionado) -> não cria uma coluna na tabela, se torna apenas uma relação com alguma outra tabela

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    # database.Text -> diferencia da String por se tratar de um texto maior
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    # id_usuario -> será a coluna que carrega a informação do usuário que é autor da postagem
    # database.ForeignKey('NomeDaClasseTodoEmMinúsculo.ItemReferência') -> busca o elemento que será referenciado de outra tabela