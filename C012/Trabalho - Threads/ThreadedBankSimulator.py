import threading
import random
import time

class ContaSemProtecao:
    def __init__(self, saldo_inicial=1000):
        self.saldo = saldo_inicial
        self.total_sacado = 0

    def consultar_saldo(self):
        return self.saldo

    def sacar(self, valor):
        if self.saldo >= valor:
            print("Thread", threading.current_thread().name, ": Verificou saldo de R$", self.saldo, "para saque de R$", valor)
            saldo_atual = self.saldo
            time.sleep(0.05)
            self.saldo = saldo_atual - valor
            self.total_sacado += valor
            print("Thread", threading.current_thread().name, ": Saque de R$", valor, "realizado. Novo saldo: R$", self.saldo)
            return True
        else:
            print("Thread", threading.current_thread().name, ": Tentou sacar R$", valor, "mas saldo insuficiente: R$", self.saldo)
            return False

def executar_saque_concorrente(conta, num_saques):
    for _ in range(num_saques):
        valor = random.randint(300, 500)
        conta.sacar(valor)

def demonstrar_sobrecarga():
    conta = ContaSemProtecao(saldo_inicial=1000)
    print("Saldo inicial da conta: R$", conta.consultar_saldo())

    threads = []
    num_threads = 10
    saques_por_thread = 3

    for i in range(num_threads):
        t = threading.Thread(target=executar_saque_concorrente, args=(conta, saques_por_thread), name="Cliente-" + str(i+1))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("============================================================")
    print("⚠️  RESULTADO DA SIMULAÇÃO:")
    print("Saldo inicial: R$", 1000)
    print("Total sacado: R$", conta.total_sacado)
    print("Saldo final:", "\033[91mR$" + str(conta.consultar_saldo()) + "\033[0m")

    if conta.saldo < 0:
        print("❗ RACE CONDITION DETECTADA: Saldo ficou NEGATIVO! Exemplo de erro grave em sistemas concorrentes.")
    elif conta.total_sacado > 1000:
        print("❗ RACE CONDITION DETECTADA: Foram sacados R$", conta.total_sacado, "de uma conta com apenas R$1000!")
    else:
        print("✅ Nenhuma inconsistência detectada.")
    print("============================================================")

if __name__ == "__main__":
    print("💣 DEMONSTRAÇÃO DE RACE CONDITION COM SALDO NEGATIVO 💣")
    demonstrar_sobrecarga()
