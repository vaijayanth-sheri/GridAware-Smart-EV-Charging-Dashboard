from dash import dcc, html

def create_ev_results():
    """Creates the layout for displaying the EV charging analysis results."""
    return html.Div(
        id='ev-results-container',
        children=[
            html.Div(id='results-warning-banner', style={'display': 'none'}, className='status-banner status-banner-warning'),
            html.Div(id='results-output', style={'display': 'none'}, children=[
                html.Div(className='results-grid', children=[
                    # Left Side: Summary Card
                    html.Div(id='results-summary-card', className='summary-card'),
                    
                    # Right Side: Savings & Breakdown
                    html.Div([
                        html.Div(id='results-savings-card', className='savings-card'),
                        dcc.Graph(id='cost-breakdown-chart', config={'displayModeBar': False})
                    ])
                ])
            ])
        ]
    )