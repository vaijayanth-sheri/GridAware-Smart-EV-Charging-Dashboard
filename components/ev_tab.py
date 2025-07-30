from dash import html
from .subcomponents.ev_config_form import create_ev_config_form
from .subcomponents.ev_results import create_ev_results

def create_ev_tab():
    """Creates the layout for the 'EV Charging Optimization' tab."""
    return html.Div([
        # Configuration Card
        html.Div(className='card', children=[
            html.H2("EV Charging Configuration", className='card-header'),
            create_ev_config_form(),
            html.Div(style={'marginTop': '20px', 'textAlign': 'center'}, children=[
                html.Button(
                    "Save & Analyze",
                    id="analyze-button",
                    n_clicks=0,
                    className='custom-button custom-button-primary'
                )
            ])
        ]),
        
        # Results Card
        html.Div(className='card', children=[
            html.H2("Charging Recommendation", className='card-header'),
            create_ev_results()
        ])
    ])