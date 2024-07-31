import time
import requests
import argparse
import pandas as pd

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
    df = pd.read_csv(csv_file, delimiter=' ', skipinitialspace=True)
    
    for _, row in df.iterrows():
        json_body = f"{db_table},src_ip={row['Src IP addr']},src_port={row['Port']},dest_ip={row['Dest IP addr']},dest_port={row['Port.1']} "
        json_body += f"pkts={row['Pkts']},lost={row['Lost'].split('(')[0]},min_delta={row['Min Delta(ms)']},"
        json_body += f"mean_delta={row['Mean Delta(ms)']},max_delta={row['Max Delta(ms)']},min_jitter={row['Min Jitter(ms)']},"
        json_body += f"mean_jitter={row['Mean Jitter(ms)']},max_jitter={row['Max Jitter(ms)']}"
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
