from bs4 import BeautifulSoup as bs

import requests
from datetime import datetime
import json
import time
import xlsxwriter


links = [
    "https://www.numbeo.com/gas-prices/in/Banja-Luka",
    "https://www.numbeo.com/gas-prices/in/Bihac-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Bijeljina-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Bosanska-Krupa-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Brcko-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Bugojno-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Capljina-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Cazin-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Doboj-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Gracanica-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Gradacac-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Gradiska-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Istočno-Sarajevo-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Kakanj-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Konjic-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Livno-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Lukavac-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Mostar",
    "https://www.numbeo.com/gas-prices/in/Neum-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Pale-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Prijedor-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Sanski-Most-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Sarajevo",
    "https://www.numbeo.com/gas-prices/in/Tesanj-Tešanj-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Travnik-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Trebinje-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Tuzla",
    "https://www.numbeo.com/gas-prices/in/Visoko-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Vogosca-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Zenica-Bosnia-And-Herzegovina",
    "https://www.numbeo.com/gas-prices/in/Zepce-Bosnia-And-Herzegovina",
]
def gov():
    cur_date = datetime.today().strftime('%Y-%m-%d')
    with open("story.json", 'r', encoding="utf-8") as story:
        story = json.load(story)

    story[cur_date] = []

    for i in links:
        try:
            URL_TEMPLATE = i
            r = requests.get(URL_TEMPLATE)

            soup = bs(r.text, "html.parser")
            vacancies_names = soup.find_all('span', class_='first_currency')
            price = float(str(vacancies_names[0].text).split(' ')[0])
            vacancies_names = soup.find_all('table', class_='table_indices')
            city = str(vacancies_names[0].tr.text)

            region = city[city.find("from") + 5:]

            story[cur_date].append(
                {
                    "region": region,
                    "price_MK": price
                }
            )
        except Exception as error:
            print(error)
            print(i)

    with open('story.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(story))




def rewrite_exl():

    workbook = xlsxwriter.Workbook('excel.xlsx')
    worksheet = workbook.add_worksheet()

    with open("story.json", 'r', encoding="utf-8") as story:
        story = json.load(story)


    worksheet.write(0, 0, "city")
    worksheet.write(0, 1, "price KM")
    worksheet.write(0, 2, "date")

    for ind, date in enumerate(story):
        for ind_2, item in enumerate(story[date]):
            row = ind * len(story[date]) + ind_2 + 1
            worksheet.write(row, 0, item["region"])
            worksheet.write(row, 1, item["price_MK"])
            worksheet.write(row, 2, date)

    workbook.close()

while True:
    gov()
    rewrite_exl()
    time.sleep(24 * 60 * 60)




