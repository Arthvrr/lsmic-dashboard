from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    ticker = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    shares = models.FloatField()             
    purchase_price = models.FloatField(null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} ({self.shares} parts)"

class AdminEmail(models.Model):
    class Meta:
        verbose_name = "Envoyer un email"
        verbose_name_plural = "Envoyer des emails"

    def __str__(self):
        return "Envoyer un email à tous les utilisateurs"

class NewsletterSubscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)  # True = abonné, False = désabonné

    def __str__(self):
        return f"{self.user.username} ({'abonné' if self.subscribed else 'désabonné'})"