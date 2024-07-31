import time
import requests
import argparse
import pandas as pd
import csv
from datetime import datetime

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

def process_csv_to_influx(csv_file, url, db, db_table, port):
    with open(csv_file, 'r') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            # Prepare the timestamp in InfluxDB format (ns precision)
            start_time = datetime.strptime(row['Start time'], '%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            end_time = datetime.strptime(row['End time'], '%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            # Fields
            json_body = (f"{db_table},StartTime=\"{start_time}\",EndTime=\"{end_time}\","
                      f"SrcPort={row['Port']},DestPort={row['Port']},"
                      f"Payload=\"{row['Payload']}\",Pkts={row['Pkts']},"
                      f"Lost={row['Lost']},MinDelta={row['Min Delta(ms)']},"
                      f"MeanDelta={row['Mean Delta(ms)']},MaxDelta={row['Max Delta(ms)']},"
                      f"MinJitter={row['Min Jitter(ms)']},MeanJitter={row['Mean Jitter(ms)']},"
                      f"MaxJitter={row['Max Jitter(ms)']},Problems=\"{row['Problems?']}\"")

            write_to_influxdb_http(url, db, port, json_body)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send RTP stream data to InfluxDB')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing RTP stream data')
    parser.add_argument('--url', type=str, default='localhost', help='InfluxDB URL')
    parser.add_argument('--db', type=str, default='mydb', help='InfluxDB database name')
    parser.add_argument('--table', type=str, default='rtp_stream', help='InfluxDB Table name')
    parser.add_argument('--port', type=int, default=8086, help='InfluxDB port')

    args = parser.parse_args()
    process_csv_to_influx(args.csv_file, args.url, args.db, args.table, args.port)
