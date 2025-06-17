# admin.py
from django.contrib import admin
from .models import MonthlyStat
from .forms import MonthlyStatForm
from django.contrib.admin import DateFieldListFilter

@admin.register(MonthlyStat)
class MonthlyStatAdmin(admin.ModelAdmin):
    form = MonthlyStatForm  # <-- Attach the form here
    list_display = ('stat_type', 'formatted_month', 'value')
    list_filter = (
        'stat_type',
        ('month', DateFieldListFilter),
    )
    ordering = ('-month', 'stat_type')

    def formatted_month(self, obj):
        return obj.month.strftime('%B %Y')
    formatted_month.short_description = 'Month'