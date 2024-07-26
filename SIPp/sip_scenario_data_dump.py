import argparse
import csv
import os
from datetime import datetime
import pyshark

def capture_traffic(interface, udp_port, rtp_port, udp_csv_file, rtp_csv_file):
    # Ensure the UDP and RTP CSV files are accessible or need to be created
    for file in [udp_csv_file, rtp_csv_file]:
        if not os.path.isfile(file):
            try:
                with open(file, 'w') as f:
                    pass
            except IOError as e:
                print(f"Error creating file {file}: {e}")
                return
    
    # Use a display filter to capture only traffic on the specified ports
    display_filter = f'udp.port == {udp_port} or udp.port == {rtp_port}'
    capture = pyshark.LiveCapture(interface=interface, display_filter=display_filter)
    
    print(f"Capturing traffic on interface {interface} for UDP port {udp_port} and RTP port {rtp_port}")

    try:
        # Open the CSV files for writing
        udp_file = open(udp_csv_file, mode='w', newline='')
        rtp_file = open(rtp_csv_file, mode='w', newline='')
        
        udp_writer = csv.writer(udp_file)
        rtp_writer = csv.writer(rtp_file)
        
        # Write the header row for UDP traffic
        udp_writer.writerow(['Timestamp', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Protocol', 'Length'])
        
        # Write the header row for RTP traffic
        rtp_writer.writerow(['Timestamp', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Protocol', 'Length', 'Sequence Number', 'Timestamp', 'RTP Stream'])
        
        for packet in capture.sniff_continuously():
            # Extract common fields
            timestamp = packet.sniff_time
            src_ip = packet.ip.src if hasattr(packet, 'ip') else 'N/A'
            dst_ip = packet.ip.dst if hasattr(packet, 'ip') else 'N/A'
            src_port = packet.udp.srcport if hasattr(packet, 'udp') else 'N/A'
            dst_port = packet.udp.dstport if hasattr(packet, 'udp') else 'N/A'
            protocol = packet.transport_layer if hasattr(packet, 'transport_layer') else 'N/A'
            length = packet.length
            
            # Check if the packet is from the RTP port
            if hasattr(packet, 'rtp'):
                rtp = packet.rtp
                
                sequence_number = rtp.seq if hasattr(rtp, 'seq') else 'N/A'
                rtp_timestamp = rtp.timestamp if hasattr(rtp, 'timestamp') else 'N/A'
                rtp_stream = rtp.ssrc if hasattr(rtp, 'ssrc') else 'N/A'
                
                # Write RTP packet information to the RTP CSV file
                rtp_writer.writerow([timestamp, src_ip, dst_ip, src_port, dst_port, protocol, length, sequence_number, rtp_timestamp, rtp_stream])
                
                # Flush the buffer to ensure data is written immediately
                rtp_file.flush()
                
                # Print RTP packet summary
                print(f"{timestamp} - {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}] (Length: {length}, Seq: {sequence_number}, Timestamp: {rtp_timestamp}, RTP Stream: {rtp_stream})")
            
            # Check if the packet is from the UDP port
            elif hasattr(packet, 'udp') and (int(src_port) == udp_port or int(dst_port) == udp_port):
                # Write UDP packet information to the UDP CSV file
                udp_writer.writerow([timestamp, src_ip, dst_ip, src_port, dst_port, protocol, length])
                
                # Flush the buffer to ensure data is written immediately
                udp_file.flush()
                
                # Print UDP packet summary
                print(f"{timestamp} - {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}] (Length: {length})")
    
    except KeyboardInterrupt:
        print("Capture stopped.")
    except IOError as e:
        print(f"Error writing to CSV files: {e}")
    finally:
        # Ensure files are closed properly
        udp_file.close()
        rtp_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture network traffic and save it to separate CSV files for UDP and RTP traffic.")
    parser.add_argument("interface", type=str, help="The network interface to capture traffic on.")
    parser.add_argument("udp_port", type=int, help="The UDP port to filter traffic on.")
    parser.add_argument("rtp_port", type=int, help="The RTP media port to filter traffic on.")
    parser.add_argument("udp_csv_file", type=str, help="The CSV file to save the captured UDP traffic.")
    parser.add_argument("rtp_csv_file", type=str, help="The CSV file to save the captured RTP traffic.")

    args = parser.parse_args()
    capture_traffic(args.interface, args.udp_port, args.rtp_port, args.udp_csv_file, args.rtp_csv_file)
