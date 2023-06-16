import pandas as pd
import os
import numpy as np
import requests
import json
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.graph_objects as go
import dash_daq as daq



#import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

# Define the API endpoint URL
url = 'https://nss-container-p57byuk3wa-uc.a.run.app/api/ask'
df = pd.DataFrame()  # Initialize an empty DataFrame

def make_api_request(query, noReviews):
    payload = {
        'query': query,
        'top_n': noReviews,
        'threshold': 0.75
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        # Return the processed data
        return data


@app.callback(
    [
        dash.dependencies.Output('graph', 'figure'),
        dash.dependencies.Output('table1', 'data'),
        dash.dependencies.Output('table1', 'columns'),
        dash.dependencies.Output('submit-button', 'disabled')
    ],
    [
        dash.dependencies.Input('submit-button', 'n_clicks'),
        dash.dependencies.Input('input1', 'value'),
    ],
    [
        dash.dependencies.State('slider1', 'value'),
        dash.dependencies.State('passcode', 'value')

    ]
)
def handle_button_click(n_clicks, input_value, slider_value, passcode_value):
    ctx = dash.callback_context
    print('Button click')

    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']

        if 'submit-button' in prop_id:
            print('prop_id',prop_id, passcode_value)

            if n_clicks is not None and n_clicks > 0 and input_value and passcode_value == 'nss23@RCU':
                print('Calling API')
                # Call the make_api_request function with the input value
                api_response = make_api_request(input_value, slider_value)

                if api_response is not None:
                    # Extract the first child of the JSON object
                    reviews_data = api_response.get('reviews', [])

                    # Convert the first child to a DataFrame
                    df = pd.DataFrame(reviews_data)

                    return (
                        {
                            'data': [
                                {
                                    'x': df['valence_score'],
                                    'y': df['arousal_score'],
                                    'mode': 'markers',
                                    'hovertext': df['Review'],
                                    'hoverinfo': df['Review'],
                                },
                            ],
                            'layout': {
                                'title': 'Valence and Arousal',
                                'width': 800,  # Set the width of the figure
                                'height': 500,  # Set the height of the figure
                                'xaxis': {
                                    'title': 'Valence Score'
                                },
                                'yaxis': {
                                    'title': 'Arousal Score'
                                },
                                'annotations': [
                                {
                                    'x': 1.25,  # X-coordinate of the annotation
                                    'y': 0.1,  # Y-coordinate of the annotation
                                    'text': 'Happy',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'green',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                                {
                                    'x': 1,  # X-coordinate of the annotation
                                    'y': 1,  # Y-coordinate of the annotation
                                    'text': 'Excited',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'orange',  # Color of the text
                                        'size': 14  # Size of the text
                                    }
                                },
                                {
                                    'x': -1.25,  # X-coordinate of the annotation
                                    'y': 0.1,  # Y-coordinate of the annotation
                                    'text': 'Sad',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'grey',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                                {
                                    'x': 0.15,  # X-coordinate of the annotation
                                    'y': 1.25,  # Y-coordinate of the annotation
                                    'text': 'Suprise',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'purple',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                                {
                                    'x': -1,  # X-coordinate of the annotation
                                    'y': 1,  # Y-coordinate of the annotation
                                    'text': 'Angry',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'red',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                                {
                                    'x': -1,  # X-coordinate of the annotation
                                    'y': -1,  # Y-coordinate of the annotation
                                    'text': 'Depressed',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'black',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                                {
                                    'x': 1,  # X-coordinate of the annotation
                                    'y': -1,  # Y-coordinate of the annotation
                                    'text': 'Relaxed',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'blue',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                                {
                                    'x': 0.1,  # X-coordinate of the annotation
                                    'y': -1.25,  # Y-coordinate of the annotation
                                    'text': 'Quiet',  # Text to display as the label
                                    'showarrow': False,  # Hide the arrow
                                    'font': {
                                        'color': 'sand',  # Color of the text
                                        'size': 12  # Size of the text
                                    }
                                },
                        ]
                    }
                },
                        df.to_dict('records'),
                        [{"name": col, "id": col} for col in df.columns[:2]],
                        False  # Enable the submit button
                    )
                else:
                    return blank_fig(), [], [], True  # Disable the submit button

    # Disable the submit button if the input value is empty
    return blank_fig(), [], [], not bool(input_value)

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig
app.layout = html.Div(
    children=[
        html.Div(
            style={'text-align': 'center', 'marginBottom': '40px'},
            children=[
                html.H1(children='National Student Survey'),
                html.H2(children='Analysis of student comments'),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin': '0 20px'},
            children=[
                dcc.Input(
                    id='passcode',
                    type='text',
                    placeholder='Enter the passcode',
                    style={'marginRight': '10px', 'width': '500px', 'height': '30px'}
                ),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin': '0 20px'},
            children=[
                dcc.Input(
                    id='input1',
                    type='text',
                    placeholder='Enter your question',
                    style={'marginBottom': '10px', 'width': '500px', 'height': '30px'}
                ),
                daq.Slider(
                    id='slider1',
                    min=0,
                    max=300,
                    value=50,
                    handleLabel={"showCurrentValue": True, "label": "No of Reviews", "style": {"fontSize": 30}},
                    step=10,
                    color="#888888"
                ),
                html.Button('Submit', id='submit-button', n_clicks=0,
                            style={'marginLeft': '30px', 'width': '70px', 'height': '30px'}, disabled=True)
            ]
        ),
        html.Div(
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            children=[
                dcc.Graph(id='graph', figure=blank_fig(), style={'width': '800px', 'height': '500px'})
            ]
        ),
        dash_table.DataTable(
            id='table1',
            columns=[],  # Only display first two columns
            data=[],
            style_table={'width': '95%', 'marginLeft': '30px','marginRight': '30px'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'text-align': 'left'
            },            
        ),
    ]
)

if __name__ == '__main__':
    PORT = os.getenv('PORT', 8050)
    app.run_server(debug=True, port=PORT, host='0.0.0.0')
