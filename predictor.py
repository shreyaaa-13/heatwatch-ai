
def classify_heat_risk(temp_c):
    """
    Educational heat-risk baseline.
    These are prototype thresholds, not official IMD criteria.
    """
    temp_c = float(temp_c)

    if temp_c < 35:
        return "Low"
    elif temp_c < 40:
        return "Moderate"
    elif temp_c < 45:
        return "High"
    else:
        return "Extreme"


def forecast_next_day_baseline(region_df):
    """
    Simple persistence baseline:
    estimate the next day's temperature using
    the most recent available observation.
    """
    if region_df.empty:
        raise ValueError("No weather observations available.")

    temperatures = region_df["max_temperature_c"].dropna()

    if temperatures.empty:
        raise ValueError("No valid temperature readings available.")

    return float(temperatures.iloc[-1])
