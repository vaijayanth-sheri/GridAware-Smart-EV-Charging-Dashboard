from dash import dcc, html
import plotly.graph_objects as go

def create_price_plot():
    """Creates the graph component for displaying market prices."""
    
    # Define an initial, empty figure with a message
    initial_fig = go.Figure()
    initial_fig.update_layout(
        xaxis={'visible': False},
        yaxis={'visible': False},
        annotations=[{
            'text': "No market data loaded. Please click 'Fetch Latest Prices.'",
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 16, 'color': '#5a6a7a'}
        }],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return dcc.Loading(
        id="loading-price-chart",
        type="default",
        children=dcc.Graph(
            id='price-chart',
            figure=initial_fig,
            config={'displayModeBar': False}
        )
    )