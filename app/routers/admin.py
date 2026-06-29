from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from models import Sale
from templates_config import templates

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("", response_class=HTMLResponse)
def admin_page(request: Request):
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
):
    context = {}
    try:
        sale_period_date = date.fromisoformat(sale_period)

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

    return templates.TemplateResponse(request, "admin.html", context)