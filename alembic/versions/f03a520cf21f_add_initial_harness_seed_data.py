"""Add initial harness seed data

Revision ID: f03a520cf21f
Revises: b6d3963f98ef
Create Date: 2025-11-16 15:05:14.534293

"""

import uuid

import sqlalchemy as sa

from alembic import op

# Define table stubs to prevent needing to import the full models
# which might have dependencies that are not available during migrations.
harnesses_table = sa.table(
    "harnesses", sa.column("id", sa.String), sa.column("name", sa.String)
)

connectors_table = sa.table(
    "connectors",
    sa.column("id", sa.String),
    sa.column("logical_id", sa.String),
    sa.column("manufacturer", sa.String),
    sa.column("part_number", sa.String),
    sa.column("harness_id", sa.String),
)

pins_table = sa.table(
    "pins",
    sa.column("id", sa.String),
    sa.column("logical_id", sa.String),
    sa.column("connector_id", sa.String),
)


# revision identifiers, used by Alembic.
revision = "f03a520cf21f"
down_revision = "b6d3963f98ef"
branch_labels = None
depends_on = None


def upgrade():
    """
    Seed the database with initial data for E2E testing.
    Creates one harness with two connectors.
    """
    harness_id = "0a9eb930-c504-4835-a281-3e5c1800e1d1"
    conn1_id = str(uuid.uuid4())
    conn2_id = str(uuid.uuid4())

    # Seed Harness
    op.bulk_insert(
        harnesses_table,
        [
            {"id": harness_id, "name": "E2E Test Harness"},
        ],
    )

    # Seed Connectors
    op.bulk_insert(
        connectors_table,
        [
            {
                "id": conn1_id,
                "logical_id": "CONN1",
                "manufacturer": "JST",
                "part_number": "XH-2P",
                "harness_id": harness_id,
            },
            {
                "id": conn2_id,
                "logical_id": "CONN2",
                "manufacturer": "JST",
                "part_number": "XH-2P",
                "harness_id": harness_id,
            },
        ],
    )

    # Seed Pins
    op.bulk_insert(
        pins_table,
        [
            {"id": str(uuid.uuid4()), "logical_id": "1", "connector_id": conn1_id},
            {"id": str(uuid.uuid4()), "logical_id": "2", "connector_id": conn1_id},
            {"id": str(uuid.uuid4()), "logical_id": "1", "connector_id": conn2_id},
            {"id": str(uuid.uuid4()), "logical_id": "2", "connector_id": conn2_id},
        ],
    )


def downgrade():
    """
    Remove the seeded E2E test data.
    """
    harness_id = "0a9eb930-c504-4835-a281-3e5c1800e1d1"

    # The connection object is not available in downgrade, so we use raw SQL.
    # The order of deletion is important to avoid foreign key violations.
    op.execute(
        f"DELETE FROM pins WHERE connector_id IN "
        f"(SELECT id FROM connectors WHERE harness_id = '{harness_id}')"
    )
    op.execute(f"DELETE FROM connectors WHERE harness_id = '{harness_id}'")
    op.execute(f"DELETE FROM harnesses WHERE id = '{harness_id}'")
