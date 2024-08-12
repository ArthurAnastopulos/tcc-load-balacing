import pyshark
import csv
import sys

# Verificar se os argumentos de linha de comando foram fornecidos
if len(sys.argv) != 6:
    print("Uso: python script_vm.py <input_pcap_file> <output_csv_file> <ip_node1> <ip_node2> <ip_node3>")
    sys.exit(1)

# Capturar os argumentos
pcap_file = sys.argv[1]
output_csv = sys.argv[2]
ip_node1 = sys.argv[3]
ip_node2 = sys.argv[4]
ip_node3 = sys.argv[5]

# Carregar o pcap
cap = pyshark.FileCapture(pcap_file)

# Inicializar contadores para cada nó
node_calls = {ip_node1: 0, ip_node2: 0, ip_node3: 0}

# Iterar sobre os pacotes e contar as chamadas sucedidas
for packet in cap:
    if hasattr(packet, 'ip'):
        if packet.ip.dst == ip_node1:
            node_calls[ip_node1] += 1
        elif packet.ip.dst == ip_node2:
            node_calls[ip_node2] += 1
        elif packet.ip.dst == ip_node3:
            node_calls[ip_node3] += 1

# Salvar os resultados em um arquivo CSV
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Node', 'Calls'])
    for node, count in node_calls.items():
        writer.writerow([node, count])

print(f"Dados salvos em '{output_csv}'")
