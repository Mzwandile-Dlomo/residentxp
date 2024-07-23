# accommodations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Building, Room, RoomInspectionRequest, MaintenanceRequest, RoomReservation, Complaint, Survey, Choice, Vote
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RoomReservationForm, ComplaintForm, VisitorLogForm, MaintenanceRequestForm, PaymentMethodForm
from django.contrib import messages


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
        # Get the inspection date and type from the form data
        inspection_date = request.POST.get('inspection_date')
        inspection_type = request.POST.get('inspection_type')

        # Create a new inspection request with the selected date and type
        inspection_request = RoomInspectionRequest.objects.create(
            room=room,
            requested_by=request.user,
            type=inspection_type,
            inspection_date=inspection_date
        )
        inspection_request.save()

        # Redirect back to the room detail page or another appropriate page
        return redirect('accommodations:room_detail', room_id=room.id)
    

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
def complaint_view(request):

    user_complaints = Complaint.objects.filter(requested_by=request.user)
    complaints = []

    for complaint in user_complaints:
        complaints.append(complaint)
    

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.requested_by = request.user
            complaint.save()
            messages.success(request, 'Complaint submitted!')
            return redirect('core:home')
    else:
        form = ComplaintForm()

    context = {'form': form, 'complaints': complaints}
    return render(request, 'accommodations/complaint.html', context)


@login_required
def log_visitor_view(request):
    visitors_list = []

    if request.method == 'POST':
        form = VisitorLogForm(request.POST)
        if form.is_valid():
            visitor_log = form.save(commit=False)
            visitor_log.student = request.user
            visitor_log.save()
            messages.success(request, 'Visitor logged successfully!')
            return redirect('core:home')
    else:
        form = VisitorLogForm()
    
    visitor_logs = request.user.visitor_logs.all()  # Get all visitor logs for the current user

    for visitor in visitor_logs:
        visitors_list.append(visitor)

    context = {
        'form': form,
        'visitor_logs': visitors_list
    }
    return render(request, 'accommodations/visitor.html', context)


def maintainance_request_view(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)

        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.requested_by = request.user
            maintenance_request.save()
            messages.success(request, "Maintainance submitted!")
            return redirect('core:home')
        else:
            messages.error(request, "Please fill out the maintenance request form below.")
    else:
        form = MaintenanceRequestForm()
    return render(request, 'accommodations/maintainance.html', {'form': form})


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




def activities(request):
    return render(request, 'accommodations/resident_activities.html')

def social_activities(request):
    return render(request, 'accommodations/social_activities.html')

def educational_activities(request):
    return render(request, 'accommodations/educational_activities.html')

def wellness_activities(request):
    return render(request, 'accommodations/wellness_activities.html')


def feedback_survey(request):
    current_survey = Survey.objects.filter(active=True).first()
    survey_history = Survey.objects.filter(active=False).order_by('-created_at')
    if request.method == 'POST' and current_survey:
        choice_id = request.POST.get('choice')
        choice = Choice.objects.get(id=choice_id)
        Vote.objects.create(choice=choice)
        return redirect('feedback_survey')
    return render(request, 'accommodations/feedback_survey.html', {
        'current_survey': current_survey,
        'survey_history': survey_history,
    })



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
