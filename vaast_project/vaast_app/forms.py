from django import forms
from .models import Experiment, Participant, Trial

class RegisterParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['extra_metadata']  # Add any additional fields as required

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subject_id = generate_unique_subject_id()  # Generate a unique Subject ID
        if commit:
            instance.save()
        return instance

def generate_unique_subject_id():
    """Generate a unique Subject ID."""
    import uuid
    return str(uuid.uuid4())[:8]  # Use a UUID or any unique ID generation method

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['name', 'description']

class RegisterParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['extra_metadata']

class TrialForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ['block_order', 'block_name', 'stimuli', 'valence', 'random_fixation', 'movement']