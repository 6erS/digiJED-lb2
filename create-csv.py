import csv;
import json;
import requests;
import boto3;
from datetime import datetime;

# Підключення до Amazon S3
s3 = boto3.resource('s3');

# Отримання даних про курс гривні до долара
usd_url = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json"
usd_response = requests.get(usd_url)
usd_data = usd_response.json()

# Отримання даних про курс гривні до євро
eur_url = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json"
eur_response = requests.get(eur_url)
eur_data = eur_response.json()

# Створення списку з потрібними даними
data = []
for i in range(len(usd_data)):
    row = [usd_data[i]['exchangedate'], usd_data[i]['rate'], eur_data[i]['rate']]
    data.append(row)

# Запис данхих у CSV-файл
filename = 'current_rate.csv';
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'USD', 'EUR'])
    writer.writerows(data)

# Завантаження CSV-файл на Amazon S3
bucket_name = 'digi-jed-db';
object_key = f'exchange_rates/{filename}';

s3.meta.client.upload_file(filename, bucket_name, object_key);