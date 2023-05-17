from config import engine
from config import metadata
from config import app
import uvicorn

from routers.post.route import post_route
from routers.mikrotik.route import mikrotik

app.include_router(post_route, prefix="/api/post", tags=["post"])
app.include_router(mikrotik, prefix="/api/mikrotik", tags=["mikrotik"])

@app.get("/")
def home():
    return {"message": "Welcome to SpiderMikrotik API"}


if __name__ == '__main__':
    metadata.create_all(engine)
    uvicorn.run("main:app", host="127.0.0.1", port=8080)