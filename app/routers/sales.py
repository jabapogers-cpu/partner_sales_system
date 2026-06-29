from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from models import Sale
from templates_config import templates

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("", response_class=HTMLResponse)
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


@router.get("/new", response_class=HTMLResponse)
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


@router.get("/category/{category}", response_class=HTMLResponse)
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


@router.get("/offer/{sale_id}", response_class=HTMLResponse)
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