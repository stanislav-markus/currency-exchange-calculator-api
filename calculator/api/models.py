from django.db import models


class CurrencyPair(models.Model):
    code = models.CharField(
                        max_length=7)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']


class CurrencyRate(models.Model):
    rate = models.DecimalField(
                        max_digits=9,
                        decimal_places=4)
    pair = models.ForeignKey(
                        CurrencyPair,
                        on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.rate)
