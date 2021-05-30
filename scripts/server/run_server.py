"""Uvicorn server initialization script.

Run ``python run_server.py --help`` to see the options.
"""
import os
from typer import Typer, Option


cli_app = Typer()


run_uvicorn_server_help = (
    "Run the FastAPI "
)
local_help = (
    "Run the uvicorn server using $POSTGRES_LOCAL_URI set in ~/.env"
)
populate_tables_help = (
    "Fill the <dog> and <user> PostgreSQL tables with mock data stored inside "
    "``mock_data.db_test_data`` module."
)
drop_tables_help = (
    "After the server is shut down, drop all tables inside PostgreSQL "
    "database."
)


@cli_app.command()
def run_uvicorn_server(
    local_db: bool = Option(False, help=local_help),
    populate_tables: bool = Option(False, help=populate_tables_help),
    drop_tables: bool = Option(False, help=drop_tables_help)
) -> None:
    """Run the FastAPI app using the uvicorn server, optionally setting
    up some db test data beforehand, and deleting it after the server is
    shut down.
    """
    from app.config import sttgs

    if local_db:
        os.environ["POSTGRES_URI"] = sttgs.get("POSTGRES_LOCAL_URI")

    # This dependencies need to be imported here so that the sqlAlchemy engine
    # is created with the correct uri (previously modified by local_db
    # oprtion). If they are imported at the beggining of the script, the
    # dependencies inside the import statements will make the server to be run
    # with the using the wrong URI
    import uvicorn

    from app.db.db_manager import create_all_tables, drop_all_tables
    from app.db.utils import populate_tables_mock_data

    if populate_tables:
        # Initialize database
        create_all_tables()
        populate_tables_mock_data(populate=True)

    # Run server
    uvicorn.run(
        "app.main:app",
        host=sttgs.get('BACKEND_HOST', 'localhost'),
        port=int(sttgs.get('BACKEND_PORT', 8080)),
        reload=True,
        debug=True,
        workers=int(sttgs.get('SERVER_WORKERS', 1))
    )

    drop_all_tables(drop=drop_tables)


if __name__ == '__main__':
    cli_app()
