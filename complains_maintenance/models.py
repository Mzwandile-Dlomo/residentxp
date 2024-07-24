from django.db import models
from django.contrib.auth import get_user_model
from accommodations.models import Room


CustomUser = get_user_model()  

# Create your models here.
class Complaint(models.Model):
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=100)
    description = models.TextField()
    CATEGORY_CHOICES = (
        ('noise', 'Noise'),
        ('maintenance', 'Maintenance'),
        ('safety', 'Safety'),
        # Add more categories as needed
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Complaint: {self.title} by {self.requested_by.email}"


class MaintenanceRequest(models.Model):
    requested_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='maintenance_requests')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_requests')

    LOCATION_CHOICES = (
        ('room', 'Room'),
        ('laundry_room', 'Laundry Room'),
        ('tv_room', 'TV Room'),
        ('stairs', 'Stairs'),
        # Add more common areas as needed
    )
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='')
    description = models.TextField()
    URGENCY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='high')
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
    )
    
    picture = models.ImageField(upload_to='maintenance_requests', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance_requests')
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.location == 'room':
            return f"Maintenance Request: {self.description} in {self.room} by {self.requested_by.email}"
        else:
            return f"Maintenance Request: {self.description} in {self.location} by {self.requested_by.email}"

