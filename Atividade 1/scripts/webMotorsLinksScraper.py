import requests
import pathlib
import json

PATH = pathlib.Path(__file__).parent
WEBMOTORS_DATA = PATH / "webmotors_data"

PER_PAGE = 800
MIN_YEAR = 2000
MIN_PRICE = 5000
MAX_PRICE = 20000

price_intervals = [
    (1000, 20000),
    (20001, 40000),
    (40001, 60000),
    (60001, 80000),
    (80001, 100000),
    (100001, 150000),
    (150001, 200000),
    (200001, 250000),
    (250000, 9999999),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

for interval in price_intervals:
    MIN_PRICE, MAX_PRICE = interval
    url = f"https://www.webmotors.com.br/api/search/car?displayPerPage={PER_PAGE}&actualPage=1&showMenu=true&showCount=true&showBreadCrumb=true&order=1&url=https:%2F%2Fwww.webmotors.com.br%2Fcarros-usados%2Festoque%2Fde.{MIN_YEAR}%3Ftipoveiculo%3Dcarros-usados%26anode%3D{MIN_YEAR}%26precode%3D{MIN_PRICE}%26precoate%3D{MAX_PRICE}%26lkid%3D1000%26page%3D1&mediaZeroKm=false"
    try:
        response = requests.get(url, headers=HEADERS)
        print(f"Acessando a url: {url}")
        if response.status_code != 200:
            raise requests.RequestException(f"Código de erro: {response.status_code}")

        with open(
            WEBMOTORS_DATA / f"{MIN_PRICE}-{MAX_PRICE}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(response.json(), f, ensure_ascii=False)

    except Exception as e:
        print(f"Erro: {e}")
