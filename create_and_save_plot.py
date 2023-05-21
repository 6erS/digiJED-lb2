import boto3
import pandas
import matplotlib.pyplot as plt

# Встановлення з'єднання з S3
s3 = boto3.client('s3');
bucket_name = 'digi-jed-db'
key = 'exchange_rates/current_rate.csv'
obj = s3.get_object(Bucket=bucket_name, Key=key)

# Зчитування даних з файлу
data = pandas.read_csv(obj['Body'])
#data['Date'] = pandas.to_datetime(data['Date']);
print(data)

# Побудова графіку
plt.plot(data['Date'], data['USD'], label='USD');
plt.plot(data['Date'], data['EUR'], label='EUR');
plt.xlabel('Дата');
plt.ylabel('Курс');
plt.title('Курс валют USD та EUR у 2021 році');
plt.legend();

# Збереження графіка в файлі
plt.savefig("plot.png");

plt.show();


# Завантаження CSV-файл на Amazon S3
with open('plot.png', 'rb') as file:
    s3.put_object(Bucket='digi-jed-db', Key='exchange_rates/plot.png', Body=file);