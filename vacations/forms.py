from django import forms
from .models import Vacation, VacationEvent

class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ['name', 'start_date', 'end_date']

class AddEventToVacationForm(forms.Form):
    vacation = forms.ModelChoiceField(queryset=Vacation.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vacation'].queryset = Vacation.objects.filter(user=user)