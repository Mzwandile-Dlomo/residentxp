from django.urls import path
from . import views


app_name = 'complains_maintenance'

urlpatterns = [
    path('complaint/', views.complaint_view, name='complaint'),
    path('maintainance-request/new/', views.maintainance_request_view, name='maintainance'),
    
]