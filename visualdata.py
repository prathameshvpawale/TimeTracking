import json
import matplotlib.pyplot as plt

# Load usage data from the JSON file
def load_usage_data(file_path):
    with open(file_path, 'r') as json_file:
        usage_data = json.load(json_file)
    return usage_data

# Convert seconds to format (hours, minutes, seconds)
def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"


def plot_usage_data(usage_data):
    titles = list(usage_data.keys())
    times = list(usage_data.values())
    
    # Convert times to hours 
    times_in_hours = [time / 3600 for time in times]
    
    plt.figure(figsize=(12, 8))
    plt.barh(titles, times_in_hours, color='skyblue')
    plt.xlabel('Time Spent (hours)')
    plt.ylabel('Applications/Websites')
    plt.title('Time Spent on Applications/Websites')
    
    # Annotate the bars with time spent in h:m:s format
    for index, value in enumerate(times):
        plt.text(value / 3600, index, seconds_to_hms(value))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    usage_data = load_usage_data('usage_data.json')
    plot_usage_data(usage_data)
