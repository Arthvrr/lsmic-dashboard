from django.contrib import admin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from main.forms import EmailForm
from .models import Position, AdminEmail
from django.contrib.auth import get_user_model
import os

print(os.getenv("SMTP_PASSWORD"))

User = get_user_model()

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
                recipients = User.objects.values_list("email", flat=True)
                send_mail(subject, message, "arthurlouette12@gmail.com", recipients)
                self.message_user(request, "Emails envoyés avec succès !")
                return redirect(".")
        else:
            form = EmailForm()
        context = {"form": form}
        return render(request, "admin/send_email.html", context)