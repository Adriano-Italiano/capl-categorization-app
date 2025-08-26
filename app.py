import os
import pandas as pd
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Wczytaj dane z Excela
df = pd.read_excel("Categorization_tool_CAPL.xlsx", sheet_name="tool", engine="openpyxl")

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# Strona główna z formularzem
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

# Obsługa wyszukiwania
@app.post("/", response_class=HTMLResponse)
async def search(request: Request, category: str = Form(...)):
    wyniki = df[df['front_category_leaf_name'].str.lower() == category.lower()]
    if wyniki.empty:
        results = [{"pim_category_id": "Nie znaleziono", "pim_category_full_path": "Brak danych"}]
    else:
        results = wyniki[['pim_category_id', 'pim_category_full_path']].drop_duplicates().to_dict(orient="records")
    
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "category": category})
