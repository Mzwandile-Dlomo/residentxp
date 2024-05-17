from django.urls import path

from . import views

app_name = 'rooms'


urlpatterns = [
    path('room/<int:pk>/', views.room_detail_view, name='room_detail'),  # Details of a specific room, # for Student, Student Leader. User side



    
    path('buildings/', views.building_list, name='building_list'),  # List of all buildings, # only for Student leaders and admin only
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),  # Details of a specific building, # only for Student leaders and admin only
    path('rooms/', views.room_list, name='room_list'),  # List of all rooms, # only for Student leaders and admin only
    path('buildings/', views.building_list, name='building_list'),  # List of all buildings, # 
    # path('rooms/<int:pk>/furniture/', views.room_furniture, name='room_furniture'),  # Furniture details for a room, # only for Student leaders and admin only
    # path('rooms/<int:pk>/report-brokage/', views.report_brokage, name='room_furniture'),  # Furniture details for a room, # for Student, Student Leader. User side
]
