from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ComplaintForm, MaintenanceRequestForm
from .models import Complaint
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
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
    return render(request, 'complains_maintenance/complain.html', context)

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
    return render(request, 'complains_maintenance/maintainance.html', {'form': form})
