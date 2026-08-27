from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    FloatField,
    SubmitField
)
from wtforms.validators import DataRequired, Optional


class LoteForm(FlaskForm):

    codigo = StringField(
        "Código do lote",
        validators=[
            DataRequired()
        ]
    )

    nome = StringField(
        "Nome do lote",
        validators=[
            DataRequired()
        ]
    )

    data_colheita = DateField(
        "Data da colheita",
        validators=[
            DataRequired()
        ],
        format="%Y-%m-%d"
    )

    quantidade_kg = FloatField(
        "Quantidade (kg)",
        validators=[
            DataRequired()
        ]
    )

    fermentacao = StringField(
        "Fermentação",
        validators=[
            DataRequired()
        ]
    )

    secagem = StringField(
        "Secagem",
        validators=[
            DataRequired()
        ]
    )

    umidade = FloatField(
        "Umidade (%)",
        validators=[
            Optional()
        ]
    )

    sistema_producao = StringField(
        "Sistema de produção",
        validators=[
            Optional()
        ]
    )

    submit = SubmitField(
        "Cadastrar lote"
    )