from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Building, Room  # Assuming your models are here


# Create your views here.
@staff_member_required  # Restricts to staff (student leader/admin)
def building_list(request):
    buildings = Building.objects.all()
    context = {'buildings': buildings}
    return render(request, 'rooms/building_list.html', context)

@staff_member_required
def building_detail(request, pk):
    building = get_object_or_404(Building, pk=pk)
    context = {'building': building}
    return render(request, 'rooms/building_detail.html', context)

@staff_member_required
def room_list(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'rooms/room_list.html', context)

@login_required  # Restricts to logged-in users (students and staff)
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # Check if user is student or staff for roommate details
    roommate_details = None
    if request.user.user_type == 'student' and room.capacity > 1:
        # Logic to retrieve roommate details based on your model structure (StudentRoom or occupants field)
        roommate_details = []# Your logic to get roommate details
    context = {'room': room, 'roommate_details': roommate_details}
    return render(request, 'rooms/room_detail.html', context)

@login_required
def room_furniture(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # Logic to retrieve furniture details for the room
    furniture_list = []# Your logic to get furniture detail
    context = {'room': room, 'furniture_list': furniture_list}
    return render(request, 'rooms/room_furniture.html', context)

@login_required
def report_brokage(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # Handle form submission for reporting broken furniture
    if request.method == 'POST':
        # Logic to process the report form and potentially create a complaint object
        return redirect('success_url')  # Replace with appropriate redirect after successful report
    context = {'room': room}
    return render(request, 'rooms/report_brokage.html', context)
