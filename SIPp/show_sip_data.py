import sys
import csv
import matplotlib.pyplot as plt

# Verify command-line arguments
if len(sys.argv) != 5:
    print("Usage: python script.py <input_txt_file> <ip_node1> <ip_node2> <ip_node3>")
    sys.exit(1)

# Capture command-line arguments
input_txt = sys.argv[1]
ip_node1 = sys.argv[2]
ip_node2 = sys.argv[3]
ip_node3 = sys.argv[4]

# Initialize counters for each node
node_calls = {ip_node1: 0, ip_node2: 0, ip_node3: 0}

# Process the TXT file line by line
with open(input_txt, 'r') as file:
    for line in file:
        destination_ip = line.strip().split()[-1]  # Get the last element as the destination IP
        if destination_ip in node_calls:
            node_calls[destination_ip] += 1

# Calculate the total number of successful calls
total_calls = sum(node_calls.values())

# Calculate the difference for each node compared to the total
percentages = {node: (count / total_calls) * 100 for node, count in node_calls.items()}

# Generate the histogram
nodes = list(percentages.keys())
values = list(percentages.values())

bars = plt.bar(nodes, values)
plt.ylim([0, 100])
plt.xlabel('Nodos')
plt.ylabel('Porcentagem de chamadas bem-sucedidas (%)')
# plt.title('Percentage of Successful Calls per Node')

# Add percentage labels inside the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval - 5, f'{yval:.2f}%', ha='center', va='bottom', color='white', fontweight='bold')

plt.show()
