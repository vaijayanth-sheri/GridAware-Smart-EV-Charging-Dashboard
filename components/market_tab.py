from dash import html
from .subcomponents.status_banner import create_status_banner
from .subcomponents.price_plot import create_price_plot

def create_market_tab():
    """Creates the layout for the 'Live Market Prices' tab."""
    return html.Div(className='card', children=[
        html.H2("Hourly Electricity Market Prices", className='card-header'),
        
        # Status banner to show fetch status, errors, and timestamps
        create_status_banner(),
        
        # Action button to fetch data
        html.Div(style={'marginBottom': '20px'}, children=[
            html.Button(
                "Fetch Latest Prices",
                id="fetch-prices-button",
                n_clicks=0,
                className='custom-button'
            )
        ]),
        
        # The plot for the price data
        create_price_plot(),
    ])