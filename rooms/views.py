from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Building, Room  # Assuming your models are here


# Create your views here.
# Room views
@login_required  # Restricts to logged-in users (students and staff)
def room_detail_view(request, room_number):
    # room = get_object_or_404(Room, id=room_id)
    room = get_object_or_404(Room, room_number=room_number)
    roommates = room.occupants.all()
    return render(request, 'rooms/room_detail.html', {
        'room': room,
        'roommates': roommates,
        # 'items': room.items.all(),
    })


@staff_member_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


@login_required
def room_furniture(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # Logic to retrieve furniture details for the room
    furniture_list = []# Your logic to get furniture detail
    context = {'room': room, 'furniture_list': furniture_list}
    return render(request, 'rooms/room_furniture.html', context)


@login_required
def report_brokage_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        # # Logic to process the report form and potentially create a complaint object
        # furniture_id = request.POST.get('furniture_id')
        # description = request.POST.get('description')
        # furniture = get_object_or_404(Furniture, id=furniture_id)
        # complaint = Complaint.objects.create(
        #     room=room,
        #     furniture=furniture,
        #     description=description,
        #     reported_by=request.user
        # )
        return redirect('success_url')  # Replace with appropriate URL name
    context = {'room': room}
    return render(request, 'rooms/report_brokage.html', context)


# Building views
@staff_member_required  # Restricts to staff (student leader/admin)
def building_list(request):
    buildings = Building.objects.all()
    return render(request, 'buildings/building_list.html', {'buildings': buildings})


@staff_member_required
def building_detail(request, pk):
    building = get_object_or_404(Building, pk=pk)
    return render(request, 'buildings/building_detail.html', {'building': building})


@login_required
def room_inspection_view(request, inspection_id):
    pass
