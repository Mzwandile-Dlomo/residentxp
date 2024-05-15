from django.urls import path

from . import views

urlpatterns = [
    path('buildings/', views.building_list, name='building_list'),  # List of all buildings, # only for Student leaders and admin only
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),  # Details of a specific building, # only for Student leaders and admin only
    path('rooms/', views.room_list, name='room_list'),  # List of all rooms, # only for Student leaders and admin only
    path('rooms/<int:pk>/', views.room_detail_view, name='room_detail'),  # Details of a specific room, # for Student, Student Leader. User side
    path('rooms/<int:pk>/furniture/', views.room_furniture, name='room_furniture'),  # Furniture details for a room, # only for Student leaders and admin only
    path('rooms/<int:pk>/report-brokage/', views.report_brokage, name='room_furniture'),  # Furniture details for a room, # for Student, Student Leader. User side

    # path('complaints/create/', views.complaint_create, name='complaint_create'),  # Create a complaint, # for Student, Student Leader. User side
    # path('complaints/', views.complaint_list, name='complaint_list'),  # List of all complaints (for student leader/admin)
    # path('complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),  # View a specific complaint detail (for student leader/admin)
    # path('complaints/<int:pk>/update/', views.complaint_update, name='complaint_update'),  # Update a complaint status (for student leader/admin)
]
