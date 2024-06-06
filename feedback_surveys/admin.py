from django.contrib import admin
from .models import Feedback, Survey, SurveyQuestion, SurveyResponse, SurveyAnswer


# Register your models here.
admin.site.register(Feedback)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(SurveyAnswer)
