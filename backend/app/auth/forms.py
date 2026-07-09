from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class CadastroForm(FlaskForm):
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

    tipo = RadioField(
        "Tipo",
        choices=[
            ("produtor", "Produtor"),
            ("comprador", "Comprador")
        ],
        default="produtor"
    )

    submit = SubmitField("Criar Conta")