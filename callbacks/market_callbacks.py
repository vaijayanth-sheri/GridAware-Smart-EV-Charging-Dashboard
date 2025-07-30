import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import html, no_update

from utils.price_api import fetch_market_prices, get_fallback_data, save_fallback_data

def register_market_callbacks(app, timezone):
    @app.callback(
        [Output('market-data-store', 'data'),
         Output('status-banner', 'children'),
         Output('status-banner', 'style'),
         Output('price-chart', 'figure')],
        [Input('fetch-prices-button', 'n_clicks')],
        [State('market-data-store', 'data')]
    )
    def update_market_data(n_clicks, existing_data):
        if n_clicks == 0:
            # On initial load, try to use fallback data
            fallback_data = get_fallback_data()
            if fallback_data and 'prices' in fallback_data:
                df = build_dataframe_from_stored_data(fallback_data, timezone)
                fig = create_price_figure(df)
                banner_text = f"Displaying cached data from {fallback_data.get('timestamp', 'an unknown time')}. Click 'Fetch Latest Prices' to update."
                return fallback_data, banner_text, {'display': 'block', 'borderColor': '#f39c12', 'backgroundColor': '#fdf5e6', 'color': '#f39c12'}, fig
            
            # Default empty state
            empty_fig = go.Figure().update_layout(
                xaxis={'visible': False}, yaxis={'visible': False}, annotations=[{'text': "No market data loaded.", 'showarrow': False, 'font': {'size': 16}}]
            )
            banner_text = "No market data loaded. Please click 'Fetch Latest Prices.'"
            banner_style = {'display': 'block', 'borderColor': '#2980b9', 'backgroundColor': '#eaf2f8', 'color': '#2980b9'}
            return no_update, banner_text, banner_style, empty_fig

        # Fetch new data from API
        api_data = fetch_market_prices(timezone)

        if api_data['success']:
            # API call was successful
            save_fallback_data(api_data)
            df = build_dataframe_from_stored_data(api_data, timezone)
            fig = create_price_figure(df)
            banner_text = f"Successfully fetched latest prices. Source: Awattar API. Last Updated: {api_data.get('timestamp')}"
            banner_style = {'display': 'block', 'borderColor': '#27ae60', 'backgroundColor': '#e9f7ef', 'color': '#27ae60'}
            # api_data is now JSON serializable and safe to store
            return api_data, banner_text, banner_style, fig
        else:
            # API call failed, attempt to use fallback
            error_message = api_data['error']
            fallback_data = get_fallback_data()
            if fallback_data and 'prices' in fallback_data:
                df = build_dataframe_from_stored_data(fallback_data, timezone)
                fig = create_price_figure(df)
                banner_text = f"Fetch failed: {error_message}. Displaying last known data from {fallback_data.get('timestamp')}."
                banner_style = {'display': 'block', 'borderColor': '#c0392b', 'backgroundColor': '#fbeae5', 'color': '#c0392b'}
                return fallback_data, banner_text, banner_style, fig
            else:
                # API failed and no fallback available
                empty_fig = go.Figure().update_layout(
                    xaxis={'visible': False}, yaxis={'visible': False}, annotations=[{'text': "Data fetch failed.", 'showarrow': False, 'font': {'size': 16}}]
                )
                banner_text = f"Fetch failed: {error_message}. No cached data is available."
                banner_style = {'display': 'block', 'borderColor': '#c0392b', 'backgroundColor': '#fbeae5', 'color': '#c0392b'}
                return None, banner_text, banner_style, empty_fig

def build_dataframe_from_stored_data(stored_data, timezone):
    """Helper to reconstruct a DataFrame from JSON-serializable stored data."""
    df = pd.DataFrame(stored_data['prices'])
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['start_time_local'] = df['start_time'].dt.tz_convert(timezone).dt.strftime('%Y-%m-%d %H:%M')
    return df

def create_price_figure(df):
    """Helper function to create the Plotly figure for prices."""
    df_display = df.head(24)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_display['start_time_local'],
        y=df_display['price_eur_kwh'],
        marker_color=df_display['price_eur_kwh'],
        marker_colorscale='viridis',
        hoverinfo='x+y',
        hovertemplate='Time: %{x}<br>Price: %{y:.2f} €/kWh<extra></extra>'
    ))

    fig.update_layout(
        title='Hourly Electricity Prices for the Next 24 Hours',
        xaxis_title='Hour of Day (Local Time)',
        yaxis_title='Price (€/kWh)',
        xaxis=dict(tickformat='%H:%M'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig