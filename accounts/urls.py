from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.apply_view, name='application'),
    path('application_confirmation/', views.application_confirmation, name='application_confirmation'),
    path('duplicate_application/', views.duplicate_application, name='duplicate_application'),
    path('application_error/', views.application_error, name='application_error'),
    path('complete_application/<int:student_id>/', views.complete_application, name='complete_application'),
]
# application_error