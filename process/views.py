from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from io import StringIO

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Calculate the number of duplicates and null values
        num_duplicates = df.duplicated().sum()
        num_nulls = df.isna().sum().sum()

        # Pass the CSV data to the processing form
        csv_data = df.to_csv(index=False) 
        return render(request, 'process_csv.html', {'csv_data': csv_data, 'num_duplicates': num_duplicates, 'num_nulls': num_nulls})

    return render(request, 'upload_csv.html')

def process_csv(request):
    if request.method == 'POST':
        # Get the CSV data from the hidden input field
        csv_data = request.POST.get('csv_data')

        try:
            # Read the CSV data into a DataFrame
            df = pd.read_csv(StringIO(csv_data))

            # Remove null values and duplicates from the DataFrame
            df.dropna(inplace=True)
            df.drop_duplicates(inplace=True)

            # Save the processed DataFrame to a CSV file in memory
            csv_content = df.to_csv(index=False)

            # Create a response to trigger file download
            response = HttpResponse(csv_content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="processed_csv.csv"'
            return response
        except Exception as e:
            print("Error:", e)  # Print any errors that occur

    # Handle case where no form is submitted
    return HttpResponse("No data submitted for processing.")
