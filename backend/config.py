import os


class Config:

    # ============================================================
    # SEGURANÇA
    # ============================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "origintech-secret-2026"
    )


    # ============================================================
    # BANCO DE DADOS
    # ============================================================

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg://postgres:origin2026@localhost:5432/origintech"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # ============================================================
    # URL BASE DA APLICAÇÃO
    # ============================================================

    BASE_URL = os.getenv(
        "BASE_URL",
        "http://127.0.0.1:5000"
    )