
## form for search request 

from django import forms

class EventSearchForm(forms.Form):
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter location'}))
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

     def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Ensure end date is after the start date
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be later than start date.")
        
        return cleaned_data


