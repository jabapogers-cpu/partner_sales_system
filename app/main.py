from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Sale
from utils import json_to_dict_list, date_today, add_sale
import os

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sales/category/{category}")
def read_category(category: str, db: Session = Depends(get_db)):
    sales = db.query(Sale).all()
    return_list = []
    for sale in sales:
        if sale.category == category:
            return_list.append(sale)
    return return_list

@app.get("/sales")
def get_all_sales(db: Session = Depends(get_db)):
    sales = db.query(Sale).all()

    categories = {}
    for sale in sales:
        category = sale.category
        categories[category] = categories.get(category, 0) + 1

    today = date_today()
    new_sales = sum(1 for sale in sales if sale.date_of_add == today)

    return {
        "new": new_sales,
        "categories": categories,
        "sales": sales
    }

# путь к json
path_to_json = os.path.join(os.path.dirname(__file__), 'sales.json')


