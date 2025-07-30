import pandas as pd
from datetime import timedelta
import numpy as np

def find_optimal_charging(price_df, config):
    """
    Core logic to calculate the best charging start time based on simplified config.
    This version finds the single cheapest continuous block of time to charge.
    
    Returns a dictionary with success status and results.
    """
    try:
        # 1. Prepare data and configuration
        df = price_df.copy()
        df['start_time'] = pd.to_datetime(df['start_time'])
        df = df.sort_values('start_time').reset_index(drop=True)

        kwh_to_add = (config['soc_target'] - config['soc_current']) / 100 * config['capacity']
        if kwh_to_add <= 0:
            return {'success': False, 'message': 'Target SoC must be higher than current SoC.'}

        kwh_needed_from_grid = kwh_to_add / (config['efficiency'] / 100)
        duration_hours = kwh_needed_from_grid / config['max_power']
        
        # Number of one-hour price slots needed for the charge (rounded up)
        slots_needed = int(np.ceil(duration_hours))
        if slots_needed == 0:
            return {'success': False, 'message': 'Calculated charging duration is zero.'}

        if len(df) < slots_needed:
            return {'success': False, 'message': f'Not enough future price data available to complete the required {duration_hours:.1f} hour charge.'}

        # 2. Find the cheapest block of 'slots_needed' hours using a rolling sum
        df['rolling_cost'] = df['price_eur_kwh'].rolling(window=slots_needed).sum()

        if df['rolling_cost'].isnull().all():
            return {'success': False, 'message': 'Could not calculate charging costs. Please check price data.'}

        # The index where the rolling cost is the minimum marks the *end* of the best window
        min_cost_end_idx = df['rolling_cost'].idxmin()
        start_idx = min_cost_end_idx - slots_needed + 1
        optimal_window_df = df.iloc[start_idx : min_cost_end_idx + 1]

        # 3. Calculate results for the optimal slot
        avg_price_in_window = optimal_window_df['price_eur_kwh'].mean()
        total_cost = avg_price_in_window * kwh_needed_from_grid
        
        start_time = optimal_window_df.iloc[0]['start_time']
        end_time = start_time + timedelta(hours=duration_hours)

        optimal_slot = {
            'start_time': start_time,
            'end_time': end_time,
            'total_cost': total_cost,
            'duration_hours': duration_hours,
            'kwh_needed': kwh_needed_from_grid
        }

        # For comparison, find the most expensive slot
        max_cost_end_idx = df['rolling_cost'].idxmax()
        max_start_idx = max_cost_end_idx - slots_needed + 1
        most_expensive_window_df = df.iloc[max_start_idx : max_cost_end_idx + 1]
        savings = (most_expensive_window_df['price_eur_kwh'].mean() * kwh_needed_from_grid) - total_cost

        # Create a DataFrame of all possible start times and their associated costs for the plot
        all_slots_df = pd.DataFrame({
            'start_time': df['start_time'].iloc[:len(df) - slots_needed + 1],
            'total_cost': (df['rolling_cost'].dropna() / slots_needed) * (kwh_needed_from_grid / duration_hours) * duration_hours
        })

        return {
            'success': True,
            'optimal_slot': optimal_slot,
            'all_slots': all_slots_df,
            'savings_eur': savings,
            'message': 'Analysis successful.'
        }
        
    except Exception as e:
        return {'success': False, 'message': f'An unexpected error occurred during analysis: {e}'}