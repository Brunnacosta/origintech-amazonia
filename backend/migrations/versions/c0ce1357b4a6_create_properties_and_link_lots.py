"""create properties and link lots

Revision ID: c0ce1357b4a6
Revises: 3356a372d0c5
Create Date: 2026-09-04 18:01:00.049783

"""

from alembic import op
import sqlalchemy as sa


# ============================================================
# IDENTIFICAÇÃO DA MIGRATION
# ============================================================

revision = "c0ce1357b4a6"
down_revision = "3356a372d0c5"
branch_labels = None
depends_on = None


# ============================================================
# UPGRADE
# ============================================================

def upgrade():

    # ========================================================
    # 1. CRIAR TABELA DE PROPRIEDADES
    # ========================================================

    op.create_table(
        "propriedades",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "nome",
            sa.String(length=150),
            nullable=False
        ),

        sa.Column(
            "municipio",
            sa.String(length=100),
            nullable=True
        ),

        sa.Column(
            "vicinal",
            sa.String(length=150),
            nullable=True
        ),

        sa.Column(
            "latitude",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "longitude",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "produtor_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "criado_em",
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ["produtor_id"],
            ["usuarios.id"]
        )
    )


    # ========================================================
    # 2. CRIAR COLUNA PROPRIEDADE_ID EM LOTES
    # ========================================================

    with op.batch_alter_table(
        "lotes",
        schema=None
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "propriedade_id",
                sa.Integer(),
                nullable=True
            )
        )


    # ========================================================
    # 3. COPIAR OS DADOS ANTIGOS DE USUARIO
    #    PARA PROPRIEDADES
    # ========================================================

    connection = op.get_bind()

    usuarios = sa.table(
        "usuarios",

        sa.column(
            "id",
            sa.Integer()
        ),

        sa.column(
            "propriedade",
            sa.String()
        ),

        sa.column(
            "municipio",
            sa.String()
        ),

        sa.column(
            "vicinal",
            sa.String()
        ),

        sa.column(
            "latitude",
            sa.Float()
        ),

        sa.column(
            "longitude",
            sa.Float()
        )
    )


    propriedades = sa.table(
        "propriedades",

        sa.column(
            "id",
            sa.Integer()
        ),

        sa.column(
            "nome",
            sa.String()
        ),

        sa.column(
            "municipio",
            sa.String()
        ),

        sa.column(
            "vicinal",
            sa.String()
        ),

        sa.column(
            "latitude",
            sa.Float()
        ),

        sa.column(
            "longitude",
            sa.Float()
        ),

        sa.column(
            "produtor_id",
            sa.Integer()
        )
    )


    # ========================================================
    # BUSCAR USUÁRIOS COM PROPRIEDADE
    # ========================================================

    resultado = connection.execute(
        sa.select(
            usuarios.c.id,
            usuarios.c.propriedade,
            usuarios.c.municipio,
            usuarios.c.vicinal,
            usuarios.c.latitude,
            usuarios.c.longitude
        )
        .where(
            usuarios.c.propriedade.isnot(None)
        )
    )


    # ========================================================
    # CRIAR UMA PROPRIEDADE PARA CADA USUARIO EXISTENTE
    # ========================================================

    for usuario in resultado:

        connection.execute(
            propriedades.insert().values(

                nome=usuario.propriedade,

                municipio=usuario.municipio,

                vicinal=usuario.vicinal,

                latitude=usuario.latitude,

                longitude=usuario.longitude,

                produtor_id=usuario.id
            )
        )


    # ========================================================
    # 4. RELACIONAR OS LOTES EXISTENTES
    # ========================================================

    connection.execute(
        sa.text(
            """
            UPDATE lotes
            SET propriedade_id = propriedades.id
            FROM propriedades
            WHERE lotes.produtor_id = propriedades.produtor_id
            """
        )
    )


    # ========================================================
    # 5. CRIAR NOVA FOREIGN KEY
    # ========================================================

    with op.batch_alter_table(
        "lotes",
        schema=None
    ) as batch_op:

        batch_op.drop_constraint(
            "lotes_produtor_id_fkey",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "lotes_propriedade_id_fkey",
            "propriedades",
            ["propriedade_id"],
            ["id"]
        )


    # ========================================================
    # 6. REMOVER O CAMPO ANTIGO PRODUTOR_ID
    # ========================================================

    with op.batch_alter_table(
        "lotes",
        schema=None
    ) as batch_op:

        batch_op.drop_column(
            "produtor_id"
        )


# ============================================================
# DOWNGRADE
# ============================================================

def downgrade():

    # ========================================================
    # 1. RECRIAR PRODUTOR_ID EM LOTES
    # ========================================================

    with op.batch_alter_table(
        "lotes",
        schema=None
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "produtor_id",
                sa.Integer(),
                nullable=True
            )
        )


    # ========================================================
    # 2. RECUPERAR PRODUTOR_ID
    # ========================================================

    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE lotes
            SET produtor_id = propriedades.produtor_id
            FROM propriedades
            WHERE lotes.propriedade_id = propriedades.id
            """
        )
    )


    # ========================================================
    # 3. TORNAR PRODUTOR_ID OBRIGATÓRIO
    # ========================================================

    with op.batch_alter_table(
        "lotes",
        schema=None
    ) as batch_op:

        batch_op.alter_column(
            "produtor_id",
            existing_type=sa.Integer(),
            nullable=False
        )

        batch_op.drop_constraint(
            "lotes_propriedade_id_fkey",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "lotes_produtor_id_fkey",
            "usuarios",
            ["produtor_id"],
            ["id"]
        )

        batch_op.drop_column(
            "propriedade_id"
        )


    # ========================================================
    # 4. REMOVER TABELA DE PROPRIEDADES
    # ========================================================

    op.drop_table(
        "propriedades"
    )