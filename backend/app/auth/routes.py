from flask import Blueprint, render_template, redirect, url_for, flash

from app.auth.forms import CadastroForm
from app.extensions import db, bcrypt
from app.models import Usuario

auth = Blueprint("auth", __name__)


@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    form = CadastroForm()

    if form.validate_on_submit():

        usuario_existente = Usuario.query.filter_by(
            email=form.email.data
        ).first()

        if usuario_existente:

            flash(
                "Já existe um usuário com esse e-mail.",
                "danger"
            )

            return redirect(url_for("auth.cadastro"))

        senha_hash = bcrypt.generate_password_hash(
            form.senha.data
        ).decode("utf-8")

        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=senha_hash,
            tipo=form.tipo.data
        )

        db.session.add(usuario)
        db.session.commit()

        flash(
            "Conta criada com sucesso!",
            "success"
        )

        return redirect(url_for("auth.cadastro"))

    return render_template(
        "cadastro.html",
        form=form
    )