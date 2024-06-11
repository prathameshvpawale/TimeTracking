import json
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def load_usage_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            usage_data = json.load(json_file)
        return usage_data
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} not found.")
        return None

# Convert seconds to a more readable format (hours, minutes, seconds)
def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"

def plot_usage_data(frame):
    usage_data = load_usage_data('usage_data.json')
    if usage_data is None:
        return
    
    titles = list(usage_data.keys())
    times = list(usage_data.values())
    
    # Convert times to hours for better readability in the plot
    times_in_hours = [time / 3600 for time in times]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(titles, times_in_hours, color='skyblue')
    ax.set_xlabel('Time Spent (hours)')
    ax.set_ylabel('Applications/Websites')
    ax.set_title('Time Spent on Applications/Websites')
    
    # Annotate the bars with time spent in h:m:s format
    for index, value in enumerate(times):
        ax.text(value / 3600, index, seconds_to_hms(value))
    
    # Embed the plot in the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Usage Data Visualizer")
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    button = tk.Button(root, text="Show Usage Data", command=lambda: plot_usage_data(frame))
    button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
