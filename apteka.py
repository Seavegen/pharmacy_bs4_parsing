import csv
import time
import traceback

import requests
from bs4 import BeautifulSoup

count = 0
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
}

with open("result.csv", "w", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["#", "АДРЕС", "ТЕЛЕФОН", "ВРЕМЯ РАБОТЫ", "КОЛИЧЕСТВО", "ЦЕНА"])

    for num in range(1, 32):
        print(f'Parsing #{num}...')

        rs = requests.get(f"https://apteka.net.ua/search/availability/6810/page-{num}?region=&city=", headers=headers)
        soup = BeautifulSoup(rs.content, 'html.parser')

        for tr in soup.find("table").select("tbody > tr"):
            # Считаем, что если нет адреса, то нет данных в таблице
            address = tr.select_one('.col_address > a')
            if not address:
                break
            try:
                address = address.text
                phones = tr.select_one('.col_phone > a').text
                work_time = tr.select_one('.col_work').text
                quantity = tr.select_one('.col_quantity').text
                prices = tr.select_one('.quantity').text
                count += 1
                writer.writerow([count, address, phones, work_time, quantity, prices])

            except Exception as e:
                print(f'ERROR. #{num}, tr:\n{tr}\n error: {e}', traceback.format_exc())
        time.sleep(0.2)
