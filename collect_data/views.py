import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CSVUploadForm
from .models import MonthYearStat, CirculationStat

ALLOWED_STAT_TYPES = {key for key, _ in CirculationStat.STAT_CHOICES}

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def upload_csv_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            decoded_file = uploaded_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            created, updated = 0, 0

            for row_num, row in enumerate(reader, start=2):
                try:
                    raw_date = row['date'].strip()
                    stat_type = row['circ_stat_type'].strip().lower()
                    circ_value = int(row['circ_value'])
                    renewal_value = int(row['renewal_value'])

                    # Normalize date to first of the month
                    parsed_date = datetime.strptime(raw_date, '%Y-%m-%d').date()
                    normalized_date = parsed_date.replace(day=1)

                    if stat_type not in ALLOWED_STAT_TYPES:
                        messages.error(request, f"Row {row_num}: Invalid stat type '{stat_type}'")
                        continue

                    # Create/reuse month object
                    month_obj, _ = MonthYearStat.objects.get_or_create(month=normalized_date)

                    # Insert or update the stat
                    obj, created_flag = CirculationStat.objects.update_or_create(
                        month=month_obj,
                        circ_stat_type=stat_type,
                        defaults={
                            'circ_value': circ_value,
                            'renewal_value': renewal_value
                        }
                    )

                    if created_flag:
                        created += 1
                    else:
                        updated += 1

                except Exception as e:
                    messages.error(request, f"Row {row_num}: Error processing row {row} — {e}")

            messages.success(request, f"Upload complete. {created} created, {updated} updated.")
            return redirect('upload_csv')

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})