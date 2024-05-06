from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.apply_for_admission, name='register'),
]