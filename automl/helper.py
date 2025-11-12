from robot_hat import utils  # Only if you're using the SunFounder Robot HAT

def get_battery_voltage():
    """Get the battery voltage (replace with your own function if needed)."""
    try:
        voltage = utils.get_battery_voltage()
    except Exception:
        # fallback or mock value for testing
        voltage = 7.5
    return voltage


def map_voltage_to_percent(voltage, min_v=6.0, max_v=8.4):
    """
    Map the battery voltage to a 0–100% range.
    
    min_v : voltage when battery is considered empty
    max_v : voltage when battery is fully charged
    """
    # Clamp voltage inside range
    if voltage < min_v:
        voltage = min_v
    elif voltage > max_v:
        voltage = max_v

    # Convert to percent
    percent = ((voltage - min_v) / (max_v - min_v)) * 100
    return round(percent, 1)
