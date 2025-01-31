# Description: This file contains the form for the event search page.
from django import forms

class EventSearchForm(forms.Form):
    location = forms.CharField(max_length=100, label='Location')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Start Date')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='End Date')

