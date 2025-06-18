# forms.py
from django import forms
from .models import MonthlyStat
from datetime import date

#this is for the model admin 
class MonthlyStatForm(forms.ModelForm):
    class Meta:
        model = MonthlyStat
        fields = '__all__'
        widgets = {
            'month': forms.DateInput(attrs={
                'type': 'month',
                'placeholder': 'YYYY-MM-DD',
                'pattern': '[0-9]{4}-[0-9]{2}',
            }),
        }

    def clean_month(self):
        """Normalize to the first of the month."""
        raw_date = self.cleaned_data['month']
        return date(raw_date.year, raw_date.month, 1)

    def clean(self):
        """Validate uniqueness of stat_type + month."""
        cleaned_data = super().clean()
        stat_type = cleaned_data.get('stat_type')
        month = cleaned_data.get('month')

        if stat_type and month:
            existing = MonthlyStat.objects.filter(stat_type=stat_type, month=month)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError(
                    f"A record for '{dict(self.fields['stat_type'].choices).get(stat_type)}' already exists for {month.strftime('%B %Y')}."
                )

        return cleaned_data

#csv upload on a different page
class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Upload CSV file')