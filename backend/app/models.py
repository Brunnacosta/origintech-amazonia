from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False, index=True)

    senha_hash = db.Column(db.String(255), nullable=False)

    tipo = db.Column(
        db.String(20),
        nullable=False,
        default="produtor"
    )

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Usuario {self.nome}>"



class Lote(db.Model):
    __tablename__ = "lotes"

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

    data_colheita = db.Column(
        db.Date,
        nullable=False
    )

    quantidade_kg = db.Column(
        db.Float,
        nullable=False
    )

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

    produtor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    produtor = db.relationship(
        "Usuario",
        backref="lotes"
    )

    def __repr__(self):
        return f"<Lote {self.codigo}>"    