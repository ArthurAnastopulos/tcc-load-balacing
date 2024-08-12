import csv
import matplotlib.pyplot as plt
import sys

# Verificar se o nome do arquivo foi fornecido
if len(sys.argv) != 2:
    print("Uso: python script_local.py <input_csv_file>")
    sys.exit(1)

# Capturar o nome do arquivo CSV a partir dos argumentos
input_csv = sys.argv[1]

# Ler os dados do CSV gerado
node_calls = {}
with open(input_csv, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        node_calls[row['Node']] = int(row['Calls'])

# Calcular total de chamadas sucedidas
total_calls = sum(node_calls.values())

# Calcular a diferença de cada nó em relação ao total
differences = {node: total_calls - count for node, count in node_calls.items()}

# Gerar o histograma
nodes = list(differences.keys())
values = list(differences.values())

plt.bar(nodes, values)
plt.xlabel('Nodes')
plt.ylabel('Diferença de Chamadas Sucedidas')
# plt.title('Diferença de Chamadas Sucedidas por Nó')
plt.show()
