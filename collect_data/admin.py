from django.contrib import admin
from .models import MonthlyStat
# Register your models here.

@admin.register(MonthlyStat)
class MonthlyStatAdmin(admin.ModelAdmin):
    list_display = ('stat_type', 'year', 'month', 'value')
    list_filter = ('stat_type', 'year', 'month')
    search_fields = ('stat_type',)
    ordering = ('-year', '-month', 'stat_type')