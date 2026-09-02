from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)


main = Blueprint("main", __name__)


# ============================================================
# PÁGINA INICIAL PÚBLICA
# ============================================================

@main.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# CONSULTAR LOTE
# ============================================================

@main.route(
    "/consultar-lote",
    methods=["GET", "POST"]
)
def consultar_lote():

    if request.method == "POST":

        codigo = request.form.get(
            "codigo",
            ""
        ).strip()

        if codigo:

            return redirect(
                url_for(
                    "lotes.lote_publico",
                    codigo=codigo
                )
            )

    return render_template(
        "consulta_lote.html"
    )