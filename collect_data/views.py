# views.py
import csv
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CSVUploadForm
from .models import MonthlyStat

ALLOWED_STAT_TYPES = {'adult_cko', 'children_cko', 'young_adult_cko', 'audiobook_cko', 
'dvd_cko', 'video_game_cko', 'magazine_cko', 'lot_cko', 'local_use_cko', 'ill_cko' }


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

            created, skipped = 0, 0
            for row_num, row in enumerate(reader, start=2):  # start=2 accounts for header line
                try:
                    stat_type_raw = row.get('stat_type', '').strip()
                    stat_type = stat_type_raw.lower()

                    if stat_type not in ALLOWED_STAT_TYPES:
                        messages.error(request, f"Row {row_num}: Invalid stat_type '{stat_type_raw}'. Allowed types: {', '.join(ALLOWED_STAT_TYPES)}.")
                        continue  # skip invalid rows

                    # Parse month, allowing YYYY-MM-DD or YYYY-MM formats:
                    try:
                        parsed_date = datetime.strptime(row['month'], '%Y-%m-%d')
                    except ValueError:
                        parsed_date = datetime.strptime(row['month'], '%Y-%m')
                    month = parsed_date.date().replace(day=1)

                    value = int(row['value'])

                    obj, created_obj = MonthlyStat.objects.get_or_create(
                        stat_type=stat_type,
                        month=month,
                        defaults={'value': value}
                    )

                    if created_obj:
                        created += 1
                    else:
                        skipped += 1

                except Exception as e:
                    messages.error(request, f"Row {row_num}: Error processing row {row} — {e}")

            messages.success(request, f"Upload complete. {created} new records, {skipped} skipped (duplicates).")
            return redirect('upload_csv')

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})
