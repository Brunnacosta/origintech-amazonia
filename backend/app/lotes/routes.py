from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Lote
from app.lotes.forms import LoteForm


lotes = Blueprint("lotes", __name__)


@lotes.route("/lotes")
@login_required
def meus_lotes():

    lotes_usuario = Lote.query.filter_by(
        produtor_id=current_user.id
    ).all()

    return render_template(
        "meus_lotes.html",
        lotes=lotes_usuario
    )

@lotes.route("/lotes/novo", methods=["GET", "POST"])
@login_required
def novo_lote():

    form = LoteForm()

    if form.validate_on_submit():

        lote = Lote(
            codigo=form.codigo.data,
            nome=form.nome.data,
            data_colheita=form.data_colheita.data,
            quantidade_kg=form.quantidade_kg.data,
            fermentacao=form.fermentacao.data,
            secagem=form.secagem.data,
            umidade=form.umidade.data,
            sistema_producao=form.sistema_producao.data,
            produtor_id=current_user.id
        )

        db.session.add(lote)
        db.session.commit()

        flash(
            "Lote cadastrado com sucesso!",
            "success"
        )

        return redirect(url_for("lotes.novo_lote"))

    return render_template(
        "lote_form.html",
        form=form
    )

@lotes.route("/lotes/<int:lote_id>")
@login_required
def detalhes_lote(lote_id):

    lote = Lote.query.filter_by(
        id=lote_id,
        produtor_id=current_user.id
    ).first_or_404()

    return render_template(
        "detalhes_lote.html",
        lote=lote
    )

@lotes.route("/lotes/<int:lote_id>/editar", methods=["GET", "POST"])
@login_required
def editar_lote(lote_id):

    lote = Lote.query.filter_by(
        id=lote_id,
        produtor_id=current_user.id
    ).first_or_404()

    form = LoteForm(obj=lote)

    if form.validate_on_submit():

        lote.codigo = form.codigo.data
        lote.nome = form.nome.data
        lote.data_colheita = form.data_colheita.data
        lote.quantidade_kg = form.quantidade_kg.data
        lote.fermentacao = form.fermentacao.data
        lote.secagem = form.secagem.data
        lote.umidade = form.umidade.data
        lote.sistema_producao = form.sistema_producao.data

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

    return render_template(
        "lote_form.html",
        form=form
    )

@lotes.route("/lotes/<int:lote_id>/excluir", methods=["POST"])
@login_required
def excluir_lote(lote_id):

    lote = Lote.query.filter_by(
        id=lote_id,
        produtor_id=current_user.id
    ).first_or_404()

    db.session.delete(lote)
    db.session.commit()

    flash(
        "Lote excluído com sucesso!",
        "success"
    )

    return redirect(url_for("lotes.meus_lotes"))