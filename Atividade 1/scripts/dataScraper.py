import pathlib
import json
from time import sleep
import re

PATH = pathlib.Path(__file__).parent
WEBMOTORS_DATA = PATH / "webmotors_data"
DATA = PATH.parent / "data"

normal_data = []

for archive in WEBMOTORS_DATA.iterdir():

    with open(archive, "r", encoding="utf-8") as f:
        data = json.load(f)

    for announce in data["SearchResults"]:
        vehicle = announce["Specification"]
        model = vehicle["Model"]["Value"]
        make = vehicle["Make"]["Value"]
        ports = vehicle["NumberPorts"]
        transmission = vehicle["Transmission"]
        bodyType = vehicle["BodyType"]
        year = vehicle["YearModel"]
        odometer = vehicle["Odometer"]
        color = vehicle["Color"]["Primary"]
        

        version: str = vehicle["Version"]["Value"]
        potency_match = re.search(r"(\d+\.\d+)", version)
        valves_match = re.search(r"(\d+)(?=\s*V)", version)
        
        if "FLEX" in version:
            fuel = "Flex"
        elif any(word in version for word in ["GASOLINA", "TSI", "INGENIUM", "SUPERCHARGED", "TWIN POWER", "MPI"]):
            fuel = "Gasolina"
        elif "ÁLCOOL" in version:
            fuel = "Etanol"
        elif "ELÉTRICO" in version:
            fuel = "Elétrico"
        elif "DIESEL" in version:
            fuel = "Diesel"
        elif any(word in version for word in ["MHEV", "HYBRID", "RECHARGE", "HÍBRIDO", "HEV"]):
            fuel = "Híbrido"
        else:
            print(version)
            raise TypeError()
        
        potency = potency_match.group(1) if potency_match else "N/A"
        valves = valves_match.group(1) if valves_match else "N/A"

        state: str = announce["Seller"]["Localization"][0]["State"]
        state = state[-3] + state[-2]
        
        price = announce["Prices"]["Price"]

        normal_data.append(
            {
                "Preço": price,
                "Marca": make,
                "Modelo": model,
                "Portas": ports,
                "Transmissão": transmission,
                "Tipo": bodyType,
                "Ano": year,
                "Quilometragem": odometer,
                "Cor": color,
                "Válvulas": valves,
                "Motor": potency,
                "Estado": state,
                "Combustível": fuel
            }
        )



with open(DATA / "data.json", "w", encoding="utf-8") as f:
    json.dump(normal_data, f, ensure_ascii=False)


