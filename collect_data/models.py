from django.db import models
from datetime import date

class MonthlyStat(models.Model):
    STAT_CHOICES = [
        ('adult_cko', 'Adult Checkout'),
        ('children_cko', 'Children CKO'),
        ('young_adult_cko', 'Young Adult CKO'),
        ('audiobook_cko', 'Audiobook CKO'),
        ('dvd_cko', 'DVD CKO'),
        ('video_game_cko', 'Video Game CKO'),
        ('magazine_cko', 'Magazine CKO'),
        ('lot_cko', 'Library of Things CKO'),
        ('local_use_cko', 'Local Use CKO'),
        ('ill_cko', 'ILL CKO'),
    ]

    stat_type = models.CharField(max_length=50, choices=STAT_CHOICES)
    month = models.DateField()  # Use first of the month
    value = models.PositiveIntegerField()

    class Meta:
        unique_together = ('stat_type', 'month')
        ordering = ['-month', 'stat_type']

    def __str__(self):
        return f"{self.get_stat_type_display()} - {self.month.strftime('%B %Y')}: {self.value}" 