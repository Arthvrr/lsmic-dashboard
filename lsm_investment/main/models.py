from django.db import models

class Position(models.Model):
    ticker = models.CharField(max_length=15)  # le ticker Yahoo, ex: "AIR.PA"
    shares = models.FloatField()               # nombre de parts détenues
    purchase_price = models.FloatField(null=True, blank=True)  # optionnel
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} ({self.shares} parts)"

class AdminEmail(models.Model):
    class Meta:
        verbose_name = "Envoyer un email"
        verbose_name_plural = "Envoyer des emails"

    def __str__(self):
        return "Envoyer un email à tous les utilisateurs"