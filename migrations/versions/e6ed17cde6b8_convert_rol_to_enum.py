"""convert rol to enum

Revision ID: e6ed17cde6b8
Revises: cd5ae23308a2
Create Date: 2026-04-27 11:50:00.940612

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'e6ed17cde6b8'
down_revision = 'cd5ae23308a2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column(
            'rol',
            existing_type=sa.String(length=20),
            type_=mysql.ENUM('cliente', 'admin'),
            existing_nullable=False,
            existing_server_default=sa.text("'cliente'"),
        )


def downgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column(
            'rol',
            existing_type=mysql.ENUM('cliente', 'admin'),
            type_=sa.String(length=20),
            existing_nullable=False,
            existing_server_default=sa.text("'cliente'"),
        )
