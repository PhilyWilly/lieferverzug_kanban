from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from app.smtp.lieferverzugs_mail import sende_lieferverzugs_mail
from db.kanban_db_connection import get_mail_for_vorgangsnummer
from db.combined_db_connection import combined_database_data

load_dotenv()
FAVICON_URL = os.getenv("FAVICON_URL")

# Setup templates
templates = Jinja2Templates(directory="src/templates")

# Initialize app
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

class Lieferverzug(BaseModel):
    vorgangsnummer: str
    neue_kw: int
    lieferverzugs_grund: str
    email: str = None  # Optional email field


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

@app.post("/verzug/")
async def insert_verzug(lieferverzug: Lieferverzug):
    from db.internal_db_connection import insert_lieferverzug
    try:
        mail = lieferverzug.email
        print(f"Received email from request: {mail}")
        if not mail:
            mail = await get_mail_for_vorgangsnummer(lieferverzug.vorgangsnummer)
        print(f"Mail for Vorgangsnummer {lieferverzug.vorgangsnummer}: {mail}")
        sende_lieferverzugs_mail(
            empfaenger_email=mail,
            bestellnummer=lieferverzug.vorgangsnummer,
            voraussichtliche_kw=lieferverzug.neue_kw,
            komission="N/A"  # Replace with actual komission if available
        )
        insert_lieferverzug(
            vorgangsnummer=lieferverzug.vorgangsnummer,
            neue_kw=lieferverzug.neue_kw,
            lieferverzugs_grund=lieferverzug.lieferverzugs_grund
        )
        return JSONResponse(content={"message": "Lieferverzug inserted successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
