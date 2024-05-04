import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from sqlalchemy.orm import Session
from typing import Annotated
from keycloak import KeycloakOpenID
from database import database as database
from database.database import CarDB
from model.model import Car

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_car")
async def add_car(car: Car, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        new_car = CarDB(**car.dict())
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        return new_car
    else:
        return "Wrong JWT Token"

@app.get("/cars")
async def list_cars(db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        return db.query(CarDB).all()
    else:
        return "Wrong JWT Token"

@app.get("/get_car_by_id/{car_id}")
async def get_car_by_id(car_id: int, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        car = db.query(CarDB).filter(CarDB.id == car_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        return car
    else:
        return "Wrong JWT Token"

@app.delete("/delete_car/{car_id}")
async def delete_car(car_id: int, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        car = db.query(CarDB).filter(CarDB.id == car_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        db.delete(car)
        db.commit()
        return {"message": "Car deleted successfully"}
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
