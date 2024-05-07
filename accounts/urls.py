from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.apply_for_admission, name='register'),
    path('application_confirmation/', views.application_confirmation, name='application_confirmation'),
    path('application_exists/', views.application_exists, name='application_exists'),
    path('complete/<int:student_id>/', views.complete_application, name='complete_application'),
]