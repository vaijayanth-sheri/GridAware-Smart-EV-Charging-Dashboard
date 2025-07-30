import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import html, dcc, no_update

from utils.ev_logic import find_optimal_charging

def register_ev_callbacks(app):
    # Main analysis callback with simplified inputs
    @app.callback(
        [Output('ev-config-store', 'data'),
         Output('analysis-results-store', 'data'),
         Output('results-output', 'style'),
         Output('results-warning-banner', 'children'),
         Output('results-warning-banner', 'style'),
         Output('price-chart', 'figure', allow_duplicate=True),
         Output('results-summary-card', 'children'),
         Output('results-savings-card', 'children'),
         Output('cost-breakdown-chart', 'figure')],
        [Input('analyze-button', 'n_clicks')],
        [State('market-data-store', 'data'),
         State('ev-capacity', 'value'),
         State('ev-soc-current', 'value'),
         State('ev-soc-target', 'value'),
         State('ev-max-power', 'value'),
         State('ev-efficiency', 'value'),
         State('price-chart', 'figure')],
        prevent_initial_call=True
    )
    def run_analysis(n_clicks, market_data, capacity, soc_current, soc_target, max_power, efficiency, existing_fig):
        if n_clicks == 0:
            return [no_update] * 9

        # --- 1. Validate Inputs ---
        if not market_data or not market_data.get('prices'):
            return show_warning("Market data is not loaded. Please fetch prices on the 'Live Market Prices' tab first.")

        config = {
            'capacity': capacity, 'soc_current': soc_current, 'soc_target': soc_target,
            'max_power': max_power, 'efficiency': efficiency
        }
        
        missing_fields = [k for k, v in config.items() if v is None]
        if missing_fields:
            return show_warning(f"Analysis failed. Missing configuration for: {', '.join(missing_fields)}.")

        if soc_current >= soc_target:
             return show_warning("Target SoC must be higher than Current SoC.")

        # --- 2. Run Simplified Recommendation Engine ---
        price_df = pd.DataFrame(market_data['prices'])
        analysis_results = find_optimal_charging(price_df, config)

        if not analysis_results['success']:
            return show_warning(analysis_results['message'])

        # --- 3. Prepare Outputs ---
        optimal = analysis_results['optimal_slot']
        
        summary_card = create_summary_card(optimal, soc_target)
        
        savings_card = html.P(
            f"You save {analysis_results['savings_eur']:.2f}€ compared to charging in the most expensive period.",
            className='savings-text'
        )
        
        cost_breakdown_fig = create_cost_breakdown_figure(
            analysis_results['all_slots'], 
            optimal['start_time']
        )
        
        updated_price_fig = add_recommendation_overlay(existing_fig, optimal['start_time'], optimal['end_time'])
        
        style_visible = {'display': 'block'}
        style_hidden = {'display': 'none'}

        # Serialize results for storage
        analysis_results_serializable = analysis_results.copy()
        
        all_slots_df = analysis_results_serializable['all_slots']
        all_slots_df['start_time'] = all_slots_df['start_time'].apply(lambda ts: ts.isoformat())
        analysis_results_serializable['all_slots'] = all_slots_df.to_dict('records')
        
        analysis_results_serializable['optimal_slot']['start_time'] = analysis_results['optimal_slot']['start_time'].isoformat()
        analysis_results_serializable['optimal_slot']['end_time'] = analysis_results['optimal_slot']['end_time'].isoformat()
        
        return (
            json.dumps(config),
            json.dumps(analysis_results_serializable),
            style_visible, "", style_hidden, updated_price_fig,
            summary_card, savings_card, cost_breakdown_fig
        )

def show_warning(message):
    style_hidden = {'display': 'none'}
    style_visible = {'display': 'block'}
    no_fig_update = go.Figure()
    return (
        no_update, no_update, style_hidden, message, style_visible, 
        no_update, None, None, no_fig_update
    )

def create_summary_card(optimal, target_soc):
    duration_h = int(optimal['duration_hours'])
    duration_m = int((optimal['duration_hours'] * 60) % 60)
    
    start_time_dt = pd.to_datetime(optimal['start_time'])
    end_time_dt = pd.to_datetime(optimal['end_time'])

    return html.Div([
        html.H4("Optimal Charging Window", className='summary-title'),
        html.Div([html.Span("Start Time", className='summary-label'), html.Span(f"{start_time_dt.strftime('%H:%M')}", className='summary-value')], className='summary-item'),
        html.Div([html.Span("Finish Time", className='summary-label'), html.Span(f"{end_time_dt.strftime('%H:%M')} (Reaches {target_soc}%)", className='summary-value')], className='summary-item'),
        html.Div([html.Span("Duration", className='summary-label'), html.Span(f"{duration_h}h {duration_m}m", className='summary-value')], className='summary-item'),
        html.Div([html.Span("Energy Added", className='summary-label'), html.Span(f"{optimal['kwh_needed']:.2f} kWh", className='summary-value')], className='summary-item'),
        html.Div([html.Span("Estimated Cost", className='summary-label'), html.Span(f"{optimal['total_cost']:.2f} €", className='summary-value')], className='summary-item'),
    ])

def create_cost_breakdown_figure(all_slots_df, optimal_start_time):
    """
    Creates a line chart comparing the cost of charging at every possible start time.
    This version uses a datetime axis, which is the correct and robust way to 
    prevent the chart from expanding and breaking the UI.
    """
    df = pd.DataFrame(all_slots_df)
    df['start_time'] = pd.to_datetime(df['start_time'])

    optimal_point = df[df['start_time'] == pd.to_datetime(optimal_start_time)]

    fig = go.Figure()

    # Add the line chart for all possible start times
    # By using actual datetime objects for 'x', we enable Plotly's intelligent
    # time-series axis formatting, which prevents label collision and expansion.
    fig.add_trace(go.Scatter(
        x=df['start_time'],
        y=df['total_cost'],
        mode='lines',
        name='Cost',
        line=dict(color='#2980b9', width=2),
        hovertemplate='Start Time: %{x|%H:%M}<br>Cost: %{y:.2f}€<extra></extra>'
    ))

    # Add a prominent red marker for the optimal (cheapest) start time
    fig.add_trace(go.Scatter(
        x=optimal_point['start_time'],
        y=optimal_point['total_cost'],
        mode='markers',
        name='Optimal Time',
        marker=dict(color='#c0392b', size=12, symbol='star', line=dict(width=1, color='white')),
        hovertemplate='Optimal Start: %{x|%H:%M}<br>Lowest Cost: %{y:.2f}€<extra></extra>'
    ))
    
    fig.update_layout(
        title='Cost Comparison by Start Time',
        xaxis_title='Possible Start Times',
        yaxis_title='Total Charging Cost (€)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=40, b=40),
        showlegend=False,
        # Set the format for the tick labels on the time-series axis
        xaxis=dict(tickformat='%H:%M')
    )
    return fig

def add_recommendation_overlay(figure_json, start_time, end_time):
    fig = go.Figure(figure_json)
    fig.add_vrect(
        x0=start_time, x1=end_time,
        fillcolor="green", opacity=0.25,
        layer="below", line_width=0,
        annotation_text="Optimal Window", annotation_position="top left"
    )
    return fig