import argparse
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

def extract_numeric(value):
    """ Extracts numeric value from a string that may contain additional characters """
    try:
        return float(value.split()[0])
    except ValueError:
        return None

def convert_to_absolute_percentage(value):
    """ Convert a percentage string to an absolute float """
    try:
        # Remove parentheses and percent sign, then convert to float
        value = value.strip(' ()%')
        number = abs(float(value))
        return number
    except ValueError:
        return None

def process_txt(txt_file):
    timestamps = []
    latencies = []
    jitters = []
    packets = []
    losses = []
    stream_ids = []

    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Identify the start of the data section
    data_started = False
    for line in lines:
        line = line.strip()
        
        # Skip header and separator lines
        if line.startswith('=') or not line:
            continue
        
        if not data_started:
            # Find the line where data starts
            if line.startswith('Start time'):
                data_started = True
            continue

        # Split line into fields
        fields = line.split()
        if len(fields) < 16:
            print(f"Skipping malformed line: {line}")
            continue

        try:
            start_time = fields[0]
            end_time = fields[1]
            src_ip = fields[2]
            src_port = int(fields[3])
            dest_ip = fields[4]
            dest_port = int(fields[5])
            ssrc_hex = fields[6]
            payload = fields[7]
            pkts = int(fields[8])
            lost_str = fields[9]
            lost_ptc = convert_to_absolute_percentage(fields[10])
            min_delta = extract_numeric(fields[11])
            mean_delta = extract_numeric(fields[12])
            max_delta = extract_numeric(fields[13])
            min_jitter = extract_numeric(fields[14])
            mean_jitter = extract_numeric(fields[15])
            max_jitter = extract_numeric(fields[16])
            # Convert SSRC from hex to decimal
            ssrc = int(ssrc_hex, 16)

            # Convert time to ISO format
            absolute_start_time = "00:00:00"
            start_time_ = datetime.strptime(absolute_start_time, "%H:%M:%S")
            start_time_absolute = start_time_ + timedelta(seconds=float(start_time))
            end_time_absolute = start_time_ + timedelta(seconds=float(end_time))
            
            timestamp_ns = int(start_time_absolute.timestamp())
            # Extract numeric part of 'lost'
            lost = extract_numeric(lost_str)

            # Collect data for plotting
            timestamps.append(start_time_absolute)
            latencies.append(mean_delta)  # or min_delta, max_delta as needed
            jitters.append(mean_jitter)   # or min_jitter, max_jitter as needed
            packets.append(pkts)
            losses.append(lost_ptc)
            stream_ids.append(ssrc)

        except (ValueError, IndexError) as e:
            print(f"Error processing line: {line}")
            print(f"Exception: {e}")

    # Plot metrics
    plot_metrics(timestamps, latencies, jitters)
    plot_loss_jitter_relation(losses, jitters)
    plot_loss_latencies_relation(latencies, jitters)

def plot_metrics(timestamps, latencies, jitters):
    plt.figure(figsize=(14, 7))

    time_format = mdates.DateFormatter('%H:%M:%S')  # Formatter for the time part only

    plt.subplot(2, 1, 1)
    plt.plot(timestamps, latencies, linestyle='-', color='b')
    # plt.title('Latency Over Time')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(time_format)  # Set the formatter for the x-axis
    plt.xticks(rotation=45)
    plt.xlim([min(timestamps), max(timestamps)])

    plt.subplot(2, 1, 2)
    plt.plot(timestamps, jitters, linestyle='-', color='r')
    # plt.title('Jitter Over Time')
    plt.xlabel('Tempo')
    plt.ylabel('Jitter (ms)')
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(time_format)  # Set the formatter for the x-axis
    plt.xticks(rotation=45)
    plt.xlim([min(timestamps), max(timestamps)])

    plt.tight_layout()
    plt.show()

def plot_loss_jitter_relation(losses, jitters):
    plt.figure(figsize=(14, 7))

    hb = plt.hexbin(losses, jitters, gridsize=50, cmap='viridis', mincnt=1)
    plt.colorbar(hb, label='Count')

    # plt.title('Plot of Jitter vs. Packet Loss')
    plt.xlabel('Porcentagem de perda de pacotes')
    plt.ylabel('Jitter (ms)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_loss_latencies_relation(latencies, jitters):
    plt.figure(figsize=(14, 7))

    hb = plt.hexbin(latencies, jitters, gridsize=50, cmap='viridis', mincnt=1)
    plt.colorbar(hb, label='Count')

    # plt.title('Hexbin Plot of latencies vs. Packet Loss')
    plt.xlabel('Porcentagem de perda de pacotes')
    plt.ylabel('Latência Média')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract RTP Stream and plot metrics')
    parser.add_argument('txt_file', type=str, help='Path to the TXT file containing RTP stream data')

    args = parser.parse_args()
    process_txt(args.txt_file)
