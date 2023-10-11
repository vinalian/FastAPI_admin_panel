from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.auth import router as auth_router
from app.main_page import router as main_page_router
from pydantic import BaseModel
import sys


class Settings(BaseModel):
    BASE_URL: str = "http://localhost:8001"
    USE_NGROK: bool = False


settings = Settings()
app = FastAPI()
app.include_router(auth_router)
app.include_router(main_page_router)
app.mount("/css", StaticFiles(directory="../css"), name="css")
app.mount("/js", StaticFiles(directory="../js"), name="JavaScript")

if __name__ == "__main__":
    if settings.USE_NGROK:
        from pyngrok import ngrok
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8001"
        public_url = ngrok.connect(port).public_url
        print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)

