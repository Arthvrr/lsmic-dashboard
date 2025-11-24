from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Position, NewsletterSubscriber
import yfinance as yf

def home(request):
    return render(request, 'home.html')

# Page d'inscription
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
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

# Page de connexion
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirige vers la page d'accueil
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')

# Déconnexion
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

def portfolio_view(request):
    positions = Position.objects.all()
    data = []

    for pos in positions:
        stock = yf.Ticker(pos.ticker)
        try:
            #current_price = stock.info.get('currentPrice')
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
            'shares': pos.shares,
            'purchase_price': pos.purchase_price,
            'current_price': current_price,
            'total_value': total_value,
            'roi_value': roi_value,
            'roi_percent': roi_percent,
            'logo': pos.logo,
        })

    return render(request, 'portfolio.html', {'data': data})

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