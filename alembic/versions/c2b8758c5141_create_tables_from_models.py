"""Create tables from models.

Revision ID: c2b8758c5141
Revises: 
Create Date: 2024-08-31 15:45:12.030800

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c2b8758c5141"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "api_users",
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(
        op.f("ix_api_users_username"), "api_users", ["username"], unique=True
    )
    op.create_table(
        "api_workpatterns",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("interval_month", sa.Integer(), nullable=False),
        sa.Column("interval_km", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "api_vehicles",
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("vin_code", sa.String(length=17), nullable=False),
        sa.Column("vehicle_manufacturer", sa.String(), nullable=False),
        sa.Column("vehicle_model", sa.String(), nullable=False),
        sa.Column("vehicle_body", sa.String(), nullable=False),
        sa.Column("vehicle_year", sa.Integer(), nullable=False),
        sa.Column("vehicle_mileage", sa.Integer(), nullable=False),
        sa.Column("vehicle_last_update_date", sa.Date(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["api_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_api_vehicles_vin_code"), "api_vehicles", ["vin_code"], unique=True
    )
    op.create_table(
        "api_mileageevents",
        sa.Column("mileage_date", sa.Date(), nullable=False),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["vehicle_id"], ["api_vehicles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "api_works",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("interval_month", sa.Integer(), nullable=False),
        sa.Column("interval_km", sa.Integer(), nullable=False),
        sa.Column("work_type", sa.Integer(), nullable=False),
        sa.Column("note", sa.String(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["vehicle_id"], ["api_vehicles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "api_events",
        sa.Column("work_date", sa.Date(), nullable=False),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("work_id", sa.Integer(), nullable=False),
        sa.Column("part_price", sa.Float(), nullable=False),
        sa.Column("work_price", sa.Float(), nullable=False),
        sa.Column("note", sa.String(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["vehicle_id"], ["api_vehicles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["work_id"], ["api_works.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("api_events")
    op.drop_table("api_works")
    op.drop_table("api_mileageevents")
    op.drop_index(op.f("ix_api_vehicles_vin_code"), table_name="api_vehicles")
    op.drop_table("api_vehicles")
    op.drop_table("api_workpatterns")
    op.drop_index(op.f("ix_api_users_username"), table_name="api_users")
    op.drop_table("api_users")
    # ### end Alembic commands ###
