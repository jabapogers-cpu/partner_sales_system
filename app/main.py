from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Sale
from datetime import date
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

    today = str(date.today())
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
    today = str(date.today())
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


@app.get("/sales/offer/{sale_id}", response_class=HTMLResponse)
def offer_page(request: Request, sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if sale is None:
        raise HTTPException(status_code=404, detail="Акция не найдена")

    return templates.TemplateResponse(
        request,
        "offer.html",
        {
            "sale": sale,
        },
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse(request, "admin.html", {})


@app.post("/admin", response_class=HTMLResponse)
def admin_add_sale(
    request: Request,
    db: Session = Depends(get_db),
    company_name: str = Form(...),
    sale_name: str = Form(...),
    category: str = Form(...),
    how_to_get: str = Form(...),
    sale_period: str = Form(...),
    about_partner: str = Form(""),
    promo: str = Form(""),
    address: str = Form(...),
):
    context = {}
    try:
        new_sale = Sale(
            company_name=company_name,
            sale_name=sale_name,
            date_of_add=str(date.today()),
            category=category,
            how_to_get=how_to_get,
            sale_period=sale_period,
            about_partner=about_partner or None,
            promo=promo or None,
            address=address,
        )
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        context["success"] = new_sale.id
    except Exception as e:
        db.rollback()
        context["error"] = str(e)

    return templates.TemplateResponse(request, "admin.html", context)