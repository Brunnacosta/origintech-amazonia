from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DateField,
    FloatField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional
)


# ============================================================
# FORMULÁRIO DE CADASTRO E EDIÇÃO DE LOTE
# ============================================================

class LoteForm(FlaskForm):

    # ========================================================
    # IDENTIFICAÇÃO DO LOTE
    # ========================================================

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


    # ========================================================
    # DADOS DA COLHEITA
    # ========================================================

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


    # ========================================================
    # BENEFICIAMENTO
    # ========================================================

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


    # ========================================================
    # QUALIDADE
    # ========================================================

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


    # ========================================================
    # BOTÃO
    # ========================================================

    submit = SubmitField(
        "Cadastrar lote"
    )