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

        # Get columns with null values and their data types
        null_columns = df.columns[df.isna().any()].tolist()
        column_types = {col: df[col].dtype for col in null_columns}

        # Pass the CSV data and additional info to the processing form
        csv_data = df.to_csv(index=False)
        return render(request, 'process_csv.html', {
            'csv_data': csv_data,
            'num_duplicates': num_duplicates,
            'num_nulls': num_nulls,
            'null_columns': null_columns,
            'column_types': column_types
        })

    return render(request, 'upload_csv.html')

def process_csv(request):
    if request.method == 'POST':
        # Get the CSV data from the hidden input field
        csv_data = request.POST.get('csv_data')
        duplicate_handling = request.POST.get('duplicate_handling')

        # Debugging print statements
        print(f"Received csv_data: {csv_data[:100]}...")  # Print first 100 chars for brevity

        try:
            # Read the CSV data into a DataFrame
            df = pd.read_csv(StringIO(csv_data))

            # Handle null values based on user selection
            column_types = {col: df[col].dtype for col in df.columns[df.isna().any()]}
            for col, dtype in column_types.items():
                null_handling = request.POST.get(f'null_handling_{col}')
                if null_handling == 'remove':
                    df.dropna(subset=[col], inplace=True)
                elif null_handling == 'mean' and dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].mean(), inplace=True)
                elif null_handling == 'median' and dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].median(), inplace=True)
                elif null_handling == 'mode':
                    df[col].fillna(df[col].mode()[0], inplace=True)

            # Handle duplicates based on user selection
            if duplicate_handling and df.duplicated().sum() > 0:
                if duplicate_handling == 'remove':
                    df.drop_duplicates(inplace=True)
                elif duplicate_handling == 'keep_first':
                    df.drop_duplicates(keep='first', inplace=True)
                elif duplicate_handling == 'keep_last':
                    df.drop_duplicates(keep='last', inplace=True)

            # Save the processed DataFrame to a CSV file in memory
            csv_content = df.to_csv(index=False)

            # Create a response to trigger file download
            response = HttpResponse(csv_content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="processed_csv.csv"'
            return response
        except Exception as e:
            print("Error:", e)  # Print any errors that occur
            return HttpResponse(f"An error occurred: {e}")

    # Handle case where no form is submitted
    return HttpResponse("No data submitted for processing.")
