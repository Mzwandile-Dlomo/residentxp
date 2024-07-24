from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date

CustomUser = get_user_model()  


# Create your models here.
class VisitorLog(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='visitor_logs')
    visitor_name = models.CharField(max_length=100)
    visitor_contact = models.CharField(max_length=10)
    visit_purpose = models.CharField(max_length=255)
    visit_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        room_numbers = [room.room_number for room in self.student.rooms.all()]
        room_info = ', '.join(room_numbers) if room_numbers else 'No Room Assigned'
        return f"Visitor: {self.visitor_name} for {self.student.first_name} {self.student.last_name} (Rooms: {room_info})"


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=False)
    allow_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title

class Choice(models.Model):
    survey = models.ForeignKey(Survey, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='votes', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

