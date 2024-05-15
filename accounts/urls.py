from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('', views.account_view, name='account'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),



    # Password Reset (using Django's built-in functionality)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   
   
   
   
    # path('', views.profile_view, name='profile'),
    # path('signup/', views.signup_view, name='signup'),
    # path('signup/additional/', views.additionalDetails_view, name='additional'),

    # path('login/', views.signin_view, name='login'),


    # path('update/', views.updateProfile_view, name='update'),


    # Sign In (Login)
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Sign Out (Logout)
    # path('logout/', views.logout_view, name='logout'),

    
    # # path('signup/', views.signup, name='signup'),
    # path('signin/', auth_views.LoginView.as_view(template_name='login.html'), name='signin'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),



    # path('application_error/', views.application_error_view, name='application_error'),


    # path('application_confirmation/', views.application_confirmation_view, name='application_confirmation'),
    # path('duplicate_application/', views.duplicate_application_view, name='duplicate_application'),
    # path('application_error/', views.application_error_view, name='application_error'),

]
