import uvicorn

from app.config import sttgs


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host=sttgs.get('HOST'),
        port=int(sttgs['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
