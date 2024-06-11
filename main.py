import json
import time
import psutil
from datetime import datetime
import pygetwindow as gw

def get_active_window_title():
    window = gw.getActiveWindow()
    if window:
        return window.title
    return None

# track_time of an application or site
def track_time(interval=5):
    usage_data = {}
    current_window = None
    start_time = None

    try:
        while True:
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

            time.sleep(interval)

    except KeyboardInterrupt:
        with open('usage_data.json', 'w') as json_file:
            json.dump(usage_data, json_file, indent=4)
        print("Usage data saved to usage_data.json")

if __name__ == "__main__":
    track_time()
