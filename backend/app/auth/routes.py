from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from app.auth.forms import CadastroForm, LoginForm
from app.extensions import db, bcrypt
from app.models import Usuario


auth = Blueprint("auth", __name__)


# ============================================================
# CADASTRO DE USUÁRIO / PRODUTOR
# ============================================================

@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    form = CadastroForm()

    if form.validate_on_submit():

        # --------------------------------------------------------
        # Verifica se o e-mail já está cadastrado
        # --------------------------------------------------------

        usuario_existente = Usuario.query.filter_by(
            email=form.email.data
        ).first()

        if usuario_existente:

            flash(
                "Já existe um usuário com esse e-mail.",
                "danger"
            )

            return redirect(
                url_for("auth.cadastro")
            )


        # --------------------------------------------------------
        # Cria o hash da senha
        # --------------------------------------------------------

        senha_hash = bcrypt.generate_password_hash(
            form.senha.data
        ).decode("utf-8")


        # --------------------------------------------------------
        # Cria o usuário com os dados da conta
        # e os dados da propriedade
        # --------------------------------------------------------

        usuario = Usuario(

            # Dados da conta
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=senha_hash,
            tipo=form.tipo.data,

            # Dados da propriedade
            propriedade=form.propriedade.data,
            municipio=form.municipio.data,
            vicinal=form.vicinal.data,

            # Localização geográfica
            latitude=form.latitude.data,
            longitude=form.longitude.data
        )


        # --------------------------------------------------------
        # Salva no PostgreSQL
        # --------------------------------------------------------

        db.session.add(usuario)
        db.session.commit()


        # --------------------------------------------------------
        # Mensagem de sucesso
        # --------------------------------------------------------

        flash(
            "Conta criada com sucesso!",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "cadastro.html",
        form=form
    )


# ============================================================
# LOGIN
# ============================================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        # --------------------------------------------------------
        # Procura o usuário pelo e-mail
        # --------------------------------------------------------

        usuario = Usuario.query.filter_by(
            email=form.email.data
        ).first()


        if not usuario:

            flash(
                "E-mail ou senha incorretos.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )


        # --------------------------------------------------------
        # Verifica a senha
        # --------------------------------------------------------

        senha_correta = bcrypt.check_password_hash(
            usuario.senha_hash,
            form.senha.data
        )


        if not senha_correta:

            flash(
                "E-mail ou senha incorretos.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )


        # --------------------------------------------------------
        # Cria a sessão do usuário
        # --------------------------------------------------------

        login_user(usuario)


        flash(
            "Login realizado com sucesso!",
            "success"
        )


        return redirect(
            url_for("auth.dashboard")
        )


    return render_template(
        "login.html",
        form=form
    )


# ============================================================
# LOGOUT
# ============================================================

@auth.route("/logout")
def logout():

    logout_user()


    flash(
        "Você saiu da sua conta.",
        "success"
    )


    return redirect(
        url_for("auth.login")
    )


# ============================================================
# DASHBOARD
# ============================================================

@auth.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )