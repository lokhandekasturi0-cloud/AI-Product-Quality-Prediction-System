from functools import lru_cache
from pathlib import Path
import pandas as pd
from utils.config import FEATURES, RANGES

ACTIONS={
 "Temperature":("Stop or inspect the production process and reduce machine temperature before continuing.","Check heating settings and sensor calibration."),
 "Voltage":("Stop the line and inspect voltage regulation and the power supply.","Check power supply and electrical connections."),
 "Current":("Inspect current control and electrical load before continuing.","Check current-control settings and electrical connections."),
 "Weight":("Hold the product and inspect material quantity and feed calibration.","Check material quantity and recalibrate the weighing/feed mechanism."),
 "Pressure":("Stop and inspect machine pressure controls before continuing.","Check machine pressure settings and pneumatic calibration."),
 "Humidity":("Hold production and restore environmental humidity control.","Check environmental conditions and humidity-control calibration."),
 "Machine_Speed":("Stop or slow the production process and inspect process stability.","Adjust machine speed and verify process settings.")}

@lru_cache(maxsize=1)
def _pass_bands():
    """Learn normal parameter bands from labelled PASS production records."""
    root=Path(__file__).resolve().parents[1]
    for source in [root/'data'/'raw'/'electronics_quality_training_6000.csv', root/'data'/'processed'/'cleaned_data.csv']:
        if source.exists():
            data=pd.read_csv(source)
            target='Quality_Status' if 'Quality_Status' in data.columns else 'Quality'
            if target in data.columns:
                passed=data[data[target].astype(str).str.upper().eq('PASS')]
                if not passed.empty:
                    return {feature:(float(passed[feature].quantile(.05)),float(passed[feature].quantile(.95))) for feature in FEATURES}
    return {}

def _profile_concerns(row):
    concerns=[]
    for feature,(low,high) in _pass_bands().items():
        value=float(row[feature]); span=max(high-low,1e-9)
        if value<low: concerns.append((feature,(low-value)/span,'below'))
        elif value>high: concerns.append((feature,(value-high)/span,'above'))
    return sorted(concerns,key=lambda item:item[1],reverse=True)

def explain(row, prediction='PASS'):
    """Give deterministic reasons from actual range distance; >=50% beyond a limit is critical."""
    moderate=[]; critical=[]
    for f in FEATURES:
        low,high=RANGES[f]; value=float(row[f]); distance=(low-value)/(high-low) if value<low else (value-high)/(high-low) if value>high else 0
        if distance>=.50: critical.append(f)
        elif distance>0: moderate.append(f)
    if len(critical)>=2:
        return ("Multiple critical manufacturing parameters are outside acceptable limits.","Reject the product and inspect the manufacturing process before producing the next batch.")
    reasons=[]; actions=[]
    for f in critical+moderate:
        low,high=RANGES[f]; direction='above' if float(row[f])>high else 'below'; significant=f in critical
        reasons.append(f"{f.replace('_',' ')} is {'significantly ' if significant else ''}{direction} the {'acceptable' if significant else 'preferred'} range.")
        actions.append(ACTIONS[f][0 if significant else 1])
    if not reasons:
        concerns=_profile_concerns(row)
        if prediction == 'PASS':
            return ("All major monitored parameters are within the configured acceptable ranges.","No corrective action required. Continue normal production monitoring.")
        if concerns:
            detail=', '.join(f"{feature.replace('_',' ')} ({direction} the PASS production profile)" for feature,_,direction in concerns[:2])
            if prediction == 'REWORK':
                return (f"The model identified a rework-risk pattern. Key measurements: {detail}.","Inspect and recalibrate the affected process settings, then rework and retest the product.")
            return (f"The model identified a reject-risk parameter pattern. Key measurements: {detail}.","Hold or reject the product and inspect the affected production controls before the next batch.")
        if prediction == 'REWORK':
            return ("The model identified a combined rework-risk pattern across the monitored parameters, even though no single value exceeds the broad limits.","Inspect process settings, rework the product where possible, and retest it before release.")
        return ("The model identified a combined reject-risk pattern across the monitored parameters, even though no single value exceeds the broad limits.","Hold or reject the product and inspect the manufacturing process before producing the next batch.")
    return (" ".join(reasons)," ".join(dict.fromkeys(actions)))
