"""Add technical specifications to connectors and wires

Revision ID: 4483e00d5df0
Revises: 7e465b44a0bd
Create Date: 2025-11-18 13:21:52.853494

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4483e00d5df0"
down_revision = "7e465b44a0bd"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("connectors", schema=None) as batch_op:
        batch_op.add_column(sa.Column("voltage_rating", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("applicable_wire_max_diameter", sa.Float(), nullable=True)
        )
        batch_op.add_column(sa.Column("is_rohs", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("is_ul", sa.Boolean(), nullable=True))

    with op.batch_alter_table("wires", schema=None) as batch_op:
        batch_op.add_column(sa.Column("voltage_rating", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("outer_diameter", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("is_rohs", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("is_ul", sa.Boolean(), nullable=True))


def downgrade():
    with op.batch_alter_table("wires", schema=None) as batch_op:
        batch_op.drop_column("is_ul")
        batch_op.drop_column("is_rohs")
        batch_op.drop_column("outer_diameter")
        batch_op.drop_column("voltage_rating")

    with op.batch_alter_table("connectors", schema=None) as batch_op:
        batch_op.drop_column("is_ul")
        batch_op.drop_column("is_rohs")
        batch_op.drop_column("applicable_wire_max_diameter")
        batch_op.drop_column("voltage_rating")
