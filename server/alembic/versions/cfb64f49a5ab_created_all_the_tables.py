"""created all the tables

Revision ID: cfb64f49a5ab
Revises: 4f2f2a13bcc1
Create Date: 2025-06-23 17:06:06.495778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfb64f49a5ab'
down_revision: Union[str, None] = '4f2f2a13bcc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
