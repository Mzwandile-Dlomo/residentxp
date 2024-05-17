# accommodations/views.py
from django.shortcuts import render, get_object_or_404
from .models import Building, Room, RoomInspection, MaintenanceRequest
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
@login_required
def room_detail(request, room_id):
    user = request.user
    room = get_object_or_404(Room, pk=room_id)
    inspections_object = room.roominspection_set.all()
    rooms_object = user.rooms.all()
    rooms_with_occupants = {}
    room_occupants = []
    inspections = []

    for inspection in inspections_object:
        inspections.append(inspection)
    
    for room in rooms_object:
        occupants = room.occupants.all()
        rooms_with_occupants[room] = occupants


    for room, occupants in rooms_with_occupants.items():
        if occupants.exists():
            for occupant in occupants:
                room_occupants.append(occupant)

    
    return render(request, 'accommodations/room_detail.html', {'room': room, 'inspections': inspections, 'room_occupants': room_occupants})


@staff_member_required
def inspection_detail(request, inspection_id):
    inspection = get_object_or_404(RoomInspection, pk=inspection_id)
    return render(request, 'accommodations/inspection_detail.html', {'inspection': inspection})

@staff_member_required
def building_list(request):
    buildings = Building.objects.all()
    return render(request, 'accommodations/building_list.html', {'buildings': buildings})

@staff_member_required
def building_detail(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    rooms = building.room_set.all()
    return render(request, 'accommodations/building_detail.html', {'building': building, 'rooms': rooms})
