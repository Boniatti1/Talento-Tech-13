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

        turbo_keywords = [
            "Turbo",
            "T ",
            "TSI",
            "TFSI",
            "THP",
            "T-GDI",
            "GDI",
            "ECOTEC",
            "BOOST",
            "TWIN",
        ]
        turbo = 1 if any(word in version.split() for word in turbo_keywords) else 0

        if "FLEX" in version:
            fuel = "Flex"
        elif any(
            word in version
            for word in [
                "GASOLINA",
                "TSI",
                "INGENIUM",
                "SUPERCHARGED",
                "TWIN POWER",
                "MPI",
            ]
        ):
            fuel = "Gasolina"
        elif "ÁLCOOL" in version:
            fuel = "Etanol"
        elif "ELÉTRICO" in version:
            fuel = "Elétrico"
        elif any(word in version for word in ["DIESEL", "PICKUP"]):
            fuel = "Diesel"
        elif any(
            word in version for word in ["MHEV", "HYBRID", "RECHARGE", "HÍBRIDO", "HEV"]
        ):
            fuel = "Híbrido"
        else:
            print(version)
            raise TypeError()

        potency = potency_match.group(1) if potency_match else "N/A"
        valves = valves_match.group(1) if valves_match else "N/A"

        if valves == "N/A":
            print(version)

        state: str = announce["Seller"]["Localization"][0]["State"]
        state = state[-3] + state[-2]

        price = announce["Prices"]["Price"]
        fipe = announce.get("FipePercent")

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
                "Turbo": turbo,
                "Estado": state,
                "Combustível": fuel,
                "Fipe": fipe,
            }
        )


with open(DATA / "data.json", "w", encoding="utf-8") as f:
    json.dump(normal_data, f, ensure_ascii=False)
