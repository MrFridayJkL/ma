import requests

base_url = 'http://localhost:8000'
add_car_url = f'{base_url}/add_car'
get_cars_url = f'{base_url}/cars'
get_car_by_id_url = f'{base_url}/get_car_by_id'
delete_car_url = f'{base_url}/delete_car'

new_car = {
    "id": 99,
    "model": "Model S",
    "manufacturer": "Tesla",
    "year": 2022,
    "price": 79999.99
}


def test_1_add_car():
    response = requests.post(add_car_url, json=new_car)
    assert response.status_code == 200
    assert response.json()['model'] == "Model S"


def test_2_get_cars():
    response = requests.get(get_cars_url)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_3_get_car_by_id():
    response = requests.get(f"{get_car_by_id_url}/99")
    assert response.status_code == 200
    assert response.json()['id'] == 99


def test_4_delete_car():
    delete_response = requests.delete(f"{delete_car_url}/99")
    assert delete_response.status_code == 200

    response = requests.get(f"{get_car_by_id_url}/99")
    assert response.status_code == 404
