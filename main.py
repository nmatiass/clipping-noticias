from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente (.env)
load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")
API_URL = "https://gnews.io/api/v4/search"

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def buscar_noticias(tema):
    params = {
        'q': tema,
        'lang': 'pt',
        'country': 'br',
        'max': 10,
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('articles', [])
    else:
        print(f"Erro na API: {response.status_code}")
        return []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    temas = ["política", "economia", "educação", "meio ambiente", "tecnologia", "congresso nacional"]
    clipping = {}

    for tema in temas:
        clipping[tema] = buscar_noticias(tema)

    return templates.TemplateResponse("index.html", {"request": request, "clipping": clipping})
