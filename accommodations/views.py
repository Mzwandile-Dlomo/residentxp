# accommodations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Building, Room, RoomInspectionRequest, RoomInspectionReport, RoomReservation
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RoomReservationForm, PaymentMethodForm, InspectionRequestFormManagement
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone



# Create your views here.
@login_required
def room_detail(request, room_id):
    user = request.user
    room = get_object_or_404(Room, pk=room_id)
    inspections_object = room.inspection_requests.all()
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


def request_inspection(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        inspection_date = request.POST.get('inspection_date')
        inspection_type = request.POST.get('inspection_type')

        inspection_request = RoomInspectionRequest.objects.create(
            room=room,
            requested_by=request.user,
            type=inspection_type,
            inspection_date=inspection_date
        )
        inspection_request.save()

        return redirect('accommodations:room_detail', room_id=room.id)
    return render(request, 'accommodations/request_inspection.html', {'room': room})


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def inspection_requests_list(request):
    inspection_requests = RoomInspectionRequest.objects.all().order_by('-requested_at')
    return render(request, 'accommodations/inspection_requests.html', {'inspection_requests': inspection_requests})


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def inspection_request_management(request, request_id):
    inspection_request = get_object_or_404(RoomInspectionRequest, pk=request_id)
    
    if request.method == 'POST':
        form = InspectionRequestFormManagement(request.POST, instance=inspection_request)
        if form.is_valid():
            form.save()
            
            # Create an inspection report if marking as done
            if inspection_request.status == 'Done' and not RoomInspectionReport.objects.filter(inspection_request=inspection_request).exists():
                RoomInspectionReport.objects.create(
                    inspection_request=inspection_request,
                    inspector=request.user,
                    report_details=request.POST.get('report_details', '')
                )
            
            return redirect('accommodations:inspection_requests_list')
    else:
        form = InspectionRequestFormManagement(instance=inspection_request)
    
    return render(request, 'accommodations/inspection_request_management.html', {'form': form, 'inspection_request': inspection_request})


@login_required
def room_reservation_view(request):
    ensuite_rooms = Room.objects.filter(room_type__in=['single_ensuite', 'double_ensuite'])

    if request.method == 'POST':
        form = RoomReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.student = request.user
            reservation.save()
            messages.success(request, 'Room reservation submitted successfully!')
            return redirect('core:home')
    else:
        form = RoomReservationForm(user=request.user)

    context = {'form': form, 'rooms': ensuite_rooms}
    return render(request, 'accommodations/room_reservation.html', context)


@login_required
def payment_method_view(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.rental_agreement = request.user.rental_agreements.first()
            payment.user = request.user
            payment.save()
            return redirect('success_url')
    else:
        form = PaymentMethodForm()

    return render(request, 'payment_method.html', {'form': form})



# --------------------------------------------------------------------------------------------------------

@staff_member_required
def inspection_detail(request, inspection_id):
    inspection = get_object_or_404(RoomInspectionRequest, pk=inspection_id)
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
