# Forçar encontrar a pasta scripts para importação do app e database
import sys
import os
# Adicionar o diretório raiz ao sys.path para encontrar 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts import app, database
from scripts.models import Usuario, Post


# Observação: qualquer manipulação, o SQLSlchemy exige que esteja dentro de um "with app.app_context():"

# Inserir ifnormações no banco de dados
# with app.app_context():

#     # instanciar tabela de Usuario
#     usuario1 = Usuario(username='Nico', email='nico@gmail.com', senha=1234)
#     usuario2 = Usuario(username='Arth', email='arth@gmail.com', senha=4321)

#     # iniciar sessão
#     database.session.add(usuario1)
#     database.session.add(usuario2)

#     # efetivar alterações
#     database.session.commit()


# # Inserir ifnormações no banco de dados 2
# with app.app_context():

#     # instanciar tabela de Post
#     post1 = Post(id_usuario=1, titulo='Primeiro post', corpo='Felicidade n eh ter de td, mas sim amar td q tem!')

#     #  iniciar sessão
#     database.session.add(post1)

#     # efetivar alterações
#     database.session.commit()


# Pegar ifnormações no banco de dados
with app.app_context():

    # meus_usuarios = Usuario.query.all()
    # meus_usuarios = Usuario.query.all()

    # print(f'Todos os usuários: {meus_usuarios}')
    # print(f'Primeiro usuário: {Usuario.query.first().username}')
    # print(f'Segundo usuário: {meus_usuarios[1].username}')

    # print(meus_usuarios)
    # print(meus_usuarios[2].username)
    # print(meus_usuarios[2].email)
    # print(meus_usuarios[2].senha)

    # meus_posts = Post.query.all()

    # print(f'Todos os usuários: {meus_posts}')
    # print(f'Segundo usuário: {meus_posts[0].titulo}')

    # # encontrar usuário que realizou um post
    # print(meus_posts[0].autor.username)
    # # autor -> backref na tabela Usuario do arquivo models.py

    # # consultar cursos do usuário
    # user_cursos = Usuario.query.filter_by(email='nico@email.com').first()

    # print(user_cursos)

    # consultar post
    posts = Post.query.all()

    print(posts[0].autor.foto_perfil)




# # Pegar ifnormações específicas no banco de dados
# with app.app_context():

#     # encontrar usuário com id = 2
#     usuarioX = Usuario.query.filter_by(id=2).all()

#     print(usuarioX[0].email)


# Deletar banco de dados
# with app.app_context():

#     database.drop_all()