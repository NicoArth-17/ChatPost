from scripts import app, database, bcrypt
from flask import render_template, url_for, request, flash, redirect, abort
from scripts.forms import FormLogin, FormCriarConta, FormEdit, FormPostar
from scripts.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


# Criar página home
@app.route('/')
# @ -> Decorator: tem a função de atribuir uma nova funcionalidade para o código abaixo dele. Neste caso irá atribuir a função home à uma URL
# .route('URL') -> é um método de app que permite diferenciar as URLs das péginas
def home():

    # Selecionar todos os posts do banco de dados
    posts = Post.query.order_by(Post.id.desc())
    # Post.id.desc() -> Ordenar os posts por ordem descrescente para que os últimos apareçam por cima no feed

    return render_template('home.html', postHTML=posts)
    # render_template -> retorna o arquivo HTML localizado na pasta de template

# Criar página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Criar página de usuários
@app.route('/usuarios')
@login_required
# login_required -> diz que a rota somente será acessada se o usuário estiver logado
def usuarios():

    # Lista de usuários
    lista_usuarios = Usuario.query.all()

    return render_template('usuarios.html', lista_usuariosHTML=lista_usuarios)

# Criar página de acesso
@app.route('/acesso', methods=['GET', 'POST'])
# methods=['GET', 'POST'] -> Permite pegar e enviar informações (necessário para os formulários)
def acesso():

    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    # Validação de dados inseridos e ação após submit formulário de login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
    # request.form -> valida quando é feita a requisição Post do formulário, ou seja, quando o botao submit é acionado

        # Tentar encontrar usuário pelo email inserido
        user = Usuario.query.filter_by(email=form_login.email.data).first()

        # Se os dados inseridos nos campos de login (email e senha) forem encontrados
        if user and bcrypt.check_password_hash(user.senha, form_login.senha.data):
        # bcrypt.check_password_hash(senha do usuário no banco de dados, senha inserida no campo para login) -> Faz uma comparação do texto inserido com a senha criptografada no banco de dados

            # Efetivar login para LoginManager
            login_user(user, remember=form_login.lembrar_login.data)
            # remember=True/False -> permite q as informações de acesso sejam guardas. True = CheckBox marcado / False = CheckBox desmarcado

            # Exibir uma mensagem pop-up
            # Uma mensagem flash se trata de um pop-up com um texto informativo que aparece uma vez e some ao atualizar a página
            flash(f'Login efetuado com sucesso no e-mail {form_login.email.data}', 'alert-success')
            # flash(mensagem que irá ser exibida, classe bootstrap para categoria do pop-up)

            # Quando o usuário for redirecionado para a página de acesso pelo login_view/login_required irá aparecer o parâmeto de URL "next"
            # Vou usar este parametro para reconhecer que ao logar nessa página redirecionada, o usuário não irá pra página de login, mas irá acessar a página que tentou antes de estar logado
            # Pegar parâmetro "next"
            p_next = request.args.get('next')
            
            # se existir o parâmetro
            if p_next:
                return redirect(p_next)
            
            # Se não existir redireciona normalmente para home
            else:
                # Redirecionar página
                return redirect(url_for('home'))
        
        # Se os dados inseridos nos campos de login (email e senha) não forem encontrados
        else:

            flash(f'Informações de login inválidas', 'alert-danger')

    # Validação de dados inseridos e ação após submit formulário de criar conta
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:

        # Criptografar senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        user = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)

        database.session.add(user)
        database.session.commit()

        flash(f'Conta criada com sucesso no e-mail {form_criarconta.email.data}', 'alert-success')

        return redirect(url_for('home'))


    return render_template('acesso.html', formlogin=form_login, formcriarconta=form_criarconta)


# Criar página de perfil
@app.route('/perfil')
@login_required
def perfil():

    
    return render_template('perfil.html')

def tratar_imagem(img):
    # Modificando nome do arquivo de imagem
    cod = secrets.token_hex(8)
    nome_img, formato = os.path.splitext(img.filename)
    nome_img_definitivo = nome_img + cod + formato

    # Configurar caminho
    caminho = os.path.join(app.root_path, 'static/FotoPerfil', nome_img_definitivo)

    # Configurar tamanho
    tamanho = (160, 160)
    img_redimensionada = Image.open(img)
    img_redimensionada.thumbnail(tamanho)
    img_redimensionada.save(caminho)

    return nome_img_definitivo

# Criar página de perfil
@app.route('/perfil/edit', methods=['GET', 'POST'])
@login_required
def editar_perfil():

    # Formulário para editar perfil
    form_edit = FormEdit()

    # Função para editar cursos que serão exibidos no perfil
    def editar_cursos(formulario):

        lista_cursos = []

        # percorrer os campos do fomrulário de edição
        for campo in formulario:

            # se no nome do campo conter "curso_"
            if 'curso_' in campo.name:

                # se o campo estiver marcado
                if campo.data:
                
                    lista_cursos.append(campo.label.text)
                    # campo.label.text -> No HTML apenas o .label é necessário para exibir o texto do campo, porém o python entende com um objeto, assim sendo necessário o .text para pegar o nome

        return ';'.join(lista_cursos)
        # ';'.join(lista_cursos) -> como a coluna do banco de dados que irá armazenar o os cursos do usuário está definida para aceitar String, então o join será usado para pegar todos os itens da lista e juntá-los separando por ';'



    # Validações do formuário e ação após botão submit
    if form_edit.validate_on_submit():

        # Editar propriedades do usuário com as informações inseridas
        current_user.email = form_edit.email.data
        current_user.username = form_edit.username.data

        if form_edit.foto_perfil.data:
            nome_imagem = tratar_imagem(form_edit.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        current_user.cursos = editar_cursos(form_edit)

        # Efetivar mudanças no banco de dados
        database.session.commit()

        flash('Perfil atualizado com sucesso', 'alert-success')

        return redirect(url_for('perfil'))
    
    # Manter os campos do formulário de edição preenchidos com os dados do usuário corrente
    elif request.method == 'GET':

        form_edit.email.data = current_user.email
        form_edit.username.data = current_user.username

    return render_template('editarperfil.html', formedit=form_edit)


# Criar página de postagem
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    
    form_post = FormPostar()

    if form_post.validate_on_submit():

        post = Post(titulo=form_post.titulo.data,
                    corpo=form_post.corpo.data, 
                    autor=current_user)
        
        database.session.add(post)
        database.session.commit()

        flash('Post criado com sucesso', 'alert-success')
        
        return redirect(url_for('home'))

    return render_template('criarpost.html', formpost=form_post)


# Criar página de logout
@app.route('/sair')
@login_required
def sair():

    # Efetivar logout para LoginManager
    logout_user()

    flash(f'Logout efetuado com sucesso.', 'alert-success')

    return redirect(url_for('home'))


# Criar página para o post
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):

    # o post será selecionado no banco de dados pelo get pegando diretamente pelo seu ID presente na rota da página
    post = Post.query.get(post_id)

    #  Se o autor do post for o usuário atual
    if current_user == post.autor:

        # formulário para editar post
        form_editarpost = FormPostar()

        # Se o metodo for get
        if request.method == 'GET':

            # Manter o formuláro preenchido para edição
            form_editarpost.titulo.data = post.titulo
            form_editarpost.corpo.data = post.corpo

        elif form_editarpost.validate_on_submit():

            post.titulo = form_editarpost.titulo.data
            post.corpo = form_editarpost.corpo.data

            # Já podemos dar um commit direto sem o 'add' pois estamos editando algo que já está no banco de dados
            database.session.commit()

            flash('Post editado com sucesso', 'alert-success')

            return redirect(url_for('home'))

    else:
        
        # formulário para editar post = None
        form_editarpost = None

    return render_template('post.html', postHTML=post, formeditarpost=form_editarpost)


# Criar página para excluir o post
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):

    post = Post.query.get(post_id)

    if current_user == post.autor:

        database.session.delete(post)
        database.session.commit()

        flash('Post excluído com sucesso', 'alert-danger')

        return redirect(url_for('home'))
    
    else:

        abort(403)