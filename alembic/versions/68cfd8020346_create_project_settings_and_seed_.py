"""Create project_settings and seed harness_designs

Revision ID: 68cfd8020346
Revises: 4483e00d5df0
Create Date: 2025-11-18 14:12:22.123456

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '68cfd8020346'
down_revision = '4483e00d5df0'
branch_labels = None
depends_on = None

harness_designs_table = sa.table(
    "harness_designs",
    sa.column("id", sa.Integer),
    sa.column("project_id", sa.Integer),
    sa.column("harness_id", sa.String),
    sa.column("design_data", sa.JSON),
    sa.column("created_at", sa.DateTime),
)

projects_table = sa.table(
    "projects",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
)

def upgrade():
    op.create_table('project_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('system_voltage', sa.Float(), nullable=True),
    sa.Column('require_rohs', sa.Boolean(), nullable=False),
    sa.Column('require_ul', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_settings_id'), 'project_settings', ['id'], unique=False)

    project_id = 1
    harness_id = "0a9eb930-c504-4835-a281-3e5c1800e1d1"

    op.bulk_insert(
        projects_table,
        [
            {"id": project_id, "name": "Test Project"},
        ],
    )

    op.bulk_insert(
        harness_designs_table,
        [
            {
                "id": 1,
                "project_id": project_id,
                "harness_id": harness_id,
                "design_data": {},
                "created_at": datetime.utcnow(),
            },
        ],
    )


def downgrade():
    op.drop_index(op.f('ix_project_settings_id'), table_name='project_settings')
    op.drop_table('project_settings')
    op.execute("DELETE FROM harness_designs WHERE id = 1")
    op.execute("DELETE FROM projects WHERE id = 1")