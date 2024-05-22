# accommodations/urls.py
from django.urls import path
from . import views

app_name = 'accommodations'

urlpatterns = [
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/<int:building_id>/', views.building_detail, name='building_detail'),
    path('rooms/room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/room/<int:room_id>/request_inspection/', views.request_inspection, name='request_inspection'),
    path('room-reservation/', views.room_reservation_view, name='room_reservation'),

    path('inspections/<int:inspection_id>/', views.inspection_detail, name='inspection_detail'),
]