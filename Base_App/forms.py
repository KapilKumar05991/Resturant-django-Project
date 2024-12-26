from django import forms
from .models import TableBooking

class TableBookingForm(forms.Form):
    class Meta:
        model = TableBooking
        fields = ['name', 'phone', 'persons', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }