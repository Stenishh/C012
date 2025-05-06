import copy

transacoes_base = [
    ("Depósito João",         4, 2, 0),
    ("Transferência Ana",     5, 1, 1),
    ("Pagamento Boleto",      3, 3, 2),
    ("Saque Carlos",          2, 2, 4),
    ("Depósito Maria",        1, 2, 5),
    ("Transferência Empresa", 6, 1, 5),
    ("Investimento Pedro",    7, 4, 6),
    ("Pagamento Cartão",      2, 3, 7),
    ("Saque Lucas",           3, 2, 8),
    ("Depósito Júlia",        1, 3, 9)
]


def fcfs(transacoes):
    print("🏦 FCFS (First Come First Serve):")
    tempo = 0
    tempos_espera = {}

    transacoes.sort(key=lambda t: t[3])  # ordenar por chegada

    for nome, duracao, _, chegada in transacoes:
        if tempo < chegada:
            tempo = chegada
        espera = tempo - chegada
        tempos_espera[nome] = espera
        print(f"{nome} inicia em {tempo}, espera {espera}, processa por {duracao}")
        tempo += duracao

    media = sum(tempos_espera.values()) / len(transacoes)
    print(f"Tempo total: {tempo}, Média espera: {media:.2f}\n")


def sjf(transacoes):
    print("🏦 SJF (Shortest Job First):")
    tempo = 0
    tempos_espera = {}
    fila = transacoes[:]
    concluídas = []

    while fila:
        disponiveis = [t for t in fila if t[3] <= tempo]
        if not disponiveis:
            tempo += 1
            continue
        disponiveis.sort(key=lambda t: t[1])
        t = disponiveis[0]
        nome, duracao, _, chegada = t
        espera = tempo - chegada
        tempos_espera[nome] = espera
        print(f"{nome} inicia em {tempo}, espera {espera}, processa por {duracao}")
        tempo += duracao
        fila.remove(t)
        concluídas.append(t)

    media = sum(tempos_espera.values()) / len(concluídas)
    print(f"Tempo total: {tempo}, Média espera: {media:.2f}\n")


def prioridade(transacoes):
    print("🏦 Prioridade (menor número = mais urgente):")
    tempo = 0
    tempos_espera = {}
    fila = transacoes[:]

    while fila:
        disponiveis = [t for t in fila if t[3] <= tempo]
        if not disponiveis:
            tempo += 1
            continue
        disponiveis.sort(key=lambda t: t[2])  # menor prioridade = maior urgência
        t = disponiveis[0]
        nome, duracao, prioridade, chegada = t
        espera = tempo - chegada
        tempos_espera[nome] = espera
        print(f"{nome} (Prioridade {prioridade}) inicia em {tempo}, espera {espera}, processa por {duracao}")
        tempo += duracao
        fila.remove(t)

    media = sum(tempos_espera.values()) / len(transacoes)
    print(f"Tempo total: {tempo}, Média espera: {media:.2f}\n")



# Simulação
print("=== Simulação Bancária de Agendamento de Transações ===\n")
fcfs(copy.deepcopy(transacoes_base))
sjf(copy.deepcopy(transacoes_base))
prioridade(copy.deepcopy(transacoes_base))

