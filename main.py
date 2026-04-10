import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ===== FUNCTIONS =====
def get_weather_value():
    weather_text = weather_var.get()
    return {"Clear": 1, "Windy": 2, "Storm": 3}[weather_text]


def calculate_fuel(distance, wind, weather, aircraft):

    # ===== BASE DATA =====
    if aircraft == "Airbus A320":
        cruise_burn = 2.7
        climb_fuel = 1800
        taxi_fuel = 200
        seats = 180

        # smooth inefficiency increase
        long_penalty = 1 + (distance / 4000)
        cruise_burn *= long_penalty

    elif aircraft == "Boeing 737":
        cruise_burn = 2.85
        climb_fuel = 1900
        taxi_fuel = 210
        seats = 170

        # smooth mid-range advantage (curve)
        efficiency = 1 - ((distance - 1400) ** 2) / (1400 ** 2)
        efficiency = max(0.75, efficiency)
        cruise_burn *= (1 / efficiency)

    else:  # Airbus A350
        cruise_burn = 6.0
        climb_fuel = 6000
        taxi_fuel = 400
        seats = 300

        # smooth improvement for long range
        long_gain = 1 - (distance / 6000)
        long_gain = max(0.6, long_gain)
        cruise_burn *= long_gain

    # ===== EFFECTS =====
    weather_factor = 1 + (weather * 0.04)
    wind_factor = 1 + (wind / 600)

    cruise_distance = distance * 0.92
    cruise_fuel = cruise_distance * cruise_burn * weather_factor * wind_factor

    total_fuel = taxi_fuel + climb_fuel + cruise_fuel

    fuel_per_passenger = total_fuel / seats

    return total_fuel, fuel_per_passenger

def predict_fuel():
    try:
        distance = float(entry_distance.get())
        wind = float(entry_wind.get())
        weather = get_weather_value()
        aircraft = aircraft_var.get()

        fuel, fpp = calculate_fuel(distance, wind, weather, aircraft)
        result_label.config(
    text=f"{aircraft}\nTotal Fuel: {fuel:.2f} kg\nFuel/Passenger: {fpp:.2f} kg"
)

    except:
        messagebox.showerror("Error", "Invalid Input")


def compare_aircraft():
    try:
        distance = float(entry_distance.get())
        wind = float(entry_wind.get())
        weather = get_weather_value()

        aircrafts = ["Airbus A320", "Boeing 737", "Airbus A350"]

        results = {}

        for aircraft in aircrafts:
            fuel, fpp = calculate_fuel(distance, wind, weather, aircraft)
            results[aircraft] = fpp   # 🔥 compare based on efficiency

        best_aircraft = min(results, key=results.get)

        # TEXT OUTPUT
        text = "=== Aircraft Comparison ===\n\n"
        for a, f in results.items():
            text += f"{a}: {f:.2f} kg/passenger\n"
        text += f"\nBest Choice:\n{best_aircraft}"
        result_label.config(text=text)

        # ===== GRAPH =====
        for widget in graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 3.8))

        fig.patch.set_facecolor("#1e1e2f")
        ax.set_facecolor("#1e1e2f")

        names = list(results.keys())
        values = list(results.values())

        ax.bar(names, values)

        ax.set_title("Aircraft Fuel Comparison", color="white")
        ax.set_ylabel("Fuel (kg)", color="white")
        ax.tick_params(colors="white")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # 🔥 IMPORTANT FIX
        plt.close(fig)

    except:
        messagebox.showerror("Error", "Enter valid inputs!")


# ===== UI =====
root = tk.Tk()
root.title("Flight AI Optimizer ✈️")
root.geometry("650x750")
root.configure(bg="#1e1e2f")

root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(1, weight=1)

# Title
tk.Label(root, text="Flight AI Optimizer",
         font=("Arial", 18, "bold"),
         bg="#1e1e2f", fg="white")\
    .grid(row=0, column=0, columnspan=2, pady=15)

# Distance
tk.Label(root, text="Distance (km)", bg="#1e1e2f", fg="white")\
    .grid(row=1, column=0, padx=20, pady=10, sticky="w")
entry_distance = tk.Entry(root)
entry_distance.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

# Wind
tk.Label(root, text="Wind Speed (km/h)", bg="#1e1e2f", fg="white")\
    .grid(row=2, column=0, padx=20, pady=10, sticky="w")
entry_wind = tk.Entry(root)
entry_wind.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

# Weather
tk.Label(root, text="Weather", bg="#1e1e2f", fg="white")\
    .grid(row=3, column=0, padx=20, pady=10, sticky="w")

weather_var = tk.StringVar(value="Clear")

tk.OptionMenu(root, weather_var, "Clear", "Windy", "Storm")\
    .grid(row=3, column=1, padx=20, pady=10, sticky="ew")

# Aircraft
tk.Label(root, text="Aircraft", bg="#1e1e2f", fg="white")\
    .grid(row=4, column=0, padx=20, pady=10, sticky="w")

aircraft_var = tk.StringVar(value="Airbus A320")

tk.OptionMenu(root, aircraft_var,
              "Airbus A320",
              "Boeing 737",
              "Airbus A350")\
    .grid(row=4, column=1, padx=20, pady=10, sticky="ew")

# Buttons
tk.Button(root, text="Predict Fuel",
          bg="#00c853", fg="white",
          font=("Arial", 12, "bold"),
          command=predict_fuel)\
    .grid(row=5, column=0, columnspan=2, pady=15)

tk.Button(root, text="Compare Aircraft",
          bg="#2962ff", fg="white",
          font=("Arial", 12, "bold"),
          command=compare_aircraft)\
    .grid(row=6, column=0, columnspan=2, pady=10)

# Result
result_label = tk.Label(root,
                        text="",
                        font=("Arial", 12),
                        bg="#1e1e2f",
                        fg="#00ffcc")
result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Graph Frame
graph_frame = tk.Frame(root, bg="#1e1e2f")
graph_frame.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

root.mainloop()
