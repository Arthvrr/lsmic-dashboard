from django.contrib import admin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from main.forms import EmailForm
from .models import Position, AdminEmail, NewsletterSubscriber
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv
from pathlib import Path

User = get_user_model()

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / "login.env")
EMAIL_HOST_USER = os.getenv("SMTP_USER")

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'shares', 'purchase_price', 'logo')

@admin.register(AdminEmail)
class AdminEmailAdmin(admin.ModelAdmin):
    change_list_template = "admin/send_email.html"

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST":
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data["subject"]
                message = form.cleaned_data["message"]
                recipients = NewsletterSubscriber.objects.filter(subscribed=True).values_list("user__email", flat=True)
                send_mail(subject, message, EMAIL_HOST_USER, recipients)
                self.message_user(request, "Emails envoyés avec succès !")
                return redirect(".")
        else:
            form = EmailForm()
        context = {"form": form}
        return render(request, "admin/send_email.html", context)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed')
    list_filter = ('subscribed',) 
    list_editable = ('subscribed',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)