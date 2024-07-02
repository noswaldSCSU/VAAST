from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Experiment, Participant, Trial, Response
from .forms import ExperimentForm, RegisterParticipantForm, TrialForm
from django.views.decorators.csrf import csrf_exempt 
import random

# Participant Homepage Setup:
def home(request):
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        try:
            participant = Participant.objects.get(subject_id=participant_id)
            return redirect('show_instructions', participant_id=participant.id)
        except Participant.DoesNotExist:
            return render(request, 'home.html', {'error': 'Invalid Participant ID'})
    return render(request, 'home.html')

# Function to create sample trials
def create_sample_trials():
    if not Trial.objects.exists():
        trials_data = [
            {'block_order': 1, 'block_name': 'blkTestPosAp', 'stimuli': 'Happy', 'valence': 1, 'random_fixation': 800, 'movement': 1},
            {'block_order': 1, 'block_name': 'blkTestNegAv', 'stimuli': 'Sad', 'valence': 2, 'random_fixation': 800, 'movement': 2},
        ]
        for trial_data in trials_data:
            Trial.objects.create(**trial_data)

# Initialize trials if not already done
create_sample_trials()

# Starting the experiment
def start_experiment(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    trials = list(Trial.objects.all())
    random.shuffle(trials)
    request.session['participant_id'] = participant.id
    request.session['trials'] = [trial.id for trial in trials]
    request.session['current_trial_index'] = 0
    return redirect('run_trial')

# Running a trial
def run_trial(request):
    if 'current_trial_index' not in request.session:
        return redirect('home')
    current_trial_index = request.session['current_trial_index']
    trial_ids = request.session['trials']
    if current_trial_index >= len(trial_ids):
        return redirect('experiment_complete')
    trial = get_object_or_404(Trial, id=trial_ids[current_trial_index])
    return render(request, 'experiment.html', {'stimulus': trial.stimuli, 'trial_id': trial.id})

# Saving a response
@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        participant = get_object_or_404(Participant, id=request.session['participant_id'])
        current_trial_index = request.session['current_trial_index']
        trial_ids = request.session['trials']
        trial = get_object_or_404(Trial, id=trial_ids[current_trial_index])
        
        response_time = float(request.POST['response_time'])
        response_key = request.POST['response_key']
        
        correct_response = 'Y' if trial.valence == 1 else 'N'  # Example logic
        accuracy = 1 if response_key == correct_response else 0

        Response.objects.create(
            participant=participant,
            trial=trial,
            response_time=response_time,
            accuracy=accuracy
        )
        
        request.session['current_trial_index'] += 1
        return redirect('run_trial')

# Completing the experiment
def experiment_complete(request):
    participant_id = request.session['participant_id']
    participant = get_object_or_404(Participant, id=participant_id)
    responses = Response.objects.filter(participant=participant)
    return render(request, 'experiment_complete.html', {'responses': responses})

# Registering Participant
def register_participant(request):
    if request.method == 'POST':
        form = RegisterParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return redirect('participant_success', subject_id=participant.subject_id)
    else:
        form = RegisterParticipantForm()
    return render(request, 'register_participant.html', {'form': form})

def participant_success(request, subject_id):
    return render(request, 'participant_success.html', {'subject_id': subject_id})

def manage_participants(request):
    participants = Participant.objects.all()
    return render(request, 'manage_participants.html', {'participants': participants})

def participant_detail(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    return render(request, 'participant_detail.html', {'participant': participant})

def edit_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    if request.method == 'POST':
        form = RegisterParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_detail', participant_id=participant.subject_id)
    else:
        form = RegisterParticipantForm(instance=participant)
    return render(request, 'edit_participant.html', {'form': form})

def delete_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    if request.method == 'POST':
        participant.delete()
        return redirect('manage_participants')
    return render(request, 'delete_participant.html', {'participant': participant})

# Instructions for Experiment
def show_instructions(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        return redirect('start_experiment', participant_id=participant_id)
    return render(request, 'instructions.html', {'participant': participant})

# Researcher Dashboard
def researcher_dashboard(request):
    experiments = Experiment.objects.all()
    return render(request, 'researcher_dashboard.html', {'experiments': experiments})

def create_experiment(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('researcher_dashboard')
    else:
        form = ExperimentForm()
    return render(request, 'create_experiment.html', {'form': form})

def list_participants(request):
    participants = Participant.objects.all()
    return render(request, 'list_participants.html', {'participants': participants})

def list_responses(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    responses = Response.objects.filter(participant=participant)
    return render(request, 'list_responses.html', {'participant': participant, 'responses': responses})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('researcher_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def researcher_dashboard(request):
    experiments = Experiment.objects.all()
    return render(request, 'researcher_dashboard.html', {'experiments': experiments})

@login_required
def create_experiment(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('researcher_dashboard')
    else:
        form = ExperimentForm()
    return render(request, 'create_experiment.html', {'form': form})

@login_required
def list_participants(request):
    participants = Participant.objects.all()
    return render(request, 'list_participants.html', {'participants': participants})

@login_required
def list_responses(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    responses = Response.objects.filter(participant=participant)
    return render(request, 'list_responses.html', {'participant': participant, 'responses': responses})