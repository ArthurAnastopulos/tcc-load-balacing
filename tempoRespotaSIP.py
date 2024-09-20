import matplotlib.pyplot as plt

# Inicializar dicionário para contar SIP INVITE por segundo
invite_count = {}

# Abrir o arquivo e processar linha por linha
with open('sip_lc_51_invite_degradado.csv', 'r') as file:
    for line in file:
        # Remover espaços em branco e dividir a linha
        parts = line.strip().split('\t')

        # Verificar se a linha tem pelo menos três partes e se o método é 'INVITE'
        if len(parts) >= 3 and parts[2] == 'INVITE':
            timestamp = float(parts[0])  # Pegar o timestamp
            second = int(timestamp)        # Converter para inteiro (segundo)

            # Contar os SIP INVITE por segundo
            if second not in invite_count:
                invite_count[second] = 0
            invite_count[second] += 1

# Preparar os dados para plotagem
seconds = sorted(invite_count.keys())
counts = [invite_count[sec] for sec in seconds]

# Plotar o gráfico
plt.figure(figsize=(12, 6))
plt.plot(seconds, counts)
# plt.title('Quantidade de SIP INVITE por segundo')
plt.xlabel('Tempo (segundos)')
plt.ylabel('Quantidade de SIP INVITE')
plt.grid()
plt.show()
