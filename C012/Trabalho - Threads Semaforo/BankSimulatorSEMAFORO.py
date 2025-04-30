import threading
import random
import time

class ContaComSemaforo:
    def __init__(self, saldo_inicial=1000):
        self.saldo = saldo_inicial
        self.total_sacado = 0
        self.semaforo = threading.Semaphore()  # Semáforo binário (mutex)

    def consultar_saldo(self):
        return self.saldo

    def sacar(self, valor):
        self.semaforo.acquire()  # Início da seção crítica
        try:
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
        finally:
            self.semaforo.release()  # Fim da seção crítica

def executar_saque_concorrente(conta, num_saques):
    for _ in range(num_saques):
        valor = random.randint(300, 500)
        conta.sacar(valor)

def demonstrar_execucao_segura():
    conta = ContaComSemaforo(saldo_inicial=1000)
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
    print("✅ RESULTADO DA SIMULAÇÃO COM SEMÁFORO (SINCRONIZADO):")
    print("Saldo inicial: R$", 1000)
    print("Total sacado: R$", conta.total_sacado)
    print("Saldo final: R$", conta.consultar_saldo())

    if conta.saldo < 0:
        print("❌ ERRO: Saldo ficou NEGATIVO! Mesmo com semáforo, algo está errado.")
    elif conta.total_sacado > 1000:
        print("❌ ERRO: Foram sacados R$", conta.total_sacado, "de uma conta com apenas R$1000!")
    else:
        print("✅ Execução segura: Nenhuma inconsistência detectada.")
    print("============================================================")

if __name__ == "__main__":
    print("🔐 DEMONSTRAÇÃO COM SEMÁFORO: ACESSO SEGURO À CONTA")
    demonstrar_execucao_segura()
