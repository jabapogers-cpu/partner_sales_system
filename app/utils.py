import json
from datetime import date
from database import SessionLocal
from models import Sale


#
def add_sale(company_name, sale_name, category, how_to_get, sale_period, about_partner, promo, address):
    """
    Добавляет новую запись в базу данных

    :param company_name: - название компании
    :param sale_name: - название акции
    :param category: - категория
    :param how_to_get: - условия акции
    :param sale_period: - период акции
    :param about_partner: - о партнере
    :param promo: - промокод
    :param address: - ссылка на сайт компании

    """
    db = SessionLocal()
    try:
        new_sale = Sale(
            company_name=company_name,
            sale_name=sale_name,
            date_of_add=str(date.today()),
            category=category,
            how_to_get=how_to_get,
            sale_period=sale_period,
            about_partner=about_partner,
            promo=promo,
            address=address
        )

        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        print(f"Запись добавлена! ID: {new_sale.id}")

    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")

    finally:
        db.close()

add_sale('нет',
         'не',
         'не',
         'нет',
         '1-нет',
         'нет',
         'нет',
         'нет',)



def date_today():
    current_date = date.today()
    return str(current_date)


