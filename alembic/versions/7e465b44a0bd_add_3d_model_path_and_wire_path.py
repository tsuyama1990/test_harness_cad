"""Add 3D model path and wire path

Revision ID: 7e465b44a0bd
Revises: c1d0890e9fff
Create Date: 2025-11-17 12:06:41.411178

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7e465b44a0bd"
down_revision = "c1d0890e9fff"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("harnesses", schema=None) as batch_op:
        batch_op.add_column(sa.Column("three_d_model_path", sa.String(), nullable=True))

    with op.batch_alter_table("wires", schema=None) as batch_op:
        batch_op.add_column(sa.Column("path_3d", sa.JSON(), nullable=True))


def downgrade():
    with op.batch_alter_table("wires", schema=None) as batch_op:
        batch_op.drop_column("path_3d")

    with op.batch_alter_table("harnesses", schema=None) as batch_op:
        batch_op.drop_column("three_d_model_path")
