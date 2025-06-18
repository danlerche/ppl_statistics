# forms.py
from django import forms
from .models import MonthYearStat, CirculationStat, HoldStat
from datetime import date

#this is for the model admin 
class MonthlyStatForm(forms.ModelForm):
    class Meta:
        model = MonthYearStat
        fields = ['month']
        widgets = {
            'month': forms.DateInput(attrs={
                'type': 'month',
                'placeholder': 'YYYY-MM-DD',
                'pattern': '[0-9]{4}-[0-9]{2}',
            }),
        }

    def clean_month(self):
        month = self.cleaned_data['month'].replace(day=1)

        if MonthYearStat.objects.filter(month=month).exists():
            raise forms.ValidationError("This month is already entered.")

        return month

#csv upload on a different page
class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Upload CSV file')