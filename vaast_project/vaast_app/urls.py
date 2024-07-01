from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    home, register_participant, participant_success, manage_participants,
    participant_detail, edit_participant, delete_participant, show_instructions,
    start_experiment, run_trial, save_response, experiment_complete, 
    researcher_dashboard, create_experiment, list_participants, list_responses, login_view, logout_view
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_participant, name='register_participant'),
    path('success/<str:subject_id>/', participant_success, name='participant_success'),
    path('manage/', manage_participants, name='manage_participants'),
    path('detail/<int:participant_id>/', participant_detail, name='participant_detail'),
    path('edit/<int:participant_id>/', edit_participant, name='edit_participant'),
    path('delete/<int:participant_id>/', delete_participant, name='delete_participant'),
    path('instructions/<int:participant_id>/', show_instructions, name='show_instructions'),
    path('start-experiment/<int:participant_id>/', start_experiment, name='start_experiment'),
    path('run-trial/', run_trial, name='run_trial'),
    path('save-response/', save_response, name='save_response'),
    path('experiment-complete/', experiment_complete, name='experiment_complete'),
    path('researcher/', researcher_dashboard, name='researcher_dashboard'),
    path('researcher/create/', create_experiment, name='create_experiment'),
    path('researcher/participants/', list_participants, name='list_participants'),
    path('researcher/responses/<int:participant_id>/', list_responses, name='list_responses'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]