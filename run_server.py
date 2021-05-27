import uvicorn

from app.config import sttgs
from app.db.init_db import init_db
from app.db.utils import populate_tables_mock_data


if __name__ == '__main__':

    # Initialize database
    init_db()
    populate_tables_mock_data(True)

    # Run server
    uvicorn.run(
        "app:app",
        host=sttgs.get('HOST', 'localhost'),
        port=int(sttgs.get('PORT', 8080)),
        reload=True,
        debug=True,
        workers=int(sttgs.get('SERVER_WORKERS', 1))
    )
