import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.get("/manufacturers")
async def get_all_manufacturers():
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllManufacturers?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error retrieving manufacturers data")


@app.get("/models/{manufacturer}")
async def get_models_for_manufacturer(manufacturer: str):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{manufacturer}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error retrieving models data")


@app.get("/vehicle_types/{make}")
async def get_vehicle_types_for_make(make: str):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleTypesForMake/{make}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error retrieving vehicle types data")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
