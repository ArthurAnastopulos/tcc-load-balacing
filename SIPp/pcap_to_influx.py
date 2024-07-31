import requests
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def write_to_influxdb_http(url, db, port, json_body):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    full_url = f'http://{url}:{port}/write?db={db}'
    print(f"Sending data to: {full_url}")
    print(f"Data: {json_body}")
    response = requests.post(full_url, data=json_body, headers=headers)
    
    if response.status_code == 204:
        print("Data written successfully")
    else:
        print(f"Error writing data: {response.text}")

def extract_numeric(value):
    """ Extracts numeric value from a string that may contain additional characters """
    try:
        return float(value.split()[0])
    except ValueError:
        return None

def process_txt_to_influx(txt_file, url, db, db_table, port):
    timestamps = []
    latencies = []
    jitters = []

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
            min_delta = extract_numeric(fields[11])
            mean_delta = extract_numeric(fields[12])
            max_delta = extract_numeric(fields[13])
            min_jitter = extract_numeric(fields[14])
            mean_jitter = extract_numeric(fields[15])
            max_jitter = extract_numeric(fields[16])

            # Convert SSRC from hex to decimal
            ssrc = int(ssrc_hex, 16)

            # Convert time to ISO format
            absolute_start_time = "2024-07-31 12:00:00"
            start_time_ = datetime.strptime(absolute_start_time, "%Y-%m-%d %H:%M:%S")
            start_time_absolute = start_time_ + timedelta(seconds=float(start_time))
            end_time_absolute = start_time_ + timedelta(seconds=float(end_time))
            
            timestamp_ns = int(start_time_absolute.timestamp())
            # Extract numeric part of 'lost'
            lost = extract_numeric(lost_str)

            # Create InfluxDB line protocol format
            json_body = (f"{db_table},SrcIP={src_ip},DestIP={dest_ip} "
                         f"StartTime=\"{start_time_absolute}\",EndTime=\"{end_time_absolute}\","
                         f"SrcPort={src_port},DestPort={dest_port},"
                         f"Pkts={pkts},Lost={lost},MinDelta={min_delta},"
                         f"MeanDelta={mean_delta},MaxDelta={max_delta},"
                         f"MinJitter={min_jitter},MeanJitter={mean_jitter},"
                         f"MaxJitter={max_jitter},time={timestamp_ns}")
            # write_to_influxdb_http(url, db, port, json_body)

            # Collect data for plotting
            timestamps.append(start_time_absolute)
            latencies.append(mean_delta)  # or min_delta, max_delta as needed
            jitters.append(mean_jitter)   # or min_jitter, max_jitter as needed

        except (ValueError, IndexError) as e:
            print(f"Error processing line: {line}")
            print(f"Exception: {e}")

    # Plot metrics
    plot_metrics(timestamps, latencies, jitters)

def plot_metrics(timestamps, latencies, jitters):
    plt.figure(figsize=(14, 7))

    plt.subplot(2, 1, 1)
    plt.plot(timestamps, latencies, linestyle='-', color='b')
    plt.title('Latency Over Time')
    plt.xlabel('Time')
    plt.ylabel('Latency (ms)')
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.subplot(2, 1, 2)
    plt.plot(timestamps, jitters, linestyle='-', color='r')
    plt.title('Jitter Over Time')
    plt.xlabel('Time')
    plt.ylabel('Jitter (ms)')
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send RTP stream data to InfluxDB and plot metrics')
    parser.add_argument('txt_file', type=str, help='Path to the TXT file containing RTP stream data')
    parser.add_argument('--url', type=str, default='localhost', help='InfluxDB URL')
    parser.add_argument('--db', type=str, default='mydb', help='InfluxDB database name')
    parser.add_argument('--table', type=str, default='rtp_stream', help='InfluxDB Table name')
    parser.add_argument('--port', type=int, default=8086, help='InfluxDB port')

    args = parser.parse_args()
    process_txt_to_influx(args.txt_file, args.url, args.db, args.table, args.port)
