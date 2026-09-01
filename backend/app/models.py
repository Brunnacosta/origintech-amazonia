from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


# ============================================================
# MODELO DE USUÁRIO / PRODUTOR
# ============================================================

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"


    # ========================================================
    # IDENTIFICAÇÃO
    # ========================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    senha_hash = db.Column(
        db.String(255),
        nullable=False
    )


    # ========================================================
    # TIPO DE USUÁRIO
    # ========================================================

    tipo = db.Column(
        db.String(20),
        nullable=False,
        default="produtor"
    )


    # ========================================================
    # DADOS DA PROPRIEDADE
    # ========================================================

    propriedade = db.Column(
        db.String(150),
        nullable=True
    )

    municipio = db.Column(
        db.String(100),
        nullable=True
    )

    vicinal = db.Column(
        db.String(150),
        nullable=True
    )


    # ========================================================
    # LOCALIZAÇÃO GEOGRÁFICA
    # ========================================================

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )


    # ========================================================
    # CONTROLE DA CONTA
    # ========================================================

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ========================================================
    # REPRESENTAÇÃO
    # ========================================================

    def __repr__(self):

        return f"<Usuario {self.nome}>"


# ============================================================
# MODELO DE LOTE
# ============================================================

class Lote(db.Model):

    __tablename__ = "lotes"


    # ========================================================
    # IDENTIFICAÇÃO
    # ========================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )


    # ========================================================
    # DADOS DA COLHEITA
    # ========================================================

    data_colheita = db.Column(
        db.Date,
        nullable=False
    )

    quantidade_kg = db.Column(
        db.Float,
        nullable=False
    )


    # ========================================================
    # QUALIDADE E BENEFICIAMENTO
    # ========================================================

    fermentacao = db.Column(
        db.String(100),
        nullable=False
    )

    secagem = db.Column(
        db.String(100),
        nullable=False
    )

    umidade = db.Column(
        db.Float,
        nullable=True
    )

    sistema_producao = db.Column(
        db.String(100),
        nullable=True
    )


    # ========================================================
    # RELACIONAMENTO COM O PRODUTOR
    # ========================================================

    produtor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    produtor = db.relationship(
        "Usuario",
        backref="lotes"
    )


    # ========================================================
    # CONTROLE
    # ========================================================

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ========================================================
    # REPRESENTAÇÃO
    # ========================================================

    def __repr__(self):

        return f"<Lote {self.codigo}>"