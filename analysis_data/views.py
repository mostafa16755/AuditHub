from django.shortcuts import render
import pandas as pd
# from pandas_profiling import ProfileReport
import os
from django.http import FileResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
# from pydantic_settings import BaseSettings
from pandasgui import show
# from dataprep.datasets import load_dataset
# from dataprep.eda import create_report
from ydata_profiling import ProfileReport
from .models import CSV



def CSVdisplaying(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
# >>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
        # model=csv(csv=file)
        # model = CSV.objects.create(csv_file=file)  # Create a new instance of the CSV model
        # model.save()
        dictionary_path = "C:\\Users\\dinas\\OneDrive\\Desktop\\analysis project\\analysis_dashboard\\analysis_dashboard"
        fs = FileSystemStorage(location=dictionary_path)  # Specify the folder where the file will be saved
        filename = fs.save(file.name, file)
        # model.csv=filename
        # model.save()

        file_url = fs.url(filename)
        file_path = os.path.join(dictionary_path, filename)
        

        if 'overview' in request.POST:
            return analyse_data2(request,file_path)
        elif "Details" in request.POST:
            return analyse_data(request, file_path)
        # else:
        #    return csv_data(request)


            
            

    return render(request, "analysis_data/CSVdisplaying.html")

def analyse_data(request, file_path):
    if not file_path:
        print("No file path provided.")
        return HttpResponse("No file path provided.")

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return HttpResponse(f"File {file_path} does not exist.")

    try:
        data = pd.read_csv(file_path, header=0)
        
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return HttpResponse(f"Error reading file {file_path}: {str(e)}")

    if data.empty:
        print(f"DataFrame is empty. Please provide a non-empty DataFrame.")
        return HttpResponse(f"DataFrame is empty. Please provide a non-empty DataFrame.")

    df = pd.DataFrame(data)
    show(df)
    # profile = ProfileReport(data, title="Profiling Report")

        # df = load_dataset(data)
        # create_report(df).show()
    html = df.to_html()

    return HttpResponse(html)


def analyse_data2(request, file_path):
    if not file_path:
        print("No file path provided.")
        return HttpResponse("No file path provided.")

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return HttpResponse(f"File {file_path} does not exist.")

    try:
        data = pd.read_csv(file_path, header=0)
        
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return HttpResponse(f"Error reading file {file_path}: {str(e)}")

    if data.empty:
        print(f"DataFrame is empty. Please provide a non-empty DataFrame.")
        return HttpResponse(f"DataFrame is empty. Please provide a non-empty DataFrame.")

    # df = pd.DataFrame(data)
    # show(df)
    profile = ProfileReport(data, title="Profiling Report")

        # df = load_dataset(data)
        # create_report(df).show()
    html = profile.to_html()

    return HttpResponse(html)
def csv_data(request):
    data=csv.objects.all()
    return render(request,"analysis_data/csv_data.html",data)