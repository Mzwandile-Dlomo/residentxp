from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomInspection, RoomItem
from .forms import RoomAssignmentForm, RoomInspectionRequestForm, RoomInspectionForm, RoomItemForm
from accounts.models import CustomUser

@login_required
def room_assignment_view(request):
    if request.method == 'POST':
        form = RoomAssignmentForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            student = request.user
            room.occupants.add(student)
            # Additional logic if needed
            return redirect('residences:room_detail', room_id=room.id)
    else:
        form = RoomAssignmentForm(user=request.user)
    return render(request, 'residences/room_assignment.html', {'form': form})

@login_required
def room_inspection_request_view(request):
    if request.method == 'POST':
        form = RoomInspectionRequestForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            # Additional logic for creating a room inspection request
            return redirect('residences:room_detail', room_id=room.id)
    else:
        form = RoomInspectionRequestForm(user=request.user)
    return render(request, 'residences/room_inspection_request.html', {'form': form})

@login_required
def room_inspection_view(request, inspection_id):
    inspection = get_object_or_404(RoomInspection, id=inspection_id)
    if request.method == 'POST':
        form = RoomInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            # Additional logic if needed
            return redirect('residences:room_detail', room_id=inspection.room.id)
    else:
        form = RoomInspectionForm(instance=inspection)
    return render(request, 'residences/room_inspection.html', {'form': form, 'inspection': inspection})

@login_required
def room_item_management_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomItemForm(request.POST)
        if form.is_valid():
            room_item = form.save()
            room.items.add(room_item)
            # Additional logic if needed
            return redirect('residences:room_detail', room_id=room.id)
    else:
        form = RoomItemForm()
    return render(request, 'residences/room_item_management.html', {'form': form, 'room': room})


@login_required
def room_detail_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    roommates = room.occupants.exclude(pk=request.user.pk)  # Exclude the current user
    return render(request, 'residences/room_detail.html', {
        'room': room,
        'roommates': roommates,
        'items': room.items.all(),
    })