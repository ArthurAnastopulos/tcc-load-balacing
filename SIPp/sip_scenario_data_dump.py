import argparse
import pyshark
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

def capture_traffic(interface, udp_port, rtp_port, influxdb_url, influxdb_token, influxdb_org, influxdb_bucket):
    # Initialize InfluxDB client
    client = InfluxDBClient(url=influxdb_url, token=influxdb_token)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    # Use a display filter to capture only traffic on the specified ports
    display_filter = f'udp.port == {udp_port} or udp.port == {rtp_port}'
    capture = pyshark.LiveCapture(interface=interface, display_filter=display_filter)
    
    print(f"Capturing traffic on interface {interface} for UDP port {udp_port} and RTP port {rtp_port}")

    try:
        for packet in capture.sniff_continuously():
            # Extract common fields
            timestamp = packet.sniff_time
            src_ip = packet.ip.src if hasattr(packet, 'ip') else 'N/A'
            dst_ip = packet.ip.dst if hasattr(packet, 'ip') else 'N/A'
            src_port = packet.udp.srcport if hasattr(packet, 'udp') else 'N/A'
            dst_port = packet.udp.dstport if hasattr(packet, 'udp') else 'N/A'
            protocol = packet.transport_layer if hasattr(packet, 'transport_layer') else 'N/A'
            length = packet.length
            
            if hasattr(packet, 'rtp'):
                # RTP packet
                rtp = packet.rtp
                sequence_number = rtp.seq if hasattr(rtp, 'seq') else 'N/A'
                rtp_timestamp = rtp.timestamp if hasattr(rtp, 'timestamp') else 'N/A'
                rtp_stream = rtp.ssrc if hasattr(rtp, 'ssrc') else 'N/A'
                
                point = Point("network_performance") \
                    .tag("type", "RTP") \
                    .tag("src_ip", src_ip) \
                    .tag("dst_ip", dst_ip) \
                    .tag("src_port", src_port) \
                    .tag("dst_port", dst_port) \
                    .field("protocol", protocol) \
                    .field("length", int(length)) \
                    .field("sequence_number", int(sequence_number)) \
                    .field("rtp_timestamp", int(rtp_timestamp)) \
                    .field("rtp_stream", rtp_stream) \
                    .time(timestamp, WritePrecision.NS)
                
                write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
                
                print(f"{timestamp} - {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}] (Length: {length}, Seq: {sequence_number}, Timestamp: {rtp_timestamp}, RTP Stream: {rtp_stream})")
            
            elif hasattr(packet, 'udp') and (int(src_port) == udp_port or int(dst_port) == udp_port):
                # UDP packet
                point = Point("network_performance") \
                    .tag("type", "UDP") \
                    .tag("src_ip", src_ip) \
                    .tag("dst_ip", dst_ip) \
                    .tag("src_port", src_port) \
                    .tag("dst_port", dst_port) \
                    .field("protocol", protocol) \
                    .field("length", int(length)) \
                    .time(timestamp, WritePrecision.NS)
                
                write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
                
                print(f"{timestamp} - {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}] (Length: {length})")
    
    except KeyboardInterrupt:
        print("Capture stopped.")
    except Exception as e:
        print(f"Error capturing traffic: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture network traffic and save it to InfluxDB for UDP and RTP traffic.")
    parser.add_argument("interface", type=str, help="The network interface to capture traffic on.")
    parser.add_argument("udp_port", type=int, help="The UDP port to filter traffic on.")
    parser.add_argument("rtp_port", type=int, help="The RTP media port to filter traffic on.")
    parser.add_argument("influxdb_url", type=str, help="The URL of the InfluxDB instance.")
    parser.add_argument("influxdb_token", type=str, help="The token for accessing InfluxDB.")
    parser.add_argument("influxdb_org", type=str, help="The organization name for InfluxDB.")
    parser.add_argument("influxdb_bucket", type=str, help="The bucket name for storing the data in InfluxDB.")

    args = parser.parse_args()
    capture_traffic(args.interface, args.udp_port, args.rtp_port, args.influxdb_url, args.influxdb_token, args.influxdb_org, args.influxdb_bucket)
