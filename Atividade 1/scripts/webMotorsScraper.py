from playwright.sync_api import sync_playwright
from time import sleep
import pathlib
import json

with open("cookies.json", "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    cookie["url"] = "https://webmotors.com"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)

    intervals = [(2000 + 4 * i, 2005 + 4 * i) for i in range(1, 2)]
    context = browser.new_context()
    context.add_cookies(cookies=cookies)
    page = context.new_page()

    elements = []
    for interval in intervals:
        a, b = interval

        # for index in range(1,15):
        for index in range(1, 2):
            try:
                
                page.goto(
                    f"https://www.webmotors.com.br/carros-usados/estoque/de.{a}/ate.{b}?tipoveiculo=carros-usados&anode=2000&anoate=2004&lkid=1000&page={index}"
                )
                sleep(8)
                links = page.locator("._Link_70j0p_83").all()
                for link in links:
                    elements.append(link.get_attribute("href"))

            except Exception as e:
                print("=====================")
                print(
                    f"Erro na url https://www.webmotors.com.br/carros-usados/estoque/de.{a}/ate.{b}?tipoveiculo=carros-usados&anode=2000&anoate=2004&lkid=1000&page={index}"
                )
                print(e)
                print("=====================")

            finally:
                context.close()


for e in elements:
    print(e)
