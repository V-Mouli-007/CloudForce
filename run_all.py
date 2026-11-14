# run_all.py
# One-click launcher: generates data, makes charts, writes the PowerBI theme,
# opens the charts in the browser, and opens the PowerBI dashboard.

import subprocess      # lets Python run other scripts
import sys             # gives us the current Python interpreter
import os              # file and folder operations
import json            # to write the theme file
import time
import webbrowser      # opens HTML files in the browser

FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(FOLDER)       # make sure we run inside the project folder

def run_script(name):
    print(f"\n>>> Running {name} ...")
    subprocess.run([sys.executable, name], check=True)

# ---------- STEP 1: generate the data (NumPy + openpyxl) ----------
run_script("generate_cloudforce_data.py")

# ---------- STEP 2: build the Plotly Express charts ----------
run_script("visualize_cloudforce.py")

# ---------- STEP 3: write the PowerBI dark/neon theme file ----------
theme = {
    "name": "CloudForce Cyber",
    "dataColors": ["#00FF9F", "#00E5FF", "#FF1744", "#FFD600", "#B388FF", "#FF6D00"],
    "background": "#0B0F19",
    "foreground": "#E6FFF5",
    "tableAccent": "#00FF9F",
    "visualStyles": {
        "page": {"*": {"background": [{"color": {"solid": {"color": "#0B0F19"}}, "transparency": 0}]}},
        "*": {"*": {
            "background": [{"color": {"solid": {"color": "#111827"}}, "transparency": 0}],
            "title": [{"fontColor": {"solid": {"color": "#00FF9F"}}}]
        }}
    }
}
with open("cloudforce_theme.json", "w") as f:
    json.dump(theme, f, indent=2)
print("\n>>> Theme file written: cloudforce_theme.json")

# ---------- STEP 4: open the HTML charts in the browser ----------
for chart in ["chart1_failed_logins_timeline.html", "chart2_top_attacking_ips.html"]:
    webbrowser.open("file://" + os.path.join(FOLDER, chart))
    time.sleep(1)

# ---------- STEP 5: open the PowerBI dashboard ----------
pbix = os.path.join(FOLDER, "CloudForce.pbix")
if os.path.exists(pbix):
    print(">>> Opening PowerBI dashboard...")
    os.startfile(pbix)          # Windows only: opens with Power BI Desktop
else:
    print(">>> CloudForce.pbix not found. Build it once in PowerBI first.")

print("\nAll done! In PowerBI click Home -> Refresh to load the new data.")