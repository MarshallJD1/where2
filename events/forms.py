from django import forms
from .models import SavedEvent

UK_CITIES = [
    ("London", "London"),
    ("Manchester", "Manchester"),
    ("Birmingham", "Birmingham"),
    ("Liverpool", "Liverpool"),
    ("Leeds", "Leeds"),
    ("Glasgow", "Glasgow"),
    ("Edinburgh", "Edinburgh"),
    ("Bristol", "Bristol"),
    ("Cardiff", "Cardiff"),
    ("Newcastle", "Newcastle"),
    ("Sheffield", "Sheffield"),
    ("Nottingham", "Nottingham"),
]

class EventSearchForm(forms.Form):
    city = forms.ChoiceField(label="City", choices=UK_CITIES)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    radius = forms.IntegerField(label="Search Radius (miles)", min_value=1, max_value=100, initial=10)


class SavedEventForm(forms.ModelForm):
    class Meta:
        model = SavedEvent
        fields = ['event_id', 'name', 'date', 'venue', 'url', 'notes']
        widgets = {
            'event_id': forms.HiddenInput(),
            'name': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'venue': forms.HiddenInput(),
            'url': forms.HiddenInput(),
        }