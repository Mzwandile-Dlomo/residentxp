# core/views
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 


# Create your views here.
@login_required
def home_view(request):
    user = request.user
    user_rooms = user.rooms.all()
    rooms_with_occupants = {}

    for room in user_rooms:
        occupants = room.occupants.all()  # Fetch all occupants for the room
        rooms_with_occupants[room] = occupants
    
    # Print rooms with occupants
    # print(rooms_with_occupants)

    room_occupants = []
    # Check if there are any rooms with occupants
    if rooms_with_occupants:
        # Example of accessing the first room and its occupants
        first_room = next(iter(rooms_with_occupants))
        first_occupants = rooms_with_occupants[first_room]
        
        # If occupants exist, get the first occupant
        if first_occupants.exists():
            custom_user = first_occupants.first()
            room_occupants.append(custom_user)
            # print(custom_user)

    context = {
        'rooms': user_rooms,
        'room_occupants': room_occupants,
        'rooms_with_occupants': rooms_with_occupants
    }

    return render(request, 'core/home.html', context)

# def home_view(request):
#     user = request.user
#     user_rooms = user.rooms.all()
#     rooms_with_occupants = {}

#     for room in user_rooms:
#         occupants = room.occupants.all()  # Fetch all occupants for the room
#         rooms_with_occupants[room] = occupants
    
#     context = {
#         'rooms': user_rooms,
#         'rooms_with_occupants': rooms_with_occupants
#     }
#     print(rooms_with_occupants)

#     if rooms_with_occupants.exists():
#         custom_user = rooms_with_occupants.first()
#         print(custom_user)
    
    
#     return render(request, 'core/home.html', context)

