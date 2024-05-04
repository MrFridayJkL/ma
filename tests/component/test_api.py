import requests

base_url = 'http://localhost:8001'
manufacturers_url = f'{base_url}/manufacturers'
models_url = f'{base_url}/models'
vehicle_types_url = f'{base_url}/vehicle_types'

test_manufacturer = "honda"
test_make = "mercedes"


def test_1_get_all_manufacturers():
    response = requests.get(manufacturers_url)
    assert response.status_code == 200
    data = response.json()
    assert 'Results' in data
    assert len(data['Results']) > 0


def test_2_get_models_for_manufacturer():
    response = requests.get(f"{models_url}/{test_manufacturer}")
    assert response.status_code == 200
    data = response.json()
    assert 'Results' in data
    assert len(data['Results']) > 0


def test_3_get_vehicle_types_for_make():
    response = requests.get(f"{vehicle_types_url}/{test_make}")
    assert response.status_code == 200
    data = response.json()
    assert 'Results' in data
    assert len(data['Results']) > 0
