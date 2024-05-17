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
    
    context = {
        'rooms': user_rooms,
        'rooms_with_occupants': rooms_with_occupants
    }
    print(rooms_with_occupants)
    return render(request, 'core/home.html', context)

