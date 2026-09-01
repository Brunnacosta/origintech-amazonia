from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    RadioField,
    FloatField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional
)


# ============================================================
# FORMULÁRIO DE CADASTRO
# ============================================================

class CadastroForm(FlaskForm):

    # ========================================================
    # DADOS DA CONTA
    # ========================================================

    nome = StringField(
        "Nome",
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )


    # ========================================================
    # TIPO DE USUÁRIO
    # ========================================================

    tipo = RadioField(
        "Tipo",
        choices=[
            ("produtor", "Produtor"),
            ("comprador", "Comprador")
        ],
        default="produtor"
    )


    # ========================================================
    # DADOS DA PROPRIEDADE
    # ========================================================

    propriedade = StringField(
        "Nome da propriedade",
        validators=[
            Optional(),
            Length(max=150)
        ]
    )

    municipio = StringField(
        "Município",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    vicinal = StringField(
        "Vicinal",
        validators=[
            Optional(),
            Length(max=150)
        ]
    )


    # ========================================================
    # LOCALIZAÇÃO GEOGRÁFICA
    # ========================================================

    latitude = FloatField(
        "Latitude",
        validators=[
            Optional()
        ]
    )

    longitude = FloatField(
        "Longitude",
        validators=[
            Optional()
        ]
    )


    # ========================================================
    # BOTÃO
    # ========================================================

    submit = SubmitField(
        "Criar Conta"
    )


# ============================================================
# FORMULÁRIO DE LOGIN
# ============================================================

class LoginForm(FlaskForm):

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Entrar"
    )