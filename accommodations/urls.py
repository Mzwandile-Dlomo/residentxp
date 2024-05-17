# accommodations/urls.py
from django.urls import path
from . import views

app_name = 'accommodations'

urlpatterns = [
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/<int:building_id>/', views.building_detail, name='building_detail'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('inspections/<int:inspection_id>/', views.inspection_detail, name='inspection_detail'),
]