import sys
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

def main(file_path):
    # Your Python script code here
    app = dash.Dash(__name__)
    data = pd.read_csv(file_path)



    app.layout = html.Div([
        html.H1("Interactive Data Table and Visualization"),
        html.Div([
            dcc.Dropdown(
                id='x-axis',
                options=[{'label': col, 'value': col} for col in data.columns],
                value=data.columns[0]
            ),
            dcc.Dropdown(
                id='y-axis',
                options=[{'label': col, 'value': col} for col in data.columns],
                value=data.columns[1]
            ),
        ]),
        dcc.Graph(id='graph'),
        html.H2("Data Table"),
        html.Div(id='table'),
        html.H2("Summary Statistics"),
        html.Div(id='summary'),
        html.H2("Histogram"),
        dcc.Dropdown(
            id='histogram-column',
            options=[{'label': col, 'value': col} for col in data.columns],
            placeholder="Select column for Histogram"
        ),
        dcc.Graph(id='histogram')
    ], style={'padding': '20px'})

    @app.callback(
        [Output('graph', 'figure'), Output('table', 'children'), Output('summary', 'children'), Output('histogram', 'figure')],
        [Input('x-axis', 'value'), Input('y-axis', 'value'), Input('histogram-column', 'value')]
    )
    def update_output(x_axis, y_axis, hist_col):
        # Scatter plot
        figure = px.scatter(data, x=x_axis, y=y_axis, title=f'Scatter plot of {x_axis} vs {y_axis}')
        
        # Data table
        table = html.Table([
            html.Thead(html.Tr([html.Th(col, style={'padding': '10px'}) for col in data.columns])),
            html.Tbody([
                html.Tr([
                    html.Td(data.iloc[i][col], style={'padding': '10px'}) for col in data.columns
                ]) for i in range(min(len(data), 10))  # Display first 10 rows
            ])
        ])
        
        # Summary statistics
        desc = data.describe()
        summary = html.Table([
            html.Thead(html.Tr([html.Th(col, style={'padding': '10px'}) for col in desc.columns])),
            html.Tbody([
                html.Tr([html.Td('Mean:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["mean"]:.2f}', style={'padding': '10px'}) for col in desc.columns]),
                html.Tr([html.Td('Std Dev:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["std"]:.2f}', style={'padding': '10px'}) for col in desc.columns]),
                html.Tr([html.Td('Min:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["min"]:.2f}', style={'padding': '10px'}) for col in desc.columns]),
                html.Tr([html.Td('25%:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["25%"]:.2f}', style={'padding': '10px'}) for col in desc.columns]),
                html.Tr([html.Td('Median:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["50%"]:.2f}', style={'padding': '10px'}) for col in desc.columns]),
                html.Tr([html.Td('75%:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["75%"]:.2f}', style={'padding': '10px'}) for col in desc.columns]),
                html.Tr([html.Td('Max:', style={'padding': '10px'})] + [html.Td(f'{desc[col]["max"]:.2f}', style={'padding': '10px'}) for col in desc.columns])
            ])
        ])
        
        # Histogram
        histogram = px.histogram(data, x=hist_col, title=f'Histogram of {hist_col}') if hist_col else {}

        return figure, table, summary, histogram

    if __name__ == '__main__':
        app.run_server(debug=True)
        print(f"File path: {file_path}")

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Usage: python script.py <file_path>")
            sys.exit(1)

        main(sys.argv[1])