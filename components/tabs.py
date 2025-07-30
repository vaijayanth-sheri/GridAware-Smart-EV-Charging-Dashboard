from dash import dcc, html
from .market_tab import create_market_tab
from .ev_tab import create_ev_tab
from .about_tab import create_about_tab

def create_main_tabs():
    """Creates the main Dash Tabs component with all three tabs."""
    return dcc.Tabs(id="app-tabs", value='tab-market', className='custom-tabs-container', children=[
        dcc.Tab(label='Live Market Prices', value='tab-market', className='custom-tab', selected_className='custom-tab--selected', children=[
            create_market_tab()
        ]),
        dcc.Tab(label='EV Charging Optimization', value='tab-ev', className='custom-tab', selected_className='custom-tab--selected', children=[
            create_ev_tab()
        ]),
        dcc.Tab(label='About & Help', value='tab-about', className='custom-tab', selected_className='custom-tab--selected', children=[
            create_about_tab()
        ]),
    ])