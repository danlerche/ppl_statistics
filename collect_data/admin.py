# admin.py
from django.contrib import admin
from .models import MonthYearStat, CirculationStat, HoldStat
from .forms import MonthlyStatForm
from django.contrib.admin import DateFieldListFilter

@admin.register(MonthYearStat)
class MonthYearStatAdmin(admin.ModelAdmin):
    form = MonthlyStatForm
    list_filter = (
        'month',
        )

    def formatted_month(self, obj):
        return obj.month.strftime('%B %Y')
    formatted_month.short_description = 'Month'

@admin.register(CirculationStat)
class CirculationStatAdmin(admin.ModelAdmin):
    list_display = ('month', 'circ_stat_type', 'circ_value', 'renewal_value')
    list_filter = (
        'circ_stat_type',
        'month',
    )
    ordering = ('-month', 'circ_stat_type')

@admin.register(HoldStat)
class HoldStatAdmin(admin.ModelAdmin):
    list_display = ('holds_placed', 'holds_fulfilled', 'holds_cko')
    list_filter = (
        'month',
        'holds_placed',
        'holds_fulfilled',
        'holds_cko',
    )
