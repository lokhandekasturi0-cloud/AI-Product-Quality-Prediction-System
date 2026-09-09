# AI-Based Product Quality Prediction System

A local Streamlit application for AI-assisted early quality prediction and decision support for electronics manufacturing. It predicts `PASS`, `REWORK`, or `REJECT`, stores each result securely by user, explains abnormal measurements, and suggests corrective actions. It supports both individual and CSV/Excel batch predictions, analytics, history exports, and PDF reports.

## Important limitation

The included `manufacturing_data.csv` is generated synthetic demonstration data. It is useful for a college demonstration, but must be replaced and validated with real, governed manufacturing data before any production decision use. The system assists engineers; it does not replace final inspection.

## Features

- Secure bcrypt-hashed account signup and login
- Random Forest quality model, with Logistic Regression and Decision Tree comparison
- Single and batch CSV/XLS/XLSX prediction
- Model-derived quality/confidence score, reasons, and corrective recommendations
- SQLite prediction history, interactive dashboard, Plotly analytics, feature importance
- CSV exports and ReportLab PDF reports
- Responsive layout and local-network configuration for phones

## Installation and use

```powershell
cd AI_Product_Quality_Prediction
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ml\train_model.py
streamlit run app.py
```

Open `http://localhost:8501`, create an account, then make a prediction.

## Dataset format

CSV or Excel files must have these columns:

`Product_ID, Temperature, Voltage, Current, Weight, Pressure, Humidity, Machine_Speed`

All measurements must be non-negative numeric values. Expected operating ranges are centralized in `utils/config.py`, making them easy to adapt.

## Phone access on the same Wi-Fi

The bundled Streamlit configuration listens on your local network only. Connect the computer and phone to the same Wi-Fi, find the computer's IPv4 address with `ipconfig`, then open `http://YOUR_COMPUTER_IP:8501` on the phone. Allow Python/Streamlit through Windows Firewall for private networks if prompted. Do not expose the service publicly.

## Project structure

- `ml/`: data generation, training, model inference, metrics and importance
- `utils/`: database, authentication, validation, explanations, PDF generation, configuration
- `pages/`: modular Streamlit page renderers
- `data/`: generated demonstration data
- `models/`: persisted trained pipeline and metadata after training
- `database/`: local SQLite data

## Retraining

Replace `data/raw/manufacturing_data.csv` with a validated dataset containing the required fields plus `Quality`, then run:

```powershell
python ml\train_model.py
```
