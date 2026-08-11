from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from smtp.lieferverzugs_mail import sende_lieferverzugs_mail
from db.kanban_db_connection import get_mail_for_vorgangsnummer
from db.combined_db_connection import combined_database_data

load_dotenv()
FAVICON_URL = os.getenv("FAVICON_URL")
SERVERURL = os.getenv("SERVERURL")
SERVERPORT = int(os.getenv("SERVERPORT"))

# Setup templates
templates = Jinja2Templates(directory="src/templates")

# Initialize app
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

departments = [
    "Pauli",
    "Zimmergestelle",
    "Rückenliegebrett",
    "Stehgeräte",
    "Fahrgestelle",
    "Sonderbau"
]

class Lieferverzug(BaseModel):
    vorgangsnummer: str
    kommission: str
    artikelbeschreibung: str
    neue_kw: int
    lieferverzugs_grund: str
    email: str


r"""
 _   _ _____ __  __ _      
| | | |_   _|  \/  | |     
| |_| | | | | |\/| | |     
|  _  | | | | |  | | |___  
|_| |_| |_| |_|  |_|_____| 
"""
# Wer das ließt ist ein Femboy :3
# @app.get("/", response_class=HTMLResponse)
# async def root(request: Request):
#     return RedirectResponse(url="/open_orders/")
# @app.get("/open_orders/", response_class=HTMLResponse)
# async def open_orders(request: Request):
#     return templates.TemplateResponse(
#         request = request,
#         name = "index.html",
#         context = {
#             "request": request,
#             "favicon_url": FAVICON_URL
#         }
#     )

@app.get("/{department}/", response_class=HTMLResponse)
async def open_orders(request: Request, department: str):
    if department not in departments:
        raise HTTPException(status_code=404, detail="Department not found")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "favicon_url": FAVICON_URL,
            "department": department,
        },
    )




r"""
    _    ____ ___  
   / \  |  _ \_ _| 
  / _ \ | |_) | |  
 / ___ \|  __/| |  
/_/   \_\_|  |___| 
"""
@app.get("/rows/{department}")
async def get_all_rows(department: str):
    if department not in departments:
        raise HTTPException(status_code=400, detail="Invalid department")
    get_db_data = await combined_database_data(department)
    return JSONResponse(content=get_db_data)

@app.post("/verzug/")
async def insert_verzug(lieferverzug: Lieferverzug):
    from db.internal_db_connection import insert_lieferverzug
    try:
        sende_lieferverzugs_mail(
            empfaenger_email=lieferverzug.email,
            bestellnummer=lieferverzug.vorgangsnummer,
            voraussichtliche_kw=lieferverzug.neue_kw,
            komission=lieferverzug.kommission,
            artikelbeschreibung=lieferverzug.artikelbeschreibung
        )
        await insert_lieferverzug(
            vorgangsnummer=lieferverzug.vorgangsnummer,
            neue_kw=lieferverzug.neue_kw,
            lieferverzugs_grund=lieferverzug.lieferverzugs_grund
        )
        return JSONResponse(content={"message": "Lieferverzug inserted successfully."})
    except Exception as e:
        print(f"Error inserting Lieferverzug: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVERURL, port=SERVERPORT)
