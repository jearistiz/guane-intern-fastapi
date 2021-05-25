import uvicorn

from app.config import sttgs
from app.db.db_manager import init_db


if __name__ == '__main__':

    # Initialize database
    init_db()

    uvicorn.run(
        "app:app",
        host=sttgs.get('HOST', 'localhost'),
        port=int(sttgs.get('PORT', 8080)),
        reload=True,
        debug=True,
        workers=int(sttgs.get('SERVER_WORKERS', 1))
    )
