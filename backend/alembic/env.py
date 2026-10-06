from logging.config import fileConfig

from alembic import context
from app.core.config import Settings
from app.core.database import Base, create_database
from app.models import StudentProfile, User  # noqa: F401

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
settings = Settings()

if context.is_offline_mode():
    context.configure(
        url=settings.database_url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=settings.database_url.startswith("sqlite"),
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    engine, _ = create_database(settings)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            render_as_batch=settings.database_url.startswith("sqlite"),
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()
