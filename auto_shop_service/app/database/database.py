from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CarDB(Base):
    __tablename__ = 'car_inventory_bespokoev'

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
