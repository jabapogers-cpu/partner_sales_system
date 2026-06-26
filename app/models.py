from sqlalchemy import Column, Integer, String, Text, Date
from database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False) # Название компании
    sale_name = Column(String(255), nullable=False) # Название акции
    date_of_add = Column(String(12), nullable=False) # Дата добавления
    category = Column(String(50), nullable=False, index=True) # Категория
    how_to_get = Column(Text, nullable=False) # Условия получения акции
    sale_period = Column(Date, nullable=False) # Дата окончания акции
    about_partner = Column(Text, nullable=True) # Информация о компании партнера
    promo = Column(String(100), nullable=True) # Промокод
    address = Column(String(500), nullable=False) # Ссылка на страницу проведения акции