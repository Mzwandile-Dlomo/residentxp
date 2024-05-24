from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentAllocation, RoomReservation, LeaseAgreement

@receiver(post_save, sender=RoomReservation)
def create_rental_agreement(sender, instance, created, **kwargs):
    if created and instance.status == 'approved':
        LeaseAgreement.objects.create(
            student=instance.student,
            # Populate other fields as needed
        )


@receiver(post_save, sender=StudentAllocation)
def update_room_occupants(sender, instance, **kwargs):
    instance.room.occupants.add(instance.student)
