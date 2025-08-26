import os
import pandas as pd
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Wczytaj dane z Excela
df = pd.read_excel("Categorization_tool_CAPL.xlsx", sheet_name="tool", engine="openpyxl")

app = FastAPI()

# Serwowanie plików statycznych (np. obrazki)
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 🔹 Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # możesz podać dokładnie domenę Salesforce, np. ["https://kingfisher.builder.salesforce-experience.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Middleware X-Frame-Options + CSP
@app.middleware("http")
async def add_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Frame-Options"] = "ALLOWALL"
    response.headers["Content-Security-Policy"] = "frame-ancestors *"
    return response

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
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results, "category": category}
    )
