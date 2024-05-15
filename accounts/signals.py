from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Room
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def set_user_permissions(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.email}, {instance.user_type}")
        if instance.user_type == 'admin':
            print("Setting superuser and staff permissions for admin")
            instance.is_superuser = True
            instance.is_staff = True
        elif instance.user_type == 'student_leader':
            print("Setting staff permissions for student leader")
            instance.is_staff = True
        instance.save()


@receiver(post_save, sender=CustomUser)
def allocate_room(sender, instance, created, **kwargs):
    if created and instance.user_type == 'student':
        available_rooms = Room.objects.filter(room_type=instance.room_type, is_full=False)
        if available_rooms.exists():
            room = available_rooms.first()
            room.occupants.add(instance)
            instance.room = room
            instance.save()