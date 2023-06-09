"""fix data type

Revision ID: 90fd18e9494c
Revises: 27ccbcd90084
Create Date: 2023-05-29 21:08:47.279209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90fd18e9494c'
down_revision = '27ccbcd90084'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tiktok_music', sa.Column('tiktok_id', sa.String(), nullable=False))
    op.drop_constraint('tiktok_music_tiktok_music_id_key', 'tiktok_music', type_='unique')
    op.create_unique_constraint(None, 'tiktok_music', ['tiktok_id'])
    op.drop_column('tiktok_music', 'tiktok_music_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tiktok_music', sa.Column('tiktok_music_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tiktok_music', type_='unique')
    op.create_unique_constraint('tiktok_music_tiktok_music_id_key', 'tiktok_music', ['tiktok_music_id'])
    op.drop_column('tiktok_music', 'tiktok_id')
    # ### end Alembic commands ###
