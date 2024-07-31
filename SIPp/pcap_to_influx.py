import time
import requests
import argparse
import pandas as pd
import numpy as np

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
    # Define the correct column names
    column_names = ['Start time', 'End time', 'Src IP addr', 'Src Port', 'Dest IP addr', 'Dest Port', 'SSRC',
                    'Payload', 'Pkts', 'Lost', 'Min Delta(ms)', 'Mean Delta(ms)', 'Max Delta(ms)', 
                    'Min Jitter(ms)', 'Mean Jitter(ms)', 'Max Jitter(ms)', 'Problems?']

    # Read the CSV file, skipping the first two rows and using predefined column names
    df = pd.read_csv(csv_file, delimiter='\s+', skiprows=2, names=column_names, engine='python')

    # Print column names for debugging
    print("Column names in the CSV:", df.columns.tolist())

    # Replace NaN and None with default values
    df.fillna({
        'Src IP addr': 'unknown',
        'Src Port': '0',
        'Dest IP addr': 'unknown',
        'Dest Port': '0',
        'SSRC': 'unknown',
        'Payload': 'unknown',
        'Pkts': '0',
        'Lost': '0',
        'Min Delta(ms)': '0',
        'Mean Delta(ms)': '0',
        'Max Delta(ms)': '0',
        'Min Jitter(ms)': '0',
        'Mean Jitter(ms)': '0',
        'Max Jitter(ms)': '0',
        'Problems?': 'none'
    }, inplace=True)

    # Convert columns to appropriate types
    df['Pkts'] = pd.to_numeric(df['Pkts'], errors='coerce').fillna(0).astype(int)
    df['Lost'] = df['Lost'].apply(lambda x: x.split('(')[0] if pd.notna(x) else '0')
    df['Min Delta(ms)'] = pd.to_numeric(df['Min Delta(ms)'], errors='coerce').fillna(0)
    df['Mean Delta(ms)'] = pd.to_numeric(df['Mean Delta(ms)'], errors='coerce').fillna(0)
    df['Max Delta(ms)'] = pd.to_numeric(df['Max Delta(ms)'], errors='coerce').fillna(0)
    df['Min Jitter(ms)'] = pd.to_numeric(df['Min Jitter(ms)'], errors='coerce').fillna(0)
    df['Mean Jitter(ms)'] = pd.to_numeric(df['Mean Jitter(ms)'], errors='coerce').fillna(0)
    df['Max Jitter(ms)'] = pd.to_numeric(df['Max Jitter(ms)'], errors='coerce').fillna(0)

    # Iterate through the DataFrame rows and create JSON body for InfluxDB
    for _, row in df.iterrows():
        json_body = (
            f"{db_table},src_ip={row['Src IP addr']},src_port={row['Src Port']},"
            f"dest_ip={row['Dest IP addr']},dest_port={row['Dest Port']},ssrc={row['SSRC']},"
            f"payload={row['Payload']} "
            f"start_time={row['Start time']},end_time={row['End time']},pkts={row['Pkts']},"
            f"lost={row['Lost']},min_delta={row['Min Delta(ms)']},mean_delta={row['Mean Delta(ms)']},"
            f"max_delta={row['Max Delta(ms)']},min_jitter={row['Min Jitter(ms)']},"
            f"mean_jitter={row['Mean Jitter(ms)']},max_jitter={row['Max Jitter(ms)']}"
        )
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
