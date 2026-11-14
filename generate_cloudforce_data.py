# generate_cloudforce_data.py
# Creates a SYNTHETIC cloud login log dataset with an injected brute-force attack.
# Output: cloudforce_logs.xlsx

import numpy as np
import pandas as pd

# A random number generator with a fixed seed -> same data every run (good for exams!)
rng = np.random.default_rng(seed=42)

# ------------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------------
N_NORMAL = 5000                                # number of normal login events
START = pd.Timestamp("2026-11-01 00:00:00")    # logs begin here
DAYS = 7                                       # logs cover 7 days

# Countries with their map coordinates (used later for the PowerBI map)
country_info = {
    "India":          (20.59,  78.96),
    "United States":  (37.09, -95.71),
    "United Kingdom": (55.38,  -3.44),
    "Germany":        (51.17,  10.45),
    "Singapore":      ( 1.35, 103.82),
    "Australia":      (-25.27, 133.78),
    "Brazil":         (-14.24, -51.93),
    "Russia":         (61.52, 105.32),
    "China":          (35.86, 104.20),
    "Nigeria":        ( 9.08,   8.68),
}
countries = np.array(list(country_info.keys()))
country_probs = [0.30, 0.20, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04]  # must sum to 1

services = np.array(["AWS Console", "Azure AD", "Google Cloud IAM", "Office 365"])

# ------------------------------------------------------------------
# 2. NORMAL TRAFFIC (generated with NumPy arrays)
# ------------------------------------------------------------------
# Timestamps: random second-offsets within 7 days, added to the start time
offsets = rng.integers(0, DAYS * 24 * 3600, size=N_NORMAL)
timestamps = START + pd.to_timedelta(offsets, unit="s")

# IP addresses: 4 random numbers (1-254) per row, joined with dots
ip_parts = rng.integers(1, 255, size=(N_NORMAL, 4))
ip_addresses = [".".join(map(str, row)) for row in ip_parts]

# Countries and cloud services chosen randomly (countries use weighted probabilities)
country = rng.choice(countries, size=N_NORMAL, p=country_probs)
cloud_service = rng.choice(services, size=N_NORMAL)

# User IDs: USER_1 ... USER_200
user_ids = np.char.add("USER_", rng.integers(1, 201, size=N_NORMAL).astype(str))

# Login status: 92% success, 8% failed (people mistype passwords sometimes)
login_status = rng.choice(["Success", "Failed"], size=N_NORMAL, p=[0.92, 0.08])

normal_df = pd.DataFrame({
    "timestamp": timestamps,
    "ip_address": ip_addresses,
    "country": country,
    "user_id": user_ids,
    "cloud_service": cloud_service,
    "login_status": login_status,
    "traffic_type": "Normal",
})

# ------------------------------------------------------------------
# 3. INJECT THE BRUTE-FORCE ATTACK
# ------------------------------------------------------------------
N_ATTACK = 900                                   # 900 attempts...
ATTACK_START = pd.Timestamp("2026-11-04 02:00:00")
ATTACK_IP = "185.220.101.45"                     # ...from ONE single IP...

# ...within just 20 minutes (1200 seconds)
attack_offsets = np.sort(rng.integers(0, 20 * 60, size=N_ATTACK))
attack_times = ATTACK_START + pd.to_timedelta(attack_offsets, unit="s")

# The attacker hammers a few privileged accounts
targets = np.array(["ADMIN_01", "ADMIN_02", "ROOT_USER"])
attack_users = rng.choice(targets, size=N_ATTACK)

# Every attempt fails, except the LAST one, where the attacker gets in
attack_status = np.array(["Failed"] * (N_ATTACK - 1) + ["Success"])

attack_df = pd.DataFrame({
    "timestamp": attack_times,
    "ip_address": ATTACK_IP,
    "country": "Russia",
    "user_id": attack_users,
    "cloud_service": "AWS Console",
    "login_status": attack_status,
    "traffic_type": "Brute-Force",
})

# ------------------------------------------------------------------
# 4. COMBINE, CLEAN AND ADD HELPER COLUMNS
# ------------------------------------------------------------------
df = pd.concat([normal_df, attack_df], ignore_index=True)
df = df.sort_values("timestamp").reset_index(drop=True)

df.insert(0, "log_id", np.arange(1, len(df) + 1))             # unique ID per row
df["latitude"] = df["country"].map(lambda c: country_info[c][0])
df["longitude"] = df["country"].map(lambda c: country_info[c][1])
df["hour_bucket"] = df["timestamp"].dt.floor("1h")            # time rounded to the hour (for line charts)

# ------------------------------------------------------------------
# 5. EXPORT TO EXCEL USING openpyxl
# ------------------------------------------------------------------
df.to_excel("cloudforce_logs.xlsx", index=False, sheet_name="Logs", engine="openpyxl")

print("Done! cloudforce_logs.xlsx created.")
print("Total rows:", len(df))
print("Failed logins:", (df['login_status'] == 'Failed').sum())
print("Attack IP:", ATTACK_IP)