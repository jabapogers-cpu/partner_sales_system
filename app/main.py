import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import sales, admin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

app.include_router(sales.router)
app.include_router(admin.router)