from accounts.models import CustomUser
from accommodations.models import Room, Building

def allocate_rooms_to_students(accepted_students):
    # Get a list of available rooms
    available_rooms = Room.objects.filter(occupants__isnull=True)

    for student in accepted_students:
        # Filter available rooms based on the student's gender and room preferences
        filtered_rooms = available_rooms.filter(
            building__gender_type=student.gender,
            room_type=student.preferred_room_type,
            # Add any other filtering criteria
        )

        # If suitable rooms are available, allocate a room to the student
        if filtered_rooms.exists():
            room = filtered_rooms.first()
            room.occupants.add(student)
            room.save()

            # Optionally, you can update the student's room information
            student.room = room
            student.save()

            # Remove the allocated room from the available_rooms list
            available_rooms = available_rooms.exclude(pk=room.pk)

    # Remaining students who couldn't be allocated a room
    unallocated_students = accepted_students.exclude(rooms__isnull=False)
    # Handle unallocated students based on your requirements
    # (e.g., send notifications, allocate remaining rooms, etc.)