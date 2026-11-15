# CloudForce
Cloud Authentication Attack Surface & Brute-Force Visualizer

Subject: Data Analysis & Visualization (G5AD21DAV)

Authors: V.Mouli (240031101631054) & Samanvay Patel (240031101631040), 
B.Tech CSE Sem-5

## What it does
Generates synthetic cloud login logs with an injected brute-force attack,
analyses them with Plotly Express, and visualises them in Power BI.

## Setup
```bash
pip install -r requirements.txt
python generate_cloudforce_data.py   # creates cloudforce_logs.xlsx
python visualize_cloudforce.py       # creates 2 interactive HTML charts
python run_all.py                    # runs everything (Windows)
```

## Data columns (cloudforce_logs.xlsx, sheet "Logs")
log_id, timestamp, ip_address, country, user_id, cloud_service,
login_status, traffic_type, latitude, longitude, hour_bucket

## Key facts for the UI
- 5,900 rows; attack IP 185.220.101.45; attack on 4 Nov 2026, 02:00-02:20
- login_status: Success / Failed; traffic_type: Normal / Brute-Force

## Power BI
Open CloudForce.pbix. If the data fails to load, go to
Home > Transform data > Data source settings > Change Source and
point it to your local cloudforce_logs.xlsx.
