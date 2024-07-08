import subprocess
import time
import os

def start_sipp(scenario_file, rate, call_limit, remote_ip, local_ip):
    sipp_cmd = [
        "sipp", remote_ip, "-sf", scenario_file, "-r", str(rate), 
        "-l", str(call_limit), "-i", local_ip, "-m", str(call_limit), 
        "-trace_err"
    ]
    sipp_process = subprocess.Popen(sipp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sipp_process

def start_tshark(interface, capture_file):
    tshark_cmd = ["tshark", "-i", interface, "-w", capture_file]
    tshark_process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return tshark_process

def stop_process(process):
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

def analyze_tshark_output(capture_file):
    tshark_analysis_cmd = ["tshark", "-r", capture_file, "-q", "-z", "io,stat,1"]
    output = subprocess.check_output(tshark_analysis_cmd)
    return output.decode()

def main():
    scenario_file = "uac_pcap.xml"  # Replace with your Sipp scenario file
    rate = 10  # Calls per second
    call_limit = 100  # Total number of calls
    remote_ip = "192.168.1.100"  # Replace with your Asterisk server IP
    local_ip = "192.168.1.101"  # Replace with your local machine IP
    interface = "eth0"  # Network interface to capture traffic
    capture_file = "capture.pcap"

    print("Starting Sipp...")
    sipp_process = start_sipp(scenario_file, rate, call_limit, remote_ip, local_ip)

    print("Starting Tshark...")
    tshark_process = start_tshark(interface, capture_file)

    # Wait for Sipp to finish
    sipp_process.wait()

    print("Stopping Tshark...")
    stop_process(tshark_process)

    print("Analyzing capture file...")
    analysis_output = analyze_tshark_output(capture_file)
    print(analysis_output)

if __name__ == "__main__":
    main()
