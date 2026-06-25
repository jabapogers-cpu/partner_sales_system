from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Sale
from utils import json_to_dict_list, date_today, add_sale
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sales", response_class=HTMLResponse)
def sales_page(request: Request, db: Session = Depends(get_db)):
    sales = db.query(Sale).all()

    categories = {}
    for sale in sales:
        categories[sale.category] = categories.get(sale.category, 0) + 1

    today = date_today()
    new_count = sum(1 for sale in sales if sale.date_of_add == today)

    return templates.TemplateResponse(
        request,
        "sales.html",
        {
            "sales": sales,
            "categories": categories,
            "new_count": new_count,
        },
    )


@app.get("/sales/new", response_class=HTMLResponse)
def new_sales_page(request: Request, db: Session = Depends(get_db)):
    today = date_today()
    sales = db.query(Sale).filter(Sale.date_of_add == today).all()

    return templates.TemplateResponse(
        request,
        "category.html",
        {
            "category": "Новые",
            "sales": sales,
        },
    )


@app.get("/sales/category/{category}", response_class=HTMLResponse)
def category_page(request: Request, category: str, db: Session = Depends(get_db)):
    sales = db.query(Sale).filter(Sale.category == category).all()

    return templates.TemplateResponse(
        request,
        "category.html",
        {
            "category": category,
            "sales": sales,
        },
    )