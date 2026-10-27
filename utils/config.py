FEATURES = ["Temperature", "Voltage", "Current", "Weight", "Pressure", "Humidity", "Machine_Speed"]
RANGES = {
    # Preferred ranges calibrated from electronics_quality_training_6000.csv.
    "Temperature": (25.0, 58.0), "Voltage": (4.5, 5.6), "Current": (1.3, 2.55),
    "Weight": (44.0, 60.5), "Pressure": (1.8, 3.75), "Humidity": (19.0, 83.0),
    "Machine_Speed": (80.0, 160.0),
}
REQUIRED_COLUMNS = ["Product_ID", *FEATURES]
