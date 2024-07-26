import argparse
import pyshark
import requests
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

def capture_traffic(interface, udp_port, rtp_port, influxdb_url, influxdb_port, influxdb_db):
    # Use a display filter to capture only traffic on the specified ports
    display_filter = f'udp.port == {udp_port} or udp.port == {rtp_port}'
    capture = pyshark.LiveCapture(interface=interface, display_filter=display_filter)
    
    print(f"Capturing traffic on interface {interface} for UDP port {udp_port} and RTP port {rtp_port}")

    try:
        for packet in capture.sniff_continuously():
            # Extract common fields
            timestamp = packet.sniff_time.isoformat()
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
                
                line_protocol = (
                    f"network_performance,type=RTP,src_ip={src_ip},dst_ip={dst_ip},"
                    f"src_port={src_port},dst_port={dst_port} "
                    f"protocol=\"{protocol}\",length={length},"
                    f"sequence_number={sequence_number},rtp_timestamp={rtp_timestamp},"
                    f"rtp_stream=\"{rtp_stream}\" {int(packet.sniff_time.timestamp() * 1e9)}"
                )
                
                write_to_influxdb_http(influxdb_url, influxdb_db, influxdb_port, line_protocol)
                
                print(f"{timestamp} - {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}] "
                      f"(Length: {length}, Seq: {sequence_number}, Timestamp: {rtp_timestamp}, RTP Stream: {rtp_stream})")
            
            elif hasattr(packet, 'udp') and (int(src_port) == udp_port or int(dst_port) == udp_port):
                # UDP packet
                line_protocol = (
                    f"network_performance,type=UDP,src_ip={src_ip},dst_ip={dst_ip},"
                    f"src_port={src_port},dst_port={dst_port} "
                    f"protocol=\"{protocol}\",length={length} {int(packet.sniff_time.timestamp() * 1e9)}"
                )
                
                write_to_influxdb_http(influxdb_url, influxdb_db, influxdb_port, line_protocol)
                
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
    parser.add_argument("influxdb_port", type=int, help="The port of the InfluxDB instance.")
    parser.add_argument("influxdb_db", type=str, help="The name of the database in InfluxDB.")

    args = parser.parse_args()
    capture_traffic(args.interface, args.udp_port, args.rtp_port, args.influxdb_url, args.influxdb_port, args.influxdb_db)
