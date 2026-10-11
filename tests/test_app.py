
import pandas as pd
import pytest

from data_processor import validate_weather_data
from predictor import (
    classify_heat_risk,
    forecast_next_day_baseline,
)
from advisory import make_advisory


def test_low_risk():
    assert classify_heat_risk(32) == "Low"


def test_moderate_risk():
    assert classify_heat_risk(37) == "Moderate"


def test_high_risk():
    assert classify_heat_risk(42) == "High"


def test_extreme_risk():
    assert classify_heat_risk(46) == "Extreme"


def test_missing_required_columns():
    df = pd.DataFrame({
        "region": ["Pune"],
        "max_temperature_c": [39],
    })

    errors = validate_weather_data(df)

    assert any("Missing required columns" in e for e in errors)


def test_temperature_out_of_range():
    df = pd.DataFrame({
        "date": ["2026-05-01"],
        "region": ["Pune"],
        "latitude": [18.5204],
        "longitude": [73.8567],
        "max_temperature_c": [99],
    })

    errors = validate_weather_data(df)

    assert any("Temperature must be between" in e for e in errors)


def test_next_day_baseline():
    df = pd.DataFrame({
        "max_temperature_c": [34, 38, 40],
    })

    result = forecast_next_day_baseline(df)

    assert result == 40.0


def test_empty_forecast():
    df = pd.DataFrame({
        "max_temperature_c": [],
    })

    with pytest.raises(ValueError):
        forecast_next_day_baseline(df)


def test_advisory_contains_disclaimer():
    message = make_advisory("Pune", 42, "High")

    assert "not an official IMD warning" in message
