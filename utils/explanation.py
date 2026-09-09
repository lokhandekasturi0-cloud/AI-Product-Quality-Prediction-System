from utils.config import FEATURES, RANGES

ACTIONS={
 "Temperature":("Stop or inspect the production process and reduce machine temperature before continuing.","Check heating settings and sensor calibration."),
 "Voltage":("Stop the line and inspect voltage regulation and the power supply.","Check power supply and electrical connections."),
 "Current":("Inspect current control and electrical load before continuing.","Check current-control settings and electrical connections."),
 "Weight":("Hold the product and inspect material quantity and feed calibration.","Check material quantity and recalibrate the weighing/feed mechanism."),
 "Pressure":("Stop and inspect machine pressure controls before continuing.","Check machine pressure settings and pneumatic calibration."),
 "Humidity":("Hold production and restore environmental humidity control.","Check environmental conditions and humidity-control calibration."),
 "Machine_Speed":("Stop or slow the production process and inspect process stability.","Adjust machine speed and verify process settings.")}

def explain(row):
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
    if not reasons: return ("All major monitored parameters are within the configured acceptable ranges.","No corrective action required. Continue normal production monitoring.")
    return (" ".join(reasons)," ".join(dict.fromkeys(actions)))
