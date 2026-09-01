from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
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

        # Verifica se o e-mail já existe
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

        # Cria o hash da senha
        senha_hash = bcrypt.generate_password_hash(
            form.senha.data
        ).decode("utf-8")

        # Cria o usuário
        usuario = Usuario(

            nome=form.nome.data,
            email=form.email.data,
            senha_hash=senha_hash,
            tipo=form.tipo.data,

            propriedade=form.propriedade.data,
            municipio=form.municipio.data,
            vicinal=form.vicinal.data,

            latitude=form.latitude.data,
            longitude=form.longitude.data
        )

        # Salva no banco
        db.session.add(usuario)
        db.session.commit()

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


# ============================================================
# MINHA PROPRIEDADE
# ============================================================

@auth.route("/propriedade")
@login_required
def minha_propriedade():

    return render_template(
        "minha_propriedade.html",
        usuario=current_user
    )


# ============================================================
# EDITAR INFORMAÇÕES DA PROPRIEDADE
# ============================================================

@auth.route(
    "/propriedade/editar",
    methods=["GET", "POST"]
)
@auth.route(
    "/propriedade/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_propriedade():

    if request.method == "POST":

        # --------------------------------------------------------
        # Atualiza somente os dados da propriedade
        # --------------------------------------------------------

        current_user.propriedade = request.form.get(
            "propriedade"
        )

        current_user.municipio = request.form.get(
            "municipio"
        )

        current_user.vicinal = request.form.get(
            "vicinal"
        )


        # --------------------------------------------------------
        # Salva alterações
        # --------------------------------------------------------

        db.session.commit()


        flash(
            "Dados da propriedade atualizados com sucesso!",
            "success"
        )


        return redirect(
            url_for("auth.minha_propriedade")
        )


    return render_template(
        "editar_propriedade.html",
        usuario=current_user
    )


# ============================================================
# ATUALIZAR LOCALIZAÇÃO
# ============================================================

@auth.route(
    "/propriedade/localizacao",
    methods=["GET", "POST"]
)
@login_required
def atualizar_localizacao():

    if request.method == "POST":

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )

        # Verifica se os dois valores foram enviados
        if not latitude or not longitude:

            flash(
                "Não foi possível obter sua localização.",
                "danger"
            )

            return redirect(
                url_for("auth.atualizar_localizacao")
            )

        try:

            current_user.latitude = float(
                latitude
            )

            current_user.longitude = float(
                longitude
            )

        except ValueError:

            flash(
                "A localização recebida não é válida.",
                "danger"
            )

            return redirect(
                url_for("auth.atualizar_localizacao")
            )

        # Salva a nova localização
        db.session.commit()

        flash(
            "Localização atualizada com sucesso!",
            "success"
        )

        return redirect(
            url_for("auth.minha_propriedade")
        )

    return render_template(
        "atualizar_localizacao.html",
        usuario=current_user
    )