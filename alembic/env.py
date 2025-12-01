import asyncio
import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importe sua Base aqui para o autogenerate funcionar
from core.infra.orm.base import Base

# ----------------------------------------------------------------------
# 1. CARREGAMENTO DE VARIÁVEIS DE AMBIENTE
# ----------------------------------------------------------------------
load_dotenv()

# Recupera a URL. Se estiver rodando via Docker, ele deve pegar do ambiente.
# Se estiver rodando local, ele pega do .env.
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificação de segurança para evitar o erro "NoneType"
if not DATABASE_URL:
    print("\n[ERRO CRÍTICO] A variável DATABASE_URL não foi encontrada.")
    print(
        "Verifique se o arquivo .env existe ou se as variáveis do Docker "
        "estão corretas.\n"
    )
    sys.exit(1)

# O Alembic Config object, que dá acesso aos valores do arquivo .ini
config = context.config

# Interpreta o arquivo de config para log (alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------------------------------------------------
# 2. IMPORTAÇÃO DOS MODELOS (METADATA)
# ----------------------------------------------------------------------

target_metadata = Base.metadata

# ----------------------------------------------------------------------
# 3. FUNÇÕES DE MIGRAÇÃO
# ----------------------------------------------------------------------


def run_migrations_offline() -> None:
    """Roda migrações no modo 'offline'.

    Isso configura o contexto apenas com uma URL, sem criar uma Engine.
    Útil para gerar scripts SQL sem conectar ao banco.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Função auxiliar para rodar as migrações de forma síncrona
    dentro do contexto assíncrono.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Nesta configuração, criamos uma AsyncEngine e associamos
    uma conexão ao contexto.
    """

    # Sobrescreve a URL do alembic.ini com a variável de ambiente real
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # O Alembic core é síncrono, então usamos run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Roda migrações no modo 'online'.

    Como estamos usando asyncpg, precisamos rodar o loop de eventos do asyncio.
    """
    asyncio.run(run_async_migrations())


# ----------------------------------------------------------------------
# 4. EXECUÇÃO PRINCIPAL
# ----------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
