from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NewsletterSubscriber

@receiver(post_save, sender=User)
def create_newsletter_subscriber(sender, instance, created, **kwargs):
    if created:
        NewsletterSubscriber.objects.create(user=instance)