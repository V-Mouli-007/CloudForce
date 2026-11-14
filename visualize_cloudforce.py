# visualize_cloudforce.py
# Reads the Excel file and builds 2 interactive HTML charts with Plotly Express.

import pandas as pd
import plotly.express as px

# Load the Excel file (openpyxl reads .xlsx files)
df = pd.read_excel("cloudforce_logs.xlsx", engine="openpyxl")

# Keep only failed logins, because those show the attack
failed = df[df["login_status"] == "Failed"]

# ---------------- CHART 1: Time-series line chart ----------------
# Count failed logins per hour
hourly = (
    failed.set_index("timestamp")
          .resample("1h")          # group into 1-hour buckets
          .size()                  # count rows per bucket
          .reset_index(name="failed_attempts")
)

fig1 = px.line(
    hourly,
    x="timestamp",
    y="failed_attempts",
    title="CloudForce: Failed Login Attempts per Hour",
    labels={"timestamp": "Time", "failed_attempts": "Failed Attempts"},
    template="plotly_dark",        # dark theme
)
fig1.update_traces(line_color="#00FF9F")     # neon green line
fig1.write_html("chart1_failed_logins_timeline.html")

# ---------------- CHART 2: Top 10 attacking IPs ----------------
top_ips = failed["ip_address"].value_counts().head(10).reset_index()
top_ips.columns = ["ip_address", "failed_attempts"]

fig2 = px.bar(
    top_ips,
    x="failed_attempts",
    y="ip_address",
    orientation="h",               # horizontal bars
    title="CloudForce: Top 10 IPs by Failed Logins",
    labels={"ip_address": "IP Address", "failed_attempts": "Failed Attempts"},
    template="plotly_dark",
    color_discrete_sequence=["#FF1744"],     # red bars
)
fig2.update_yaxes(type="category", autorange="reversed")  # biggest bar on top
fig2.write_html("chart2_top_attacking_ips.html")

print("Charts saved: chart1_failed_logins_timeline.html, chart2_top_attacking_ips.html")