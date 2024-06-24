from django.shortcuts import render
from django.conf import settings
import pandas as pd
import os
import pygwalker as pyg
import subprocess

def analysis(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        file_path = os.path.join(settings.MEDIA_ROOT, csv_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        subprocess.run(['python', 'script.py', file_path])

        df = pd.read_csv(file_path)

        walker_html = pyg.walk(df).to_html()
        return render(request, 'pygwalker_report.html', {'walker_html': walker_html})
    

    return render(request, 'analysis.html')
