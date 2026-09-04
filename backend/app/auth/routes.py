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
from app.models import Usuario, Propriedade


auth = Blueprint("auth", __name__)


# ============================================================
# FUNÇÃO AUXILIAR
# ============================================================

def obter_propriedade_principal():
    """
    Retorna a primeira propriedade cadastrada do usuário.

    Esta função é mantida temporariamente para compatibilidade
    durante a transição da arquitetura antiga para a nova.

    Quando o usuário ainda possui somente os dados antigos
    armazenados em Usuario, cria automaticamente uma Propriedade
    com esses dados.
    """

    propriedade = (
        Propriedade.query
        .filter_by(
            produtor_id=current_user.id
        )
        .order_by(Propriedade.id)
        .first()
    )

    if propriedade:
        return propriedade


    # ========================================================
    # MIGRAÇÃO TEMPORÁRIA DOS DADOS ANTIGOS
    # ========================================================

    if current_user.propriedade:

        propriedade = Propriedade(
            nome=current_user.propriedade,
            municipio=current_user.municipio,
            vicinal=current_user.vicinal,
            latitude=current_user.latitude,
            longitude=current_user.longitude,
            produtor_id=current_user.id
        )

        db.session.add(propriedade)
        db.session.commit()

        return propriedade


    return None


# ============================================================
# CADASTRO DE USUÁRIO / PRODUTOR
# ============================================================

@auth.route(
    "/cadastro",
    methods=["GET", "POST"]
)
def cadastro():

    form = CadastroForm()

    if form.validate_on_submit():

        # ----------------------------------------------------
        # Verifica e-mail existente
        # ----------------------------------------------------

        usuario_existente = (
            Usuario.query
            .filter_by(
                email=form.email.data
            )
            .first()
        )

        if usuario_existente:

            flash(
                "Já existe um usuário com esse e-mail.",
                "danger"
            )

            return redirect(
                url_for("auth.cadastro")
            )


        # ----------------------------------------------------
        # Cria hash da senha
        # ----------------------------------------------------

        senha_hash = (
            bcrypt
            .generate_password_hash(
                form.senha.data
            )
            .decode("utf-8")
        )


        # ----------------------------------------------------
        # Cria usuário
        # ----------------------------------------------------

        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=senha_hash,
            tipo=form.tipo.data
        )

        db.session.add(usuario)

        db.session.flush()


        # ----------------------------------------------------
        # Cria primeira propriedade
        # ----------------------------------------------------

        if form.propriedade.data:

            propriedade = Propriedade(

                nome=form.propriedade.data,

                municipio=form.municipio.data,

                vicinal=form.vicinal.data,

                latitude=form.latitude.data,

                longitude=form.longitude.data,

                produtor_id=usuario.id

            )

            db.session.add(propriedade)


        # ----------------------------------------------------
        # Salva tudo
        # ----------------------------------------------------

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

@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    form = LoginForm()

    if form.validate_on_submit():

        usuario = (
            Usuario.query
            .filter_by(
                email=form.email.data
            )
            .first()
        )


        if not usuario:

            flash(
                "E-mail ou senha incorretos.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )


        senha_correta = (
            bcrypt.check_password_hash(
                usuario.senha_hash,
                form.senha.data
            )
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
# MINHAS PROPRIEDADES
# ============================================================

@auth.route("/propriedade")
@login_required
def minha_propriedade():

    # --------------------------------------------------------
    # Garante que dados antigos sejam convertidos para
    # a nova estrutura quando necessário.
    # --------------------------------------------------------

    obter_propriedade_principal()


    # --------------------------------------------------------
    # Busca TODAS as propriedades do produtor
    # --------------------------------------------------------

    propriedades = (
        Propriedade.query
        .filter_by(
            produtor_id=current_user.id
        )
        .order_by(
            Propriedade.nome
        )
        .all()
    )


    return render_template(
        "minha_propriedade.html",
        usuario=current_user,
        propriedades=propriedades
    )


# ============================================================
# NOVA PROPRIEDADE
# ============================================================

@auth.route(
    "/propriedade/nova",
    methods=["GET", "POST"]
)
@login_required
def nova_propriedade():

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    if request.method == "GET":

        propriedade = Propriedade(
            nome="",
            produtor_id=current_user.id
        )

        return render_template(
            "editar_propriedade.html",
            usuario=current_user,
            propriedade=propriedade,
            nova_propriedade=True
        )


    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    nome = (
        request.form.get(
            "propriedade",
            ""
        )
        .strip()
    )

    municipio = (
        request.form.get(
            "municipio",
            ""
        )
        .strip()
    )

    vicinal = (
        request.form.get(
            "vicinal",
            ""
        )
        .strip()
    )


    # --------------------------------------------------------
    # Validação do nome
    # --------------------------------------------------------

    if not nome:

        flash(
            "Informe o nome da propriedade.",
            "warning"
        )

        propriedade = Propriedade(
            nome="",
            produtor_id=current_user.id
        )

        propriedade.municipio = municipio
        propriedade.vicinal = vicinal


        return render_template(
            "editar_propriedade.html",
            usuario=current_user,
            propriedade=propriedade,
            nova_propriedade=True
        )


    # --------------------------------------------------------
    # Cria a propriedade
    # --------------------------------------------------------

    propriedade = Propriedade(

        nome=nome,

        municipio=municipio or None,

        vicinal=vicinal or None,

        produtor_id=current_user.id

    )


    db.session.add(propriedade)

    db.session.commit()


    flash(
        "Nova propriedade cadastrada com sucesso!",
        "success"
    )


    return redirect(
        url_for(
            "auth.minha_propriedade"
        )
    )


# ============================================================
# EDITAR PROPRIEDADE
# ============================================================

@auth.route(
    "/propriedade/<int:propriedade_id>/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_propriedade(propriedade_id):

    # --------------------------------------------------------
    # Buscar propriedade garantindo que pertence ao usuário
    # --------------------------------------------------------

    propriedade = (
        Propriedade.query
        .filter_by(
            id=propriedade_id,
            produtor_id=current_user.id
        )
        .first_or_404()
    )


    # --------------------------------------------------------
    # SALVAR ALTERAÇÕES
    # --------------------------------------------------------

    if request.method == "POST":

        nome = (
            request.form.get(
                "propriedade",
                ""
            )
            .strip()
        )

        municipio = (
            request.form.get(
                "municipio",
                ""
            )
            .strip()
        )

        vicinal = (
            request.form.get(
                "vicinal",
                ""
            )
            .strip()
        )


        # ----------------------------------------------------
        # Validação
        # ----------------------------------------------------

        if not nome:

            flash(
                "O nome da propriedade é obrigatório.",
                "warning"
            )

            return render_template(
                "editar_propriedade.html",
                usuario=current_user,
                propriedade=propriedade,
                nova_propriedade=False
            )


        # ----------------------------------------------------
        # Atualiza
        # ----------------------------------------------------

        propriedade.nome = nome

        propriedade.municipio = municipio or None

        propriedade.vicinal = vicinal or None


        db.session.commit()


        flash(
            "Dados da propriedade atualizados com sucesso!",
            "success"
        )


        return redirect(
            url_for(
                "auth.minha_propriedade"
            )
        )


    # --------------------------------------------------------
    # EXIBIR FORMULÁRIO
    # --------------------------------------------------------

    return render_template(
        "editar_propriedade.html",
        usuario=current_user,
        propriedade=propriedade,
        nova_propriedade=False
    )


# ============================================================
# COMPATIBILIDADE COM ROTA ANTIGA
# ============================================================
#
# Mantemos esta rota porque o restante do sistema ainda pode
# chamar auth.editar_propriedade sem propriedade_id.
#
# Se existir uma propriedade, abrimos a primeira.
# Se não existir, levamos o produtor para criar uma nova.
# ============================================================

@auth.route(
    "/propriedade/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_propriedade_compatibilidade():

    propriedade = obter_propriedade_principal()


    if propriedade:

        return redirect(
            url_for(
                "auth.editar_propriedade",
                propriedade_id=propriedade.id
            )
        )


    return redirect(
        url_for(
            "auth.nova_propriedade"
        )
    )


# ============================================================
# ATUALIZAR LOCALIZAÇÃO
# ============================================================

@auth.route(
    "/propriedade/<int:propriedade_id>/localizacao",
    methods=["GET", "POST"]
)
@login_required
def atualizar_localizacao(propriedade_id):

    # --------------------------------------------------------
    # Garantir que a propriedade pertence ao usuário
    # --------------------------------------------------------

    propriedade = (
        Propriedade.query
        .filter_by(
            id=propriedade_id,
            produtor_id=current_user.id
        )
        .first_or_404()
    )


    # --------------------------------------------------------
    # RECEBER LOCALIZAÇÃO
    # --------------------------------------------------------

    if request.method == "POST":

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )


        # ----------------------------------------------------
        # Verifica valores
        # ----------------------------------------------------

        if not latitude or not longitude:

            flash(
                "Não foi possível obter sua localização.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.atualizar_localizacao",
                    propriedade_id=propriedade.id
                )
            )


        # ----------------------------------------------------
        # Converter coordenadas
        # ----------------------------------------------------

        try:

            latitude = float(latitude)

            longitude = float(longitude)


        except (TypeError, ValueError):

            flash(
                "A localização recebida não é válida.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.atualizar_localizacao",
                    propriedade_id=propriedade.id
                )
            )


        # ----------------------------------------------------
        # Salvar
        # ----------------------------------------------------

        propriedade.latitude = latitude

        propriedade.longitude = longitude


        db.session.commit()


        flash(
            "Localização da propriedade atualizada com sucesso!",
            "success"
        )


        return redirect(
            url_for(
                "auth.minha_propriedade"
            )
        )


    # --------------------------------------------------------
    # EXIBIR TELA
    # --------------------------------------------------------

    return render_template(
        "atualizar_localizacao.html",
        usuario=current_user,
        propriedade=propriedade
    )


# ============================================================
# COMPATIBILIDADE COM ROTA ANTIGA DE LOCALIZAÇÃO
# ============================================================
#
# Mantemos /propriedade/localizacao para evitar quebra de
# links antigos durante a transição.
# ============================================================

@auth.route(
    "/propriedade/localizacao",
    methods=["GET", "POST"]
)
@login_required
def atualizar_localizacao_compatibilidade():

    propriedade = obter_propriedade_principal()


    if propriedade:

        return redirect(
            url_for(
                "auth.atualizar_localizacao",
                propriedade_id=propriedade.id
            )
        )


    flash(
        "Cadastre uma propriedade antes de atualizar a localização.",
        "warning"
    )


    return redirect(
        url_for(
            "auth.nova_propriedade"
        )
    )