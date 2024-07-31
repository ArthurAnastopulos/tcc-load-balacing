import time
import requests
import argparse
import pandas as pd
import csv
from datetime import datetime
import subprocess

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

def get_tshark_rtp_streams(pcap_file):
    # Run tshark command and capture output
    command = ['tshark', '-r', pcap_file, '-q', '-z', 'rtp,streams']
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def parse_tshark_output(output):
    lines = output.splitlines()
    data = []

    # Start processing lines after the header
    is_data_section = False
    for line in lines:
        # Skip lines with '======' and headers
        if '=====' in line:
            is_data_section = not is_data_section
            continue
        
        if is_data_section:
            # Split and clean up the line
            columns = line.split()
            # Ensure there are enough columns
            if len(columns) >= 16:
                data.append(columns)

    # Create a DataFrame
    df = pd.DataFrame(data, columns=[
        'Start time', 'End time', 'Src IP addr', 'Src Port', 'Dest IP addr', 'Dest Port',
        'SSRC', 'Payload', 'Pkts', 'Lost', 'Min Delta(ms)', 'Mean Delta(ms)', 'Max Delta(ms)',
        'Min Jitter(ms)', 'Mean Jitter(ms)', 'Max Jitter(ms)', 'Problems?'
    ])

    return df

def process_csv_to_influx(df, url, db, db_table, port):
    for _, row in df.iterrows():
            try:
                start_time = datetime.strptime(row['Start time'].strip(), '%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                end_time = datetime.strptime(row['End time'].strip(), '%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%fZ')

                json_body = (f"{db_table},StartTime=\"{start_time}\",EndTime=\"{end_time}\","
                          f"SrcPort={row['Src Port'].strip()},DestPort={row['Dest Port'].strip()},"
                          f"Payload=\"{row['Payload'].strip()}\",Pkts={row['Pkts'].strip()},"
                          f"Lost={row['Lost'].strip()},MinDelta={row['Min Delta(ms)'].strip()},"
                          f"MeanDelta={row['Mean Delta(ms)'].strip()},MaxDelta={row['Max Delta(ms)'].strip()},"
                          f"MinJitter={row['Min Jitter(ms)'].strip()},MeanJitter={row['Mean Jitter(ms)'].strip()},"
                          f"MaxJitter={row['Max Jitter(ms)'].strip()},Problems=\"{row['Problems?'].strip()}\"")

                write_to_influxdb_http(url, db, port, json_body)

            except KeyError as e:
                print(f"KeyError: Missing column {e} in row {row.to_dict()}")
            except ValueError as e:
                print(f"ValueError: Issue with data formatting in row {row.to_dict()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send RTP stream data to InfluxDB')
    parser.add_argument('pcap_file', type=str, help='Path to the pcap file containing RTP stream data')
    parser.add_argument('--url', type=str, default='localhost', help='InfluxDB URL')
    parser.add_argument('--db', type=str, default='mydb', help='InfluxDB database name')
    parser.add_argument('--table', type=str, default='rtp_stream', help='InfluxDB Table name')
    parser.add_argument('--port', type=int, default=8086, help='InfluxDB port')

    args = parser.parse_args()
    output = get_tshark_rtp_streams(args.pcap_file)
    df = parse_tshark_output(output)
    process_csv_to_influx(df, args.url, args.db, args.table, args.port)
