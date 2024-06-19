# csv_analyzer/views.py
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from ydata_profiling import ProfileReport
import pandas as pd
import glob

def analyse_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/Reports')
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = fs.url(filename)

        # Read CSV file
        df = pd.read_csv(fs.path(filename))

        # Generate profiling report
        profile = ProfileReport(df, title="Profiling Report")
        profile_html = profile.to_html()

        # Save HTML report
        report_name = os.path.splitext(filename)[0] + '.html'
        report_path = os.path.join(settings.MEDIA_ROOT, 'Reports', report_name)
        with open(report_path, 'w') as report_file:
            report_file.write(profile_html)

        return redirect('report_list')  # Redirect to list of reports after analysis

    return render(request, 'csv_analyzer/analyse_csv.html')


def report_list(request):
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'Reports')
    report_files = glob.glob(os.path.join(reports_dir, '*.html'))
    report_names = [os.path.splitext(os.path.basename(f))[0] for f in report_files]
    
    return render(request, 'csv_analyzer/report_list.html', {
        'report_names': report_names,
    })


def view_report(request, report_name):
    report_path = os.path.join(settings.MEDIA_ROOT, 'Reports', report_name + '.html')
    
    try:
        with open(report_path, 'r') as report_file:
            report_html = report_file.read()
    except FileNotFoundError:
        report_html = f"Report '{report_name}' not found."

    return render(request, 'csv_analyzer/view_report.html', {
        'report_name': report_name,
        'report_html': report_html,
    })
