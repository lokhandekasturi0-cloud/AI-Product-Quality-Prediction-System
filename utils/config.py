FEATURES = ["Temperature", "Voltage", "Current", "Weight", "Pressure", "Humidity", "Machine_Speed"]
RANGES = {
    "Temperature": (20.0, 42.0), "Voltage": (4.75, 5.25), "Current": (1.8, 2.3),
    "Weight": (38.0, 46.0), "Pressure": (0.85, 1.15), "Humidity": (35.0, 60.0),
    "Machine_Speed": (80.0, 120.0),
}
REQUIRED_COLUMNS = ["Product_ID", *FEATURES]
