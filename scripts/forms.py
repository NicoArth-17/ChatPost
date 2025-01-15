from flask_wtf import FlaskForm # Define um formulário,
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField # Define campos do formulário
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # Realiza validação dos campos do formulário
from scripts.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
# FlaskForm -> Transforma uma classe python em um formulário
    username = StringField('Nome de usuário', validators=[DataRequired()])
    # StringField('label do campo', lista de validações) -> define um campo de entrada de texto
    # DataRequired() -> campo com preenchimento obrigatório
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    # Email() -> verifica o formato de endereço de e-mail inserido
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    # PasswordField() -> define um campo de entrada de senha
    # Length(6, 20) -> valida se a entrada contem entre 6 e 20 caracteres
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    # EqualTo('nome de outro campo') -> define a mesma validação de outro campo
    botao_submit_criarconta = SubmitField('Criar conta')
    # SubmitField() -> define um botão de submissão das informações

    # Além dos validator em cada campo, esse método importado também funciona para qualquer função criada com o prefixo "validate_"
    # Validar campo de e-mail
    def validate_email(self, email):

        # Buscar email, já iserido por algum usuário no banco de dados, onde o endereço de email seja o mesmo do preenchido no campo
        email_user = Usuario.query.filter_by(email=email.data).first()

        # Se o mesmo email preenchido já for encontrado no banco de dados
        if email_user:

            # Exibir mensagem de erro
            raise ValidationError('Email já cadastrado, utilize outro endereço.')



class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_login = BooleanField('Lembrar dados de login')
    # BooleanField() -> campo booleano, exemplo: check box / não tem validator pois não é um campo obrigatório
    botao_submit_login = SubmitField('Fazer login')


class FormEdit(FlaskForm):
    foto_perfil = FileField('Trocar foto do perfil', validators=[FileAllowed(['jpg', 'png'])])
    # FileField() -> campo para arquivo
    # FileAllowed(lista com a extensão do arquivo que deve ser aceito) -> faz uma validação a partir do formato do arquivo
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nome de usuário', validators=[DataRequired()])

    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_bi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    curso_html = BooleanField('HTML Impressionador')
    curso_css = BooleanField('CSS Impressionador')
    curso_java = BooleanField('Java Impressionador')

    botao_submit_edit = SubmitField('Confirmar edição')

    def validate_email(self, email):

        # Se o email preenchido for diferente do email já cadastrado no usuário corrente
        if current_user.email != email.data:
            
            email_user = Usuario.query.filter_by(email=email.data).first()

            # Se o email já existir cadastrado para outro usuário
            if email_user:

                raise ValidationError('Email já cadastrado, utilize outro endereço.')
            


class FormPostar(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Mensagem', validators=[DataRequired()])
    botao_submit_post = SubmitField('Postar')