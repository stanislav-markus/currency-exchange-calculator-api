import csv
import os

from django.core.management.base import BaseCommand
from calculator.api.models import CurrencyRate, CurrencyPair


class Command(BaseCommand):
    help = 'Creates data in database from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the CSV file with data.')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        try:
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    reader = csv.DictReader(f)
                    for line in reader:
                        date = line.pop('Date')
                        for code, rate in line.items():
                            print(code, rate)
                            currency_pair, created = CurrencyPair.objects.get_or_create(code=code)
                            currency_rate, created = CurrencyRate.objects.get_or_create(date=date, pair=currency_pair, rate=rate)
        except Exception as e:
            raise Exception("Failed to create data: error {}".format(e))
        self.stdout.write("Ok.")
