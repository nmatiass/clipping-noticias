from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from helpers import gerar_clipping
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    noticias = gerar_clipping()
    return templates.TemplateResponse("index.html", {"request": request, "noticias": noticias})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
