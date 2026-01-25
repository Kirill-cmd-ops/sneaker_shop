"""Renaming table from Countries to Countries

Revision ID: e04404f59385
Revises: 116fcd2ecd80
Create Date: 2025-08-25 10:29:20.410415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e04404f59385"
down_revision: Union[str, None] = "116fcd2ecd80"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table('countrys', 'countries')
    # Если нужно, переименуй и внешний ключ, чтобы имя было консистентным
    op.execute(
        "ALTER TABLE sneakers RENAME CONSTRAINT fk_sneakers_country_id_countrys TO fk_sneakers_country_id_countries"
    )

def downgrade():
    op.rename_table('countries', 'countrys')
    op.execute(
        "ALTER TABLE sneakers RENAME CONSTRAINT fk_sneakers_country_id_countries TO fk_sneakers_country_id_countrys"
    )

