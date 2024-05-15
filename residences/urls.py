from django.urls import path
from . import views

app_name = 'residences'

urlpatterns = [
    path('room-assignment/', views.room_assignment_view, name='room_assignment'),
    path('room-inspection-request/', views.room_inspection_request_view, name='room_inspection_request'),
    path('room-inspection/<int:inspection_id>/', views.room_inspection_view, name='room_inspection'),
    path('room/<int:room_id>/item-management/', views.room_item_management_view, name='room_item_management'),
    path('room/<int:room_id>/details/', views.room_detail_view, name='room_detail'),  # New view for room details

]