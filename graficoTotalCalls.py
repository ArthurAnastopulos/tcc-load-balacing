import matplotlib.pyplot as plt
import sys

# Função principal
def process_csv(csv_file, nodes):
    # Inicializar dicionário para contar chamadas SIP por nó
    node_count = {node: 0 for node in nodes}
    total_calls = 0

    # Abrir o arquivo CSV e processar linha por linha
    with open(csv_file, 'r') as file:
        for line in file:
            # Remover espaços em branco e dividir a linha
            parts = line.strip().split('\t')

            # Verificar se a linha tem pelo menos três partes
            if len(parts) >= 3:
                node = parts[2]  # O nó está na terceira coluna

                # Verificar se o nó está nos nós fornecidos
                if node in node_count:
                    node_count[node] += 1
                    total_calls += 1

    # Exibir o total de chamadas SIP no cenário e o total por nó
    print(f"Total de chamadas SIP no cenário: {total_calls}")
    for node, count in node_count.items():
        print(f"Total de chamadas para {node}: {count}")

    # Preparar os dados para o gráfico de pizza
    nodes_in_use = [node for node in nodes if node_count[node] > 0]
    calls_in_use = [node_count[node] for node in nodes_in_use]

    # Criar gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(calls_in_use, labels=nodes_in_use, autopct='%1.1f%%', startangle=90)
    # plt.title('Distribuição de Chamadas SIP entre os Nós do Balanceador de Carga')
    plt.axis('equal')  # Garantir que o gráfico de pizza seja um círculo
    plt.show()


if __name__ == "__main__":
    # Argumentos: nome do arquivo CSV seguido pelos endereços dos nós
    if len(sys.argv) < 3:
        print("Uso: python script.py <arquivo_csv> <endereco_no_1> <endereco_no_2> ...")
        sys.exit(1)

    csv_file = sys.argv[1]
    nodes = sys.argv[2:]

    # Processar o CSV e gerar o gráfico
    process_csv(csv_file, nodes)
