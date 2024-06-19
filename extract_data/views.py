from django.shortcuts import render, redirect
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from django.http import HttpResponse
from django.contrib.sessions.models import Session
import csv
from django.http import HttpResponse

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def extract_tables(request):
    if request.method == 'POST':
        # Extract database connection parameters from the form
        db_type = request.POST.get('db_type').lower()
        db_host = request.POST.get('db_host')
        db_name = request.POST.get('db_name')
        db_user = request.POST.get('db_user')
        db_password = request.POST.get('db_password')
        db_port = request.POST.get('db_port') or "3306"
        
        # Validate the database type
        if db_type not in ["mysql", "postgresql"]:
            return render(request, 'error.html', {'message': "Invalid Database Type"})
        
        try:
            # Create the SQLAlchemy engine based on the provided parameters
            if db_type == "mysql":
                con_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
            elif db_type == "postgresql":
                con_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
                
            engine = create_engine(con_string)
            # Store the connection string in the session
            request.session['con_string'] = con_string
            
            # Use the inspector to get table names and attributes
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            table_attributes = {}
            for table in tables:
                columns = inspector.get_columns(table)
                attributes = [column['name'] for column in columns]
                table_attributes[table] = attributes
            
            # Render a template with the table names and attributes
            return render(request, 'tables_info.html', {'table_attributes': table_attributes})
        
        except SQLAlchemyError as e:
            # If connection fails, render an error template with the error message
            return render(request, 'connection_failed.html', {'error_message': str(e)})
    
    # Render the form template if the request method is not POST
    return render(request, 'extract_tables.html')


def display_all_table_data(request):
    # Retrieve the connection string from the session
    con_string = request.session.get('con_string')
    
    # Create the SQLAlchemy engine
    engine = create_engine(con_string)

    # Establish a connection to the database
    connection = engine.connect()
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    table_data = {}

    # Loop over each table and fetch its data
    for table_name in tables:
        try:
            # Use the Inspector to get table metadata
            columns = inspector.get_columns(table_name)
            column_names = [column['name'] for column in columns]

            # Construct and execute the query to fetch data from the table
            query = text(f"SELECT * FROM {table_name}")
            result = connection.execute(query)
            data = result.fetchall()

            # Add data and column names to the table_data dictionary
            table_data[table_name] = {'data': data, 'columns': column_names}

        except Exception as e:
            # Handle exceptions if any occur
            print(f"Error fetching data from table {table_name}: {e}")
            table_data[table_name] = {'data': [], 'columns': []}

    # Close the database connection
    connection.close()

    # Pass the table data to the template
    return render(request, 'display_all_table_data.html', {'table_data': table_data})


def download_csv(request):
    table_name = request.GET.get('table_name')
    columns = request.GET.getlist('columns')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not table_name:
        return HttpResponse("Table name is missing", status=400)

    if not columns:
        return HttpResponse("No columns selected", status=400)

    con_string = request.session.get('con_string')
    if not con_string:
        return HttpResponse("Database connection string is missing", status=400)

    try:
        engine = create_engine(con_string)
        connection = engine.connect()
        inspector = inspect(engine)

        table_columns = inspector.get_columns(table_name)
        column_names = [column['name'] for column in table_columns]

        for col in columns:
            if col not in column_names:
                return HttpResponse(f"Column '{col}' does not exist in table '{table_name}'", status=400)

        select_columns = ', '.join(columns)
        query = f"SELECT {select_columns} FROM {table_name}"
        params = {}

        if start_date and end_date:
            # Ensure proper handling of dates to prevent SQL injection
            query += " WHERE PurchaseDate BETWEEN :start_date AND :end_date"
            params = {'start_date': start_date, 'end_date': end_date}

        # Execute the query with parameters using SQLAlchemy text
        result = connection.execute(text(query).params(**params))

        data = result.fetchall()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.csv"'

        writer = csv.writer(response)
        writer.writerow(columns)
        for row in data:
            writer.writerow(row)

        connection.close()

        return response

    except SQLAlchemyError as e:
        return HttpResponse(str(e), status=500)
