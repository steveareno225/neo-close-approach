import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Constants
EARTH_RADIUS_KM = 6371
LUNAR_DISTANCE_KM = 384400
AU_TO_KM = 149597870.7
GEOSYNC_KM = EARTH_RADIUS_KM + 35786  # 42157 km

# Conversion helpers
def convert_distance(value, from_unit, to_unit):
    unit_to_km = {
        "km": 1,
        "miles": 1.60934,
        "earth_radii": EARTH_RADIUS_KM,
        "lunar": LUNAR_DISTANCE_KM,
        "au": AU_TO_KM
    }
    km = value * unit_to_km[from_unit]
    return km / unit_to_km[to_unit]

def load_json_file(path):
    with open(path, 'r') as f:
        return json.load(f)

# Safe date parsing with fallback
def parse_date_safe(date_str):
    for fmt in ("%Y-%b-%d %H:%M:%S", "%Y-%b-%d %H:%M", "%Y-%b-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    raise ValueError(f"Unknown date format: {date_str}")

def filter_and_plot(data, start_date, end_date, limit_val, limit_unit, output_unit, top_n, annotate_n):
    fields = data['fields']
    fullname_idx = fields.index("fullname")
    dist_idx = fields.index("dist")
    date_idx = fields.index("cd")

    filtered_data = []
    for entry in data['data']:
        try:
            date_str = entry[date_idx]
            date_obj = parse_date_safe(date_str)
            au = float(entry[dist_idx])
            km = au * AU_TO_KM
            distance_out = convert_distance(km, "km", output_unit)
            if start_date <= date_obj <= end_date:
                if km <= convert_distance(limit_val, limit_unit, "km"):
                    filtered_data.append((date_obj, distance_out, entry[fullname_idx], km))
        except Exception:
            continue

    if not filtered_data:
        messagebox.showinfo("No Data", "No NEOs within the given filters.")
        return

    if top_n > 0:
        filtered_data = sorted(filtered_data, key=lambda x: x[3])[:top_n]

    dates = [x[0] for x in filtered_data]
    dists = [x[1] for x in filtered_data]
    labels = [x[2] for x in filtered_data]

    fig, ax = plt.subplots(figsize=(15, 7))
    ax.scatter(dates, dists)

    for i in range(min(len(labels), annotate_n)):
        ax.annotate(labels[i], (dates[i], dists[i]), textcoords="offset points", xytext=(5, 5), ha='left',
                    fontsize=7, arrowprops=dict(arrowstyle='-', lw=0.5, color='gray'))

    ax.set_title("NEO Close Approaches")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Distance ({output_unit})")
    ax.grid(True, linestyle=":")

    earth_line = convert_distance(EARTH_RADIUS_KM, "km", output_unit)
    geo_line = convert_distance(GEOSYNC_KM, "km", output_unit)
    ax.axhline(y=earth_line, linestyle='--', color='gray')

    limit_lunar = convert_distance(limit_val, limit_unit, "lunar")
    if limit_lunar >= 1:
        lunar_line = convert_distance(LUNAR_DISTANCE_KM, "km", output_unit)
        ax.axhline(y=lunar_line, linestyle='--', color='orange')

    if geo_line < max(dists) * 1.2:
        ax.axhline(y=geo_line, linestyle='--', color='purple')

    ax.set_xlim(start_date, end_date)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    fig.autofmt_xdate()
    plt.subplots_adjust(left=0.11, right=0.9)
    plt.show()

def run_gui():
    root = tk.Tk()
    root.title("NEO Close Approach Scatter Plot")

    tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0)
    start_entry = tk.Entry(root); start_entry.insert(0, "2004-01-01"); start_entry.grid(row=0, column=1)

    tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=1, column=0)
    end_entry = tk.Entry(root); end_entry.insert(0, "2029-12-31"); end_entry.grid(row=1, column=1)

    tk.Label(root, text="Limit Distance:").grid(row=2, column=0)
    limit_entry = tk.Entry(root); limit_entry.insert(0, "42157"); limit_entry.grid(row=2, column=1)

    tk.Label(root, text="Limit Unit:").grid(row=3, column=0)
    limit_unit_combo = ttk.Combobox(root, values=["km", "miles", "earth_radii", "lunar", "au"])
    limit_unit_combo.set("km"); limit_unit_combo.grid(row=3, column=1)

    tk.Label(root, text="Output Unit:").grid(row=4, column=0)
    output_unit_combo = ttk.Combobox(root, values=["km", "miles", "earth_radii", "lunar", "au"])
    output_unit_combo.set("earth_radii"); output_unit_combo.grid(row=4, column=1)

    tk.Label(root, text="Top N Closest (0=All):").grid(row=5, column=0)
    top_n_entry = tk.Entry(root); top_n_entry.insert(0, "0"); top_n_entry.grid(row=5, column=1)

    tk.Label(root, text="Annotations (0=none):").grid(row=6, column=0)
    anno_entry = tk.Entry(root); anno_entry.insert(0, "100"); anno_entry.grid(row=6, column=1)

    def plot_action():
        try:
            json_path = os.path.join(os.path.dirname(__file__), "cad.customization.json")
            data = load_json_file(json_path)
            start = datetime.strptime(start_entry.get(), "%Y-%m-%d")
            end = datetime.strptime(end_entry.get(), "%Y-%m-%d")
            limit_val = float(limit_entry.get())
            limit_unit = limit_unit_combo.get()
            output_unit = output_unit_combo.get()
            top_n = int(top_n_entry.get())
            anno_n = int(anno_entry.get())
            filter_and_plot(data, start, end, limit_val, limit_unit, output_unit, top_n, anno_n)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Plot with cad.customization.json", command=plot_action).grid(row=7, column=0, columnspan=2, pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
