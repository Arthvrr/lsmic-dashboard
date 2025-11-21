from django.urls import path, include
from . import views
from .views import portfolio_view

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('update-password/', views.update_password_view, name='update_password'),
    path('portfolio/', portfolio_view, name='portfolio'),
]