from django.db import models

class Position(models.Model):
    ticker = models.CharField(max_length=15)  # le ticker Yahoo, ex: "AIR.PA"
    shares = models.FloatField()               # nombre de parts détenues
    purchase_price = models.FloatField(null=True, blank=True)  # optionnel
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} ({self.shares} parts)"