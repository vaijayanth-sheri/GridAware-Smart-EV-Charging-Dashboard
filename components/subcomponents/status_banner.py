from dash import html

def create_status_banner():
    """Creates the div that will act as a status banner."""
    return html.Div(id='status-banner', className='status-banner')