import io

import qrcode

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    request,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.models import (
    Lote,
    Propriedade
)

from app.lotes.forms import LoteForm


lotes = Blueprint("lotes", __name__)


# ============================================================
# MEUS LOTES
# ============================================================

@lotes.route("/lotes")
@login_required
def meus_lotes():

    lotes_usuario = (
        Lote.query
        .join(Propriedade)
        .filter(
            Propriedade.produtor_id == current_user.id
        )
        .order_by(Lote.id.desc())
        .all()
    )

    return render_template(
        "meus_lotes.html",
        lotes=lotes_usuario
    )


# ============================================================
# CADASTRAR LOTE
# ============================================================

@lotes.route(
    "/lotes/novo",
    methods=["GET", "POST"]
)
@login_required
def novo_lote():

    form = LoteForm()

    # --------------------------------------------------------
    # Buscar propriedades do produtor logado
    # --------------------------------------------------------

    propriedades = (
        Propriedade.query
        .filter_by(
            produtor_id=current_user.id
        )
        .order_by(Propriedade.nome)
        .all()
    )

    # --------------------------------------------------------
    # Se o produtor ainda não possui propriedade
    # --------------------------------------------------------

    if not propriedades:

        flash(
            "Cadastre uma propriedade antes de registrar um lote.",
            "warning"
        )

        return redirect(
            url_for("auth.editar_propriedade")
        )

    # --------------------------------------------------------
    # Cadastro do lote
    # --------------------------------------------------------

    if form.validate_on_submit():

        # ----------------------------------------------------
        # A propriedade vem do formulário HTML
        # ----------------------------------------------------

        propriedade_id = request.form.get("propriedade_id")

        if not propriedade_id:

            flash(
                "Selecione uma propriedade para o lote.",
                "warning"
            )

            return render_template(
                "lote_form.html",
                form=form,
                usuario=current_user,
                propriedades=propriedades,
                propriedade_selecionada=None
            )

        # ----------------------------------------------------
        # Validar ID da propriedade
        # ----------------------------------------------------

        try:

            propriedade_id = int(propriedade_id)

        except (TypeError, ValueError):

            flash(
                "A propriedade selecionada é inválida.",
                "danger"
            )

            return render_template(
                "lote_form.html",
                form=form,
                usuario=current_user,
                propriedades=propriedades,
                propriedade_selecionada=None
            )

        # ----------------------------------------------------
        # Garantir que a propriedade pertence ao usuário
        # ----------------------------------------------------

        propriedade = (
            Propriedade.query
            .filter_by(
                id=propriedade_id,
                produtor_id=current_user.id
            )
            .first()
        )

        if not propriedade:

            flash(
                "A propriedade selecionada não pertence ao seu cadastro.",
                "danger"
            )

            return render_template(
                "lote_form.html",
                form=form,
                usuario=current_user,
                propriedades=propriedades,
                propriedade_selecionada=None
            )

        # ----------------------------------------------------
        # Criar o lote
        # ----------------------------------------------------

        lote = Lote(

            # Identificação
            codigo=form.codigo.data,

            # Colheita
            data_colheita=form.data_colheita.data,

            quantidade_kg=form.quantidade_kg.data,

            # Beneficiamento
            fermentacao=form.fermentacao.data,

            secagem=form.secagem.data,

            # Informações
            umidade=form.umidade.data,

            sistema_producao=form.sistema_producao.data,

            # Relacionamento com a propriedade
            propriedade_id=propriedade.id
        )

        db.session.add(lote)

        db.session.commit()

        flash(
            "Lote cadastrado com sucesso!",
            "success"
        )

        return redirect(
            url_for("lotes.meus_lotes")
        )

    # --------------------------------------------------------
    # Exibir formulário
    # --------------------------------------------------------

    return render_template(
        "lote_form.html",
        form=form,
        usuario=current_user,
        propriedades=propriedades,
        propriedade_selecionada=None
    )


# ============================================================
# DETALHES DO LOTE
# ============================================================

@lotes.route("/lotes/<int:lote_id>")
@login_required
def detalhes_lote(lote_id):

    lote = (
        Lote.query
        .join(Propriedade)
        .filter(
            Lote.id == lote_id,
            Propriedade.produtor_id == current_user.id
        )
        .first_or_404()
    )

    return render_template(
        "detalhes_lote.html",
        lote=lote
    )


# ============================================================
# EDITAR LOTE
# ============================================================

@lotes.route(
    "/lotes/<int:lote_id>/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_lote(lote_id):

    # --------------------------------------------------------
    # Buscar lote garantindo que pertence ao usuário
    # --------------------------------------------------------

    lote = (
        Lote.query
        .join(Propriedade)
        .filter(
            Lote.id == lote_id,
            Propriedade.produtor_id == current_user.id
        )
        .first_or_404()
    )

    form = LoteForm(obj=lote)

    # --------------------------------------------------------
    # Buscar propriedades do produtor
    # --------------------------------------------------------

    propriedades = (
        Propriedade.query
        .filter_by(
            produtor_id=current_user.id
        )
        .order_by(Propriedade.nome)
        .all()
    )

    # --------------------------------------------------------
    # Atualizar lote
    # --------------------------------------------------------

    if form.validate_on_submit():

        propriedade_id = request.form.get("propriedade_id")

        if not propriedade_id:

            flash(
                "Selecione uma propriedade para o lote.",
                "warning"
            )

            return render_template(
                "lote_form.html",
                form=form,
                usuario=current_user,
                propriedades=propriedades,
                lote=lote,
                propriedade_selecionada=lote.propriedade_id
            )

        # ----------------------------------------------------
        # Validar ID
        # ----------------------------------------------------

        try:

            propriedade_id = int(propriedade_id)

        except (TypeError, ValueError):

            flash(
                "A propriedade selecionada é inválida.",
                "danger"
            )

            return render_template(
                "lote_form.html",
                form=form,
                usuario=current_user,
                propriedades=propriedades,
                lote=lote,
                propriedade_selecionada=lote.propriedade_id
            )

        # ----------------------------------------------------
        # Garantir que a propriedade pertence ao usuário
        # ----------------------------------------------------

        propriedade = (
            Propriedade.query
            .filter_by(
                id=propriedade_id,
                produtor_id=current_user.id
            )
            .first()
        )

        if not propriedade:

            flash(
                "A propriedade selecionada não pertence ao seu cadastro.",
                "danger"
            )

            return render_template(
                "lote_form.html",
                form=form,
                usuario=current_user,
                propriedades=propriedades,
                lote=lote,
                propriedade_selecionada=lote.propriedade_id
            )

        # ----------------------------------------------------
        # Atualizar os dados
        # ----------------------------------------------------

        lote.codigo = form.codigo.data

        lote.data_colheita = form.data_colheita.data

        lote.quantidade_kg = form.quantidade_kg.data

        lote.fermentacao = form.fermentacao.data

        lote.secagem = form.secagem.data

        lote.umidade = form.umidade.data

        lote.sistema_producao = form.sistema_producao.data

        # ----------------------------------------------------
        # Atualizar propriedade
        # ----------------------------------------------------

        lote.propriedade_id = propriedade.id

        db.session.commit()

        flash(
            "Lote atualizado com sucesso!",
            "success"
        )

        return redirect(
            url_for(
                "lotes.detalhes_lote",
                lote_id=lote.id
            )
        )

    # --------------------------------------------------------
    # Exibir formulário
    # --------------------------------------------------------

    return render_template(
        "lote_form.html",
        form=form,
        usuario=current_user,
        propriedades=propriedades,
        lote=lote,
        propriedade_selecionada=lote.propriedade_id
    )


# ============================================================
# EXCLUIR LOTE
# ============================================================

@lotes.route(
    "/lotes/<int:lote_id>/excluir",
    methods=["POST"]
)
@login_required
def excluir_lote(lote_id):

    lote = (
        Lote.query
        .join(Propriedade)
        .filter(
            Lote.id == lote_id,
            Propriedade.produtor_id == current_user.id
        )
        .first_or_404()
    )

    db.session.delete(lote)

    db.session.commit()

    flash(
        "Lote excluído com sucesso!",
        "success"
    )

    return redirect(
        url_for("lotes.meus_lotes")
    )


# ============================================================
# TELA DO QR CODE
# ============================================================

@lotes.route(
    "/lotes/<int:lote_id>/qrcode"
)
@login_required
def qrcode_lote(lote_id):

    lote = (
        Lote.query
        .join(Propriedade)
        .filter(
            Lote.id == lote_id,
            Propriedade.produtor_id == current_user.id
        )
        .first_or_404()
    )

    return render_template(
        "qrcode.html",
        lote=lote
    )


# ============================================================
# IMAGEM DO QR CODE
# ============================================================

@lotes.route(
    "/lotes/<int:lote_id>/qrcode/imagem"
)
@login_required
def imagem_qrcode(lote_id):

    lote = (
        Lote.query
        .join(Propriedade)
        .filter(
            Lote.id == lote_id,
            Propriedade.produtor_id == current_user.id
        )
        .first_or_404()
    )

    url_publica = (
        f"{current_app.config['BASE_URL']}"
        f"{url_for('lotes.lote_publico', codigo=lote.codigo)}"
    )

    imagem = qrcode.make(url_publica)

    arquivo = io.BytesIO()

    imagem.save(
        arquivo,
        format="PNG"
    )

    arquivo.seek(0)

    return send_file(
        arquivo,
        mimetype="image/png"
    )


# ============================================================
# BAIXAR QR CODE
# ============================================================

@lotes.route(
    "/lotes/<int:lote_id>/qrcode/download"
)
@login_required
def baixar_qrcode(lote_id):

    lote = (
        Lote.query
        .join(Propriedade)
        .filter(
            Lote.id == lote_id,
            Propriedade.produtor_id == current_user.id
        )
        .first_or_404()
    )

    url_publica = (
        f"{current_app.config['BASE_URL']}"
        f"{url_for('lotes.lote_publico', codigo=lote.codigo)}"
    )

    imagem = qrcode.make(url_publica)

    arquivo = io.BytesIO()

    imagem.save(
        arquivo,
        format="PNG"
    )

    arquivo.seek(0)

    return send_file(
        arquivo,
        mimetype="image/png",
        as_attachment=True,
        download_name=f"qrcode-{lote.codigo}.png"
    )


# ============================================================
# PÁGINA PÚBLICA DO LOTE
# ============================================================

@lotes.route("/lote/<codigo>")
def lote_publico(codigo):

    lote = (
        Lote.query
        .filter_by(
            codigo=codigo
        )
        .first()
    )

    if not lote:

        return render_template(
            "lote_nao_encontrado.html",
            codigo=codigo
        ), 404

    return render_template(
        "lote_publico.html",
        lote=lote
    )