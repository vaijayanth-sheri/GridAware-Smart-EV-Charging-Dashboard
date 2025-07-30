from dash import dcc, html

def create_ev_config_form():
    """
    Creates the simplified layout for the EV configuration input form.
    Removes presets, time windows, and modes for a more direct analysis.
    """
    return html.Div(className='form-grid', children=[
        # Battery Capacity
        html.Div(className='input-group', children=[
            html.Label("Battery Capacity (kWh)", className='input-label'),
            dcc.Input(id='ev-capacity', type='number', min=10, max=200, step=0.1, placeholder="e.g., 75", required=True)
        ]),
        # Current SoC
        html.Div(className='input-group', children=[
            html.Label("Current State of Charge (SoC %)", className='input-label'),
            dcc.Input(id='ev-soc-current', type='number', min=0, max=100, step=1, placeholder="e.g., 20", required=True)
        ]),
        # Target SoC
        html.Div(className='input-group', children=[
            html.Label("Target State of Charge (SoC %)", className='input-label'),
            dcc.Input(id='ev-soc-target', type='number', min=0, max=100, step=1, placeholder="e.g., 80", required=True)
        ]),
        # Max Charging Power
        html.Div(className='input-group', children=[
            html.Label("Max Charging Power (kW)", className='input-label'),
            dcc.Input(id='ev-max-power', type='number', min=1, max=50, step=0.1, placeholder="e.g., 11", required=True)
        ]),
        # Charging Efficiency
        html.Div(className='input-group', children=[
            html.Label("Charging Efficiency (%)", className='input-label'),
            dcc.Input(id='ev-efficiency', type='number', min=50, max=100, value=90, step=1, required=True)
        ]),
    ])