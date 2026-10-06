"""Account foundation. Only implemented domains are migrated here."""

import sqlalchemy as sa

from alembic import op

revision = "0001_accounts"
down_revision = None
branch_labels = None
depends_on = None


def timestamps():
    return [
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    ]


def upgrade():
    id_type = sa.BigInteger().with_variant(sa.Integer(), "sqlite")
    op.create_table(
        "users",
        sa.Column("id", id_type, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(64), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(16), nullable=False, server_default="student"),
        sa.Column("token_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("is_demo", sa.Boolean(), nullable=False, server_default="1"),
        *timestamps(),
        sa.UniqueConstraint("username", name="uq_users_username"),
        sa.CheckConstraint("role IN ('student','admin')", name="role"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_table(
        "student_profiles",
        sa.Column("id", id_type, primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("nickname", sa.String(64), nullable=False),
        sa.Column("education", sa.String(16)),
        sa.Column("target_category", sa.String(16)),
        sa.Column("preferred_cities_json", sa.JSON(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        *timestamps(),
        sa.UniqueConstraint("user_id", name="uq_student_profiles_user_id"),
        sa.CheckConstraint(
            "education IS NULL OR education IN ('college','bachelor','master')", name="education"
        ),
        sa.CheckConstraint(
            "target_category IS NULL OR target_category IN ('python','frontend','data')",
            name="target_category",
        ),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )


def downgrade():
    op.drop_table("student_profiles")
    op.drop_table("users")
