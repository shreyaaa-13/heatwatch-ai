
import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "region",
    "latitude",
    "longitude",
    "max_temperature_c",
]

def load_weather_data(path="data/weather_data.csv"):
    """Load the weather dataset from a CSV file."""
    return pd.read_csv(path, parse_dates=["date"])


def validate_weather_data(df):
    """Check that weather data has valid columns and values."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        return [f"Missing required columns: {', '.join(missing)}"]

    if df.empty:
        return ["The dataset contains no rows."]

    errors = []

    if df["region"].isna().any():
        errors.append("Region contains missing values.")

    for col in ["latitude", "longitude", "max_temperature_c"]:
        values = pd.to_numeric(df[col], errors="coerce")

        if values.isna().any():
            errors.append(f"{col} contains invalid or missing values.")

    if errors:
        return errors

    temperatures = pd.to_numeric(df["max_temperature_c"])

    if ((temperatures < -20) | (temperatures > 60)).any():
        errors.append("Temperature must be between -20 and 60 °C.")

    latitudes = pd.to_numeric(df["latitude"])
    longitudes = pd.to_numeric(df["longitude"])

    if ((latitudes < -90) | (latitudes > 90)).any():
        errors.append("Latitude must be between -90 and 90.")

    if ((longitudes < -180) | (longitudes > 180)).any():
        errors.append("Longitude must be between -180 and 180.")

    return errors


def summarize_regions(df):
    """Calculate average, maximum and minimum temperature per region."""
    return (
        df.groupby("region")["max_temperature_c"]
        .agg(["mean", "max", "min"])
        .reset_index()
    )
