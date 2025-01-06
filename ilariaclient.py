from flask import requests
import json

SERVER_URL = "http://127.0.0.1:5000"

def cerca_case_vendita(indirizzo, prezzo_max):
    payload = {"indirizzo" : indirizzo, "prezzo_max" : prezzo_max}
    response = requests.post(f"{SERVER_URL}/cerca_case_vendita", json=payload)
    return response.json()

def vendi_casa(catastale, filiale_venditrice, prezzo_vendita):
    payload = {"catastale" : catastale, "filiale_venditrice" : filiale_venditrice, "prezzo_vendita" : prezzo_vendita}
    response = requests.post(f"{SERVER_URL}/vendi_casa", json=payload)
    return response.json()

def report_marketing(data_inizio, data_fine):
    payload = {"data_inizio" : data_inizio, "data_fine" : data_fine}
    response = requests.post(f"{SERVER_URL}/report_marketing", json=payload)
    with open("report_marketing.json","w") as file:
        json.dump(response.json(), file, indent=4)
    return "Report salvato in 'report_marketing.json'."

#ESEMPIO D'USO
if __name__ == "__main__":
    print(cerca_case_vendita("Via Roma, 30000"))
    print(vendi_casa(1,2, 250000))
    print(report_marketing("2023-01-01", "2023-12-31"))

