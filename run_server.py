import uvicorn

from app.config import sttgs
from app.db.db_manager import create_all_tables, drop_all_tables
from app.db.utils import populate_tables_mock_data


if __name__ == '__main__':

    # Initialize database
    create_all_tables()
    populate_tables_mock_data(populate=True)

    # Run server
    uvicorn.run(
        "app:app",
        host=sttgs.get('BACKEND_HOST', 'localhost'),
        port=int(sttgs.get('BACKEND_PORT', 8080)),
        reload=True,
        debug=True,
        workers=int(sttgs.get('SERVER_WORKERS', 1))
    )

    # Optionally delete tables after server is shut down
    drop_all_tables(drop=True)
