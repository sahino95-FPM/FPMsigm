from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

config = context.config
fileConfig(config.config_file_name)


# Configure SQLAlchemy URL from Flask app


def get_app_config():
    from app import create_app

    app = create_app()
    return app.config["SQLALCHEMY_DATABASE_URI"]


# target_metadata = db.metadata  # if using models metadata


def run_migrations_offline():
    url = get_app_config()
    context.configure(url=url, literal_binds=True, dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = get_app_config()
    connectable = engine_from_config({"sqlalchemy.url": url}, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
