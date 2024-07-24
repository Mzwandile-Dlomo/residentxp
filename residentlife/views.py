from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import VisitorLogForm
from .models import Survey, Vote, Choice


# Create your views here.
def activities(request):
    return render(request, 'residentlife/resident_activities.html')

def social_activities(request):
    return render(request, 'residentlife/social_activities.html')

def educational_activities(request):
    return render(request, 'residentlife/educational_activities.html')

def wellness_activities(request):
    return render(request, 'residentlife/wellness_activities.html')

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
    return render(request, 'residentlife/visitor.html', context)


@login_required
def feedback_survey(request):
    current_survey = Survey.objects.filter(active=True).first()
    survey_history = Survey.objects.filter(active=False).order_by('-closed_at')
    user_vote = None

    if current_survey:
        user_vote = Vote.objects.filter(user=request.user, choice__survey=current_survey).first()

    if request.method == 'POST':
        if 'title' in request.POST:  # Creating a new survey
            title = request.POST['title']
            description = request.POST['description']
            choices = request.POST['choices'].split('\n')
            allow_update = 'allow_update' in request.POST

            if current_survey:
                current_survey.active = False
                current_survey.closed_at = timezone.now()
                current_survey.save()

            new_survey = Survey.objects.create(title=title, description=description, active=True, allow_update=allow_update)
            for choice_text in choices:
                Choice.objects.create(survey=new_survey, text=choice_text.strip())

        elif 'choice' in request.POST:  # Voting
            choice_id = request.POST['choice']
            choice = get_object_or_404(Choice, id=choice_id)
            
            if user_vote and current_survey.allow_update:
                user_vote.choice = choice
                user_vote.save()
            elif not user_vote:
                Vote.objects.create(choice=choice, user=request.user)

        return redirect('residentlife:feedback_survey')

    context = {
        'current_survey': current_survey,
        'survey_history': survey_history,
        'user_vote': user_vote,
    }
    return render(request, 'residentlife/feedback_survey.html', context)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def close_survey(request, survey_id):
    if request.method == 'POST':
        survey = get_object_or_404(Survey, id=survey_id)
        survey.active = False
        survey.closed_at = timezone.now()
        survey.save()
    return redirect('residentlife:feedback_survey')
