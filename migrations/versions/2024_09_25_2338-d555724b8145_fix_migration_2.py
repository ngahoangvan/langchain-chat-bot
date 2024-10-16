"""fix migration 2

Revision ID: d555724b8145
Revises: 916db931e6e3
Create Date: 2024-09-25 23:38:42.760851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd555724b8145'
down_revision: Union[str, None] = '916db931e6e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('labels', sa.Column('restaurant_id', sa.Integer(), nullable=True), schema='shopee')
    op.create_foreign_key(op.f('labels_restaurant_id_fkey'), 'labels', 'restaurants', ['restaurant_id'], ['id'], source_schema='shopee', referent_schema='shopee')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('labels_restaurant_id_fkey'), 'labels', schema='shopee', type_='foreignkey')
    op.drop_column('labels', 'restaurant_id', schema='shopee')
    # ### end Alembic commands ###
