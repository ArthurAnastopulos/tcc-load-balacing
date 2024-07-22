import subprocess
import csv
from datetime import datetime
import pyshark

sipp_cmd = []

proxy_interface = 'docker0'

sipp_uas_interfaces = ['docker1', 'docker2', 'docker3']

def capture_traffic(interface, port, csv_file):
    # Use a display filter to capture only traffic on the specified port
    capture = pyshark.LiveCapture(interface=interface, display_filter=f'tcp.port == {port}')
    
    print(f"Capturing traffic on interface {interface} for port {port}")
    
    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Timestamp', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Protocol', 'Length', 'Jitter', 'Latency', 'Packet Loss', 'RTP Stream'])
        
        try:
            for packet in capture.sniff_continuously():
                # Extract required fields from each packet
                timestamp = packet.sniff_time
                src_ip = packet.ip.src if 'IP' in packet else 'N/A'
                dst_ip = packet.ip.dst if 'IP' in packet else 'N/A'
                src_port = packet.tcp.srcport if 'TCP' in packet else 'N/A'
                dst_port = packet.tcp.dstport if 'TCP' in packet else 'N/A'
                protocol = packet.transport_layer
                length = packet.length
                
                # Initialize additional metrics
                jitter = 'N/A'
                latency = 'N/A'
                packet_loss = 'N/A'
                rtp_stream = 'N/A'
                
                # Check if the packet is an RTP packet and extract relevant metrics
                if 'RTP' in packet:
                    rtp = packet.rtp
                    jitter = rtp.get_field('jitter') if 'jitter' in rtp.field_names else 'N/A'
                    latency = rtp.get_field('delta') if 'delta' in rtp.field_names else 'N/A'
                    rtp_stream = rtp.ssrc
                    
                    # Note: Packet loss calculation might require additional logic to track sequence numbers
                    # and calculate loss over time. Here we just check if packet loss field is available.
                    packet_loss = rtp.get_field('pkt_lost') if 'pkt_lost' in rtp.field_names else 'N/A'

                # Write packet information to CSV
                writer.writerow([timestamp, src_ip, dst_ip, src_port, dst_port, protocol, length, jitter, latency, packet_loss, rtp_stream])
                
                # Print packet summary
                print(f"{timestamp} - {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}] (Length: {length}, Jitter: {jitter}, Latency: {latency}, Packet Loss: {packet_loss}, RTP Stream: {rtp_stream})")
                
        except KeyboardInterrupt:
            print("Capture stopped.")


