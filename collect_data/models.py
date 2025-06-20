from django.db import models
from datetime import date

class MonthYearStat(models.Model):
    month = models.DateField() 

    def __str__(self):
        return self.month.strftime('%Y-%m-%d')


class CirculationStat(models.Model):
    month = models.ForeignKey(MonthYearStat, on_delete=models.CASCADE)
    STAT_CHOICES = [
        ('adult', 'Adult'),
        ('children', 'Children'),
        ('young_adult', 'Young Adult'),
        ('audiobook', 'Audiobook'),
        ('dvd', 'DVD'),
        ('video_game', 'Video Game'),
        ('magazine', 'Magazine'),
        ('lot', 'Library of Things'),
        ('local_use', 'Local Use'),
        ('ill', 'ILL'),
        ('other', 'Other'),
    ]

    circ_stat_type = models.CharField(max_length=50, choices=STAT_CHOICES)
    checkouts = models.PositiveIntegerField()
    renewals = models.PositiveIntegerField()

    class Meta:
        unique_together = ('month', 'circ_stat_type')  # prevent duplicates
        ordering = ['circ_stat_type']

    def __str__(self):
        return self.circ_stat_type

class HoldStat(models.Model):
    month = models.ForeignKey(MonthYearStat, on_delete=models.CASCADE)
    holds_placed = models.PositiveIntegerField()
    holds_fulfilled = models.PositiveIntegerField()
    holds_cko = models.PositiveIntegerField()