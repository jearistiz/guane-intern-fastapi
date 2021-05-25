import uvicorn

from app.config import sttgs
from app.db.db_manager import init_db


if __name__ == '__main__':

    # Initialize database
    init_db()

    uvicorn.run(
        "app:app",
        host=sttgs.get('HOST'),
        port=int(sttgs['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
