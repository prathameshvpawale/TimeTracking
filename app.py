import json
import time
import psutil
from datetime import datetime
import pygetwindow as gw
import threading
import flet as ft
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64

# Global variable to control tracking
tracking_active = False

# Function to get the active window title
def get_active_window_title():
    window = gw.getActiveWindow()
    if window:
        return window.title
    return None

# Function to track time spent on applications/websites
def track_time():
    global tracking_active
    usage_data = {}
    current_window = None
    start_time = None

    try:
        while tracking_active:
            new_window = get_active_window_title()

            if new_window != current_window:
                if current_window and start_time:
                    end_time = datetime.now()
                    elapsed_time = (end_time - start_time).total_seconds()

                    if current_window not in usage_data:
                        usage_data[current_window] = 0
                    usage_data[current_window] += elapsed_time

                current_window = new_window
                start_time = datetime.now()

            time.sleep(5)

    finally:
        with open('usage_data.json', 'w') as json_file:
            json.dump(usage_data, json_file, indent=4)
        print("Usage data saved to usage_data.json")

# Load usage data from the JSON file
def load_usage_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            usage_data = json.load(json_file)
        return usage_data
    except FileNotFoundError:
        return None

# Convert seconds to a more readable format (hours, minutes, seconds)
def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"

# Plot the usage data and return as a PIL image
def plot_usage_data():
    usage_data = load_usage_data('usage_data.json')
    if usage_data is None:
        return None
    
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
    
    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    return img

def main(page: ft.Page):
    global tracking_active
    page.title = "Usage Data Visualizer"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width=720.00
    page.window_height=720.00
    # Function to handle starting the tracking
    def on_start_tracking(e):
        global tracking_active
        if not tracking_active:
            tracking_active = True
            threading.Thread(target=track_time, daemon=True).start()
            start_tracking_button.disabled = True
            stop_tracking_button.disabled = False
            page.update()

    # Function to handle stopping the tracking
    def on_stop_tracking(e):
        global tracking_active
        tracking_active = False
        start_tracking_button.disabled = False
        stop_tracking_button.disabled = True
        page.update()

    # Function to handle button click
    def on_show_usage_data(e):
        img = plot_usage_data()
        if img is not None:
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            img_widget.src_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            page.update()
        else:
            ft.dialog.MessageDialog("Error", "Usage data file not found.", on_close=lambda _: page.update()).show(page)

    # Create buttons and image widgets
    start_tracking_button = ft.ElevatedButton(text="Start Tracking", on_click=on_start_tracking)
    stop_tracking_button = ft.ElevatedButton(text="Stop Tracking", on_click=on_stop_tracking, disabled=True)
    show_usage_button = ft.ElevatedButton(text="Show Usage Data", on_click=on_show_usage_data)
    img_widget = ft.Image()

    # Add widgets to the page
    page.add(
        ft.Column(
            [start_tracking_button, stop_tracking_button, show_usage_button, img_widget],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
