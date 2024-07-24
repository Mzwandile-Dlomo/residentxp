from django.urls import path
from . import views

app_name = 'residentlife'

urlpatterns = [
    path('activities/', views.activities, name='activities'),
    path('activities/social/', views.social_activities, name='social_activities'),
    path('activities/educational/', views.educational_activities, name='educational_activities'),
    path('activities/wellness/', views.wellness_activities, name='wellness_activities'),
    path('log-visitor/', views.log_visitor_view, name='visitor'),
    path('survey/', views.feedback_survey, name='feedback_survey'),
    path('close_survey/<int:survey_id>/', views.close_survey, name='close_survey'),
]
