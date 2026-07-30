from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from app.db.combined_db_connection import combined_database_data

load_dotenv()
FAVICON_URL = os.getenv("FAVICON_URL")

# Setup templates
templates = Jinja2Templates(directory="src/templates")

# Initialize app
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")


r"""
 _   _ _____ __  __ _      
| | | |_   _|  \/  | |     
| |_| | | | | |\/| | |     
|  _  | | | | |  | | |___  
|_| |_| |_| |_|  |_|_____| 
"""
# Wer das ließt ist ein Femboy :3
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/open_orders/")
@app.get("/open_orders/", response_class=HTMLResponse)
async def open_orders(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "request": request,
            "favicon_url": FAVICON_URL
        }
    )


r"""
    _    ____ ___  
   / \  |  _ \_ _| 
  / _ \ | |_) | |  
 / ___ \|  __/| |  
/_/   \_\_|  |___| 
"""
@app.get("/rows/")
async def get_all_rows():
    get_db_data = combined_database_data()
    return JSONResponse(content= get_db_data)
    return JSONResponse(content=[
        {
            "jahr": 2026,
            "kw": 24,
            "kundenname": "Kunde A",
            "vorgangsnummer": "AU-202604/203065",
            "vorgangstext": "Vorgang A",
            "artikelbeschreibung": "Artikel A",
            "artikelnr": "A123"
         },
        {
            "jahr": 2026,
            "kw": 24,
            "kundenname": "Kunde B",
            "vorgangsnummer": "AU-202604/203066",
            "vorgangstext": "Vorgang B",
            "artikelbeschreibung": "Artikel B",
            "artikelnr": "B456"
         },
        {
            "jahr": 2026,
            "kw": 24,
            "kundenname": "Kunde C",
            "vorgangsnummer": "AU-202604/203067",
            "vorgangstext": "Vorgang C",
            "artikelbeschreibung": "Artikel C",
            "artikelnr": "C789"
         }

    ])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
