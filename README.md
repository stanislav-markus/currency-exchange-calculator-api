# currency-exchange-calculator-api

```
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser --email admin@example.com --username admin

python manage.py create_data_from_csv ~/Downloads/exchange.csv

python manage.py runserver


# historical data for pair
curl -u admin:admin http://localhost:8000/rates/?pair__code=EUR/USD

# data for pair and date
curl -u admin:admin http://localhost:8000/rates/?pair__code=EUR/USD&date=2020-03-05

# For non-direct ratio NZD/AUD 
curl -u admin:admin http://localhost:8000/rates/?pair__code=NZD/AUD&date=2020-03-05

```