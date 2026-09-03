from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DateField,
    FloatField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    NumberRange
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
            DataRequired(),
            NumberRange(
                min=0.1,
                message="Informe uma quantidade maior que zero."
            )
        ]
    )


    # ========================================================
    # BENEFICIAMENTO
    # ========================================================

    fermentacao = StringField(
        "Fermentação",
        validators=[
            DataRequired()
        ],
        description="Informe quantos dias o cacau ficou em fermentação."
    )

    secagem = SelectField(
        "Método de secagem",
        choices=[
            ("Natural", "Natural"),
            ("Solar", "Solar"),
            ("Secador", "Secador"),
            ("Mista", "Mista"),
            ("Outro", "Outro")
        ],
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
            Optional(),
            NumberRange(
                min=0,
                max=100,
                message="A umidade deve estar entre 0 e 100%."
            )
        ]
    )

    sistema_producao = SelectField(
        "Sistema de produção",
        choices=[
            ("Agroflorestal", "Agroflorestal"),
            ("Orgânico", "Orgânico"),
            ("Convencional", "Convencional"),
            ("Misto", "Misto"),
            ("Outro", "Outro")
        ],
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
