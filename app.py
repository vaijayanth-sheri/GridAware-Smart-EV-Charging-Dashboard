# --- Standard Library and Third-Party Imports ---
import pytz
from dash import Dash, dcc, html

# --- Local Module Imports ---
# These imports bring in the UI components and callback logic from other files.
from components.tabs import create_main_tabs
from callbacks.market_callbacks import register_market_callbacks
from callbacks.ev_callbacks import register_ev_callbacks

# --- Constants ---
# Define the application's primary timezone. All time-sensitive calculations and displays will use this.
GERMAN_TIMEZONE = pytz.timezone('Europe/Berlin')

def create_app() -> Dash:
    """
    Creates and configures the main Dash application instance.
    
    This factory pattern encapsulates the app's setup, making it reusable,
    testable, and easier to manage.

    Returns:
        Dash: The configured Dash application object.
    """
    # --- App Initialization ---
    # Initialize the Dash app with necessary configurations.
    # - suppress_callback_exceptions=True is needed because tab content is rendered dynamically.
    # - assets_folder='assets' links the app to the CSS file.
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        assets_folder='assets',
        title="GridAware – Smart EV Charging Dashboard"
    )
    # Expose the Flask server instance for production deployments (e.g., with Gunicorn).
    server = app.server

    # --- App Layout Definition ---
    # The layout defines the structure of the web page's HTML.
    app.layout = html.Div(className='app-container', children=[
        # Centralized Data Storage using dcc.Store.
        # These components store data in the user's browser session, not on the server.
        dcc.Store(id='market-data-store'),      # Caches raw price data fetched from the Awattar API.
        dcc.Store(id='ev-config-store'),        # Persists the user's EV configuration form data.
        dcc.Store(id='analysis-results-store'), # Caches the results of the charging recommendation engine.

        # Static Page Header
        html.Div(className='header-container', children=[
            html.H1("⚡ GridAware – Smart EV Charging Dashboard", className='header-title'),
            html.P("Optimize your EV charging based on real-time German electricity prices.", className='header-subtitle')
        ]),

        # Main Content Area, organized into tabs.
        create_main_tabs()
    ])

    # --- Register Callbacks ---
    # Callbacks are the functions that connect UI components (like buttons and dropdowns)
    # to the application's logic. They are registered with the app instance here.
    register_market_callbacks(app, GERMAN_TIMEZONE)
    register_ev_callbacks(app)

    return app

# --- Main Execution Block ---
# This condition is true only when the script is executed directly (e.g., `python app.py`).
# It is not true when the file is imported by another script.
if __name__ == '__main__':
    # Create the app instance using the factory function.
    app = create_app()
    # CORRECTED: Use app.run() instead of the obsolete app.run_server()
    app.run(debug=True)