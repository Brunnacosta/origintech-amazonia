import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "origintech-secret-2026")

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg://postgres:origin2026@localhost:5432/origintech"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False