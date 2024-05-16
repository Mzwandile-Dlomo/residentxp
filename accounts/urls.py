from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('', views.account_view, name='account'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),        
    path('update', views.update_view, name='update'),

    # Password Reset (using Django's built-in functionality)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
