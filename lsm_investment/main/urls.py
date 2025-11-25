from django.urls import path, include, reverse_lazy
from . import views
from .views import portfolio_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('update-password/', views.update_password_view, name='update_password'),
    path('portfolio/', portfolio_view, name='portfolio'),
    path('performance/', views.performance_view, name='performance'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('confirm-delete/', views.confirm_delete_view, name='confirm_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)