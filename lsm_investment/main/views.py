from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Position, NewsletterSubscriber
import yfinance as yf
import os
from django.conf import settings
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

def get_last_monday():
    """Calcule la date du dernier lundi (début de la semaine de trading)."""
    today = datetime.now().date()
    # 0 = Lundi, 1 = Mardi, ... 6 = Dimanche
    days_to_subtract = today.weekday() 
    return today - timedelta(days=days_to_subtract)

# def home(request):
#     return render(request, 'home.html')

def home(request):
    top_flop_data = []
    
    # --- 1. Préparation des données ---
    positions = Position.objects.all()
    monday_date = get_last_monday()
    
    for pos in positions:
        stock = yf.Ticker(pos.ticker)
        
        try:
            # Récupération des données historiques depuis le dernier lundi
            hist_data = stock.history(start=monday_date)
            
            # Prix de clôture du Lundi (ou de la première journée de trading de la semaine)
            start_price = hist_data['Close'].iloc[0] if not hist_data.empty else None
            
            # Prix actuel
            current_price = stock.info.get('regularMarketPrice') or stock.info.get('currentPrice') or stock.info.get('previousClose')
            
            if start_price and current_price:
                # Calcul du ROI en pourcentage (%)
                weekly_roi_percent = ((current_price - start_price) / start_price) * 100
            else:
                weekly_roi_percent = 0
                
        except Exception as e:
            print(f"Erreur pour le ticker {pos.ticker}: {e}")
            weekly_roi_percent = 0
            
        top_flop_data.append({
            'ticker': pos.ticker,
            'roi_percent': weekly_roi_percent,
        })

    # --- 2. Trier pour obtenir le TOP 3 et FLOP 3 ---
    
    # Trier la liste par ROI en pourcentage (du plus grand au plus petit)
    sorted_data = sorted(top_flop_data, key=lambda x: x['roi_percent'], reverse=True)
    
    top3 = sorted_data[:3]
    flop3 = sorted_data[-3:]

    flop3 = list(reversed(flop3)) #reverse la liste
    
    return render(request, 'home.html', {
        'top3': top3,
        'flop3': flop3,
    })

def load_whitelist():

    ABSOLUTE_PROJECT_ROOT = Path("/home/Arthvrrr/lsmic-dashboard")
    whitelist_path = ABSOLUTE_PROJECT_ROOT / "whitelist_emails.txt"
    
    try:
        with open(str(whitelist_path), 'r') as f: 
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print(f"ATTENTION: Fichier de liste blanche non trouvé à: {whitelist_path}")
        return set()


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email'].lower()
        password = request.POST['password']
        password2 = request.POST['password2']

        EMAIL_WHITELIST = load_whitelist()

        if email not in EMAIL_WHITELIST:
            print(f"DEBUG: E-mail bloqué: '{email}'")
            messages.error(request, "Cet e-mail n'est pas autorisé à créer un compte.")

        elif password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Compte créé avec succès !")
            return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    subscribed = False
    try:
        sub, created = NewsletterSubscriber.objects.get_or_create(user=request.user)
        subscribed = sub.subscribed
    except:
        pass

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_username":
            new_username = request.POST.get("new_username")
            if new_username:
                request.user.username = new_username
                request.user.save()
                messages.success(request, "Nom d'utilisateur mis à jour !")
                return redirect("profile")

        elif action == "change_password":
            p1 = request.POST.get("new_password1")
            p2 = request.POST.get("new_password2")
            if p1 != p2:
                messages.error(request, "⚠️ Les mots de passe ne correspondent pas.")
            else:
                request.user.set_password(p1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Mot de passe mis à jour !")
            return redirect("profile")

        elif action == "toggle_newsletter":
            sub.subscribed = not sub.subscribed
            sub.save()
            messages.success(request, "Préférences newsletter mises à jour !")
            return redirect("profile")
        
        elif action == "delete_account":
            return redirect("confirm_delete")

    return render(request, "profile.html", {"subscribed": subscribed})


@login_required
def update_password_view(request):
    if request.method == "POST":
        p1 = request.POST.get("password1")
        p2 = request.POST.get("password2")

        if p1 != p2:
            messages.error(request, "⚠️ Les mots de passe ne correspondent pas.")
            return redirect("profile")

        request.user.set_password(p1)
        request.user.save()

        # Reste connecté après changement du mot de passe
        update_session_auth_hash(request, request.user)

        messages.success(request, "Mot de passe mis à jour !")
        return redirect("profile")

    return redirect("profile")

@login_required
def portfolio_view(request):
    positions = Position.objects.all()
    data = []

    for pos in positions:
        
        stock = yf.Ticker(pos.ticker)


        company_name = stock.info.get('longName')
        
        # Si le nom est trouvé et n'est pas déjà enregistré dans la DB, on l'enregistre
        if company_name and pos.company_name != company_name:
            pos.company_name = company_name
            pos.save() # Sauvegarde le nom dans la DB
        
        # Si le nom n'a pas été trouvé via yfinance mais existe dans la DB, on le récupère
        elif not company_name and pos.company_name:
            company_name = pos.company_name

        try:
            current_price = stock.info.get('regularMarketPrice') or stock.info.get('currentPrice') or stock.info.get('previousClose')
        except:
            current_price = None

        total_value = current_price * pos.shares if current_price else None
        if pos.purchase_price and current_price:
            roi_value = (current_price - pos.purchase_price) * pos.shares
            roi_percent = ((current_price - pos.purchase_price) / pos.purchase_price) * 100
        else:
            roi_value = None
            roi_percent = None

        data.append({
            'ticker': pos.ticker,
            'company_name': company_name,
            'shares': pos.shares,
            'purchase_price': pos.purchase_price,
            'current_price': current_price,
            'total_value': total_value,
            'roi_value': roi_value,
            'roi_percent': roi_percent,
            'logo': pos.logo,
        })

    tickers = [d['ticker'] for d in data]
    values = [d['total_value'] if d['total_value'] is not None else 0 for d in data]
    purchase_prices = [d['purchase_price'] if d['purchase_price'] is not None else 0 for d in data]
    current_prices = [d['current_price'] if d['current_price'] is not None else 0 for d in data]
    roi_percents = [d['roi_percent'] if d['roi_percent'] is not None else 0 for d in data]

    return render(request, 'portfolio.html', {
        'data': data,
        'tickers': tickers,
        'values': values,
        'roipercents': roi_percents,
        'purchase_prices': purchase_prices,
        'current_prices': current_prices,
    })


@login_required
def performance_view(request):
    # Exemple de données pour le membre connecté
    # Remplace ces valeurs par tes calculs réels
    invested_amount = 5000
    current_value = 6200
    roi_value = current_value - invested_amount
    roi_percent = (roi_value / invested_amount) * 100

    context = {
        'invested_amount': invested_amount,
        'current_value': current_value,
        'roi_value': roi_value,
        'roi_percent': roi_percent,
    }

    return render(request, 'performance.html', context)


def confirm_delete_view(request):
    """Affiche un formulaire de re-connexion avant suppression."""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user == request.user:
            user.delete()
            logout(request)
            messages.success(request, "Votre compte a bien été supprimé.")
            return redirect("home")

        else:
            messages.error(request, "Identifiants incorrects.")

    return render(request, "confirm_delete.html")