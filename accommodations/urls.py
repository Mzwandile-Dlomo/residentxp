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

    path('complaint/', views.complaint_view, name='complaint'),

    path('log-visitor/', views.log_visitor_view, name='visitor'),

    path('maintainance-request/new/', views.maintainance_request_view, name='maintainance'),

    path('payment-method/', views.payment_method_view, name='payment_create'),


    path('inspections/<int:inspection_id>/', views.inspection_detail, name='inspection_detail'),

    path('activities/', views.activities, name='activities'),

    path('activities/social/', views.social_activities, name='social_activities'),
    path('activities/educational/', views.educational_activities, name='educational_activities'),
    path('activities/wellness/', views.wellness_activities, name='wellness_activities'),
]