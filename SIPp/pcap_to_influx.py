import requests
import argparse
from datetime import datetime, timedelta

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
            # problems = fields[17] if len(fields) > 16 else ''

            print("Min Delta:", min_delta)

            # Convert SSRC from hex to decimal
            ssrc = int(ssrc_hex, 16)

            # Convert time to ISO format
            absolute_start_time = "2024-07-31 12:00:00"
            start_time_ = datetime.strptime(absolute_start_time, "%Y-%m-%d %H:%M:%S")
            start_time_absolute = start_time_ + timedelta(seconds=float(start_time))
            end_time_absolute = start_time_ + timedelta(seconds=float(end_time))

            # Extract numeric part of 'lost'
            lost = extract_numeric(lost_str)

            # Create InfluxDB line protocol format
            json_body = (f"{db_table},SrcIP={src_ip},DestIP={dest_ip} "
                         f"StartTime=\"{start_time_absolute}\",EndTime=\"{end_time_absolute}\","
                         f"SrcPort={src_port},DestPort={dest_port},"
                         f"Pkts={pkts},Lost={lost},MinDelta={min_delta},"
                         f"MeanDelta={mean_delta},MaxDelta={max_delta},"
                         f"MinJitter={min_jitter},MeanJitter={mean_jitter},"
                         f"MaxJitter={max_jitter}")
            # curl -i -XPOST 'http://localhost:8086/write?db=your_database_name' --data-binary 'network_performance,type=RTP,src_ip=192.168.1.1,dst_ip=192.168.1.2,src_port=1234,dst_port=5678 protocol="UDP",length=128 sequence_number=123 rtp_timestamp=456 rtp_stream="stream1" 1596518400000000000'

            write_to_influxdb_http(url, db, port, json_body)

        except (ValueError, IndexError) as e:
            print(f"Error processing line: {line}")
            print(f"Exception: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send RTP stream data to InfluxDB')
    parser.add_argument('txt_file', type=str, help='Path to the TXT file containing RTP stream data')
    parser.add_argument('--url', type=str, default='localhost', help='InfluxDB URL')
    parser.add_argument('--db', type=str, default='mydb', help='InfluxDB database name')
    parser.add_argument('--table', type=str, default='rtp_stream', help='InfluxDB Table name')
    parser.add_argument('--port', type=int, default=8086, help='InfluxDB port')

    args = parser.parse_args()
    process_txt_to_influx(args.txt_file, args.url, args.db, args.table, args.port)
