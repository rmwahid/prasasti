"""Initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-07-28
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    op.create_table(
        'persons',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('alias', sa.String(255), nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'cases',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('person_id', sa.UUID(as_uuid=True), sa.ForeignKey('persons.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('source_url', sa.String(1000), nullable=True),
        sa.Column('case_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'embeddings',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('person_id', sa.UUID(as_uuid=True), sa.ForeignKey('persons.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('vector', Vector(512), nullable=False),
        sa.Column('source_photo_url', sa.String(500), nullable=True),
        sa.Column('model_version', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # HNSW index for cosine similarity search
    op.execute('CREATE INDEX idx_embeddings_vector_hnsw ON embeddings USING hnsw (vector vector_cosine_ops)')

    op.create_table(
        'search_history',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('device_id', sa.String(255), nullable=True, index=True),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('top_match_person_id', sa.UUID(as_uuid=True), sa.ForeignKey('persons.id', ondelete='SET NULL'), nullable=True),
        sa.Column('top_match_score', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('search_history')
    op.execute('DROP INDEX IF EXISTS idx_embeddings_vector_hnsw')
    op.drop_table('embeddings')
    op.drop_table('cases')
    op.drop_table('persons')
    op.execute('DROP EXTENSION IF EXISTS vector')
