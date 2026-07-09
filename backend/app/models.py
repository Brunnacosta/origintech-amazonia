from datetime import datetime

from app.extensions import db


class Usuario(db.Model):
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