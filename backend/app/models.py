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
    # DADOS ANTIGOS DA PROPRIEDADE
    #
    # Mantidos temporariamente para podermos migrar os dados
    # existentes para a nova tabela "propriedades".
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
    # LOCALIZAÇÃO ANTIGA
    #
    # Também será migrada para a tabela "propriedades".
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
    # RELACIONAMENTO COM PROPRIEDADES
    # ========================================================

    propriedades = db.relationship(
        "Propriedade",
        back_populates="produtor",
        cascade="all, delete-orphan"
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
# MODELO DE PROPRIEDADE / FAZENDA
# ============================================================

class Propriedade(db.Model):

    __tablename__ = "propriedades"


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


    # ========================================================
    # LOCALIZAÇÃO
    # ========================================================

    municipio = db.Column(
        db.String(100),
        nullable=True
    )

    vicinal = db.Column(
        db.String(150),
        nullable=True
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
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
        back_populates="propriedades"
    )


    # ========================================================
    # RELACIONAMENTO COM LOTES
    # ========================================================

    lotes = db.relationship(
        "Lote",
        back_populates="propriedade"
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

        return f"<Propriedade {self.nome}>"


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
    # RELACIONAMENTO COM A PROPRIEDADE
    # ========================================================

    propriedade_id = db.Column(
        db.Integer,
        db.ForeignKey("propriedades.id"),
        nullable=True
    )

    propriedade = db.relationship(
        "Propriedade",
        back_populates="lotes"
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