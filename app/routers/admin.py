from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import date
from typing import Any

from database import get_db
from models import Sale
from templates_config import templates

router = APIRouter(prefix="/admin", tags=["admin"])


def create_sale(
    db: Session,
    company_name: str,
    sale_name: str,
    category: str,
    how_to_get: str,
    sale_period: str,
    about_partner: str,
    promo: str,
    address: str,
) -> dict[str, Any]:
    
    context: dict[str, Any] = {}
    try:
        sale_period_date: date = date.fromisoformat(sale_period)

        new_sale = Sale(
            company_name=company_name,
            sale_name=sale_name,
            date_of_add=str(date.today()),
            category=category,
            how_to_get=how_to_get,
            sale_period=sale_period_date,
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

    return context


@router.get("", response_class=HTMLResponse)
def admin_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "admin.html", {})


@router.post("", response_class=HTMLResponse)
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
) -> HTMLResponse:

    context: dict[str, Any] = create_sale(
        db=db,
        company_name=company_name,
        sale_name=sale_name,
        category=category,
        how_to_get=how_to_get,
        sale_period=sale_period,
        about_partner=about_partner,
        promo=promo,
        address=address,
    )
    return templates.TemplateResponse(request, "admin.html", context)