from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('account/', views.account_view, name='account'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),        
    path('update', views.update_view, name='update'),

    path('account/lease-agreement/create/', views.lease_agreement_view, name='lease_agreement'),


    path('account/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('account/rental-agreement/<int:pk>/update/', views.RentalAgreementUpdateView.as_view(), name='rental_agreement_update'),
    path('account/rental-agreement/create/', views.RentalAgreementCreateView.as_view(), name='rental_agreement'),
    path('account/payment/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment_update'),
    path('account/payment/create/', views.PaymentCreateView.as_view(), name='payment_create'),



    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/comp`lete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
