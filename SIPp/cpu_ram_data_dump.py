import psutil
import time
import requests
import argparse

def get_cpu_ram_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

def send_to_influxdb(url, db, measurement, cpu, ram, timestamp):
    data = f"{measurement} cpu={cpu},ram={ram} {int(timestamp * 1e9)}"
    response = requests.post(url, params={'db': db}, data=data)
    if response.status_code != 204:
        print(f"Failed to send data to InfluxDB: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send CPU and RAM usage to InfluxDB")
    parser.add_argument('--url', required=True, help='InfluxDB HTTP API URL (e.g., http://localhost:8086/write)')
    parser.add_argument('--db', required=True, help='InfluxDB database name')
    parser.add_argument('--measurement', required=True, help='Measurement name in InfluxDB')
    parser.add_argument('--interval', type=int, default=5, help='Interval in seconds between data points')

    args = parser.parse_args()

    while True:
        cpu, ram = get_cpu_ram_usage()
        timestamp = time.time()
        send_to_influxdb(args.url, args.db, args.measurement, cpu, ram, timestamp)
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}, CPU Usage: {cpu}%, RAM Usage: {ram}%")
        time.sleep(args.interval)
