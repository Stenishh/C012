import threading
import random

# =============================================================================
# Bloco 2: Criando nossa conta bancária com proteção usando semáforo
# =============================================================================
class ContaComProtecao:
    def __init__(self, saldo_inicial=1000):
        self.saldo = saldo_inicial
        self.total_sacado = 0
        self.semaforo = threading.Semaphore()  # Semáforo com 0 permissão (para proteger a seção crítica)
        
    def consultar_saldo(self):
        return self.saldo
    
    def sacar(self, valor):
        # Usando o semáforo para garantir que apenas uma thread acesse a seção crítica por vez
        with self.semaforo:
            if self.saldo >= valor:
                print(f"Thread {threading.current_thread().name}: Verificou saldo de R${self.saldo} para saque de R${valor}")
                
                saldo_atual = self.saldo
                self.saldo = saldo_atual - valor
                self.total_sacado += valor
                
                print(f"Thread {threading.current_thread().name}: Saque de R${valor} realizado. Novo saldo: R${self.saldo}")
                return True
            else:
                print(f"Thread {threading.current_thread().name}: Tentou sacar R${valor}, mas saldo insuficiente: R${self.saldo}")
                return False

"""
Classe ContaComProtecao:

- Agora a classe conta tem um semáforo chamado `semaforo`, que é usado para sincronizar o acesso ao método `sacar()`.
- O semáforo garante que apenas uma thread possa realizar o saque de cada vez, evitando race conditions.
"""

# =============================================================================
# Bloco 3: Função que simula um cliente do banco com proteção
# =============================================================================
def cliente_com_protecao(conta, nome, saques):
    """Função que simula as operações de um cliente no banco com proteção de semáforo"""
    print(f"Cliente {nome} entrou no banco")
    
    for i in range(saques):
        # Valores maiores para forçar sobrecarga
        valor = random.randint(300, 500)
        conta.sacar(valor)

"""
Função cliente_com_protecao:

Simula um cliente realizando saques com proteção de semáforo.
A função funciona de maneira similar ao código anterior, mas agora, com a proteção contra race conditions.
"""

# =============================================================================
# Bloco 4: Função que roda a simulação do banco com proteção
# =============================================================================
def demonstrar_sobrecarga_com_protecao():
    # Criar uma conta com saldo inicial
    conta = ContaComProtecao(saldo_inicial=1000)
    print(f"Saldo inicial da conta: R${conta.consultar_saldo()}")
    
    # Lista para armazenar as threads
    threads = []
    
    # Criar várias threads simulando clientes tentando sacar dinheiro simultaneamente
    num_clientes = 5
    saques_por_cliente = 2
    
    for i in range(num_clientes):
        t = threading.Thread(target=cliente_com_protecao, args=(conta, f"Cliente-{i+1}", saques_por_cliente), name=f"Cliente-{i+1}")
        threads.append(t)
    
    # Iniciar todas as threads
    for t in threads:
        t.start()
    
    # Aguardar todas as threads terminarem
    for t in threads:
        t.join()
    
    # Verificar o saldo final
    print("\n" + "="*60)
    print(f"Saldo inicial: R$1000")
    print(f"Total sacado: R${conta.total_sacado}")
    print(f"Saldo final: R${conta.consultar_saldo()}")
    
    # Análise dos resultados
    if conta.saldo < 0:
        print("\n SOBRECARGA DETECTADA: Saldo negativo!")
        print(f"O banco permitiu saques além do disponível devido à falta de sincronização.")
    elif conta.total_sacado > 1000:
        print("\n SOBRECARGA DETECTADA: Total sacado maior que o saldo inicial!")
        print(f"Os clientes conseguiram sacar R${conta.total_sacado} de uma conta com apenas R$1000.")
    print("="*60)

"""
Demonstração da Sobrecarga (Race Condition) com Proteção:

A função `demonstrar_sobrecarga_com_protecao` funciona de maneira semelhante à anterior, mas agora as operações de saque estão protegidas por um semáforo. Com isso, a condição de sobrecarga devido a race conditions deve ser evitada.
"""

# =============================================================================
# Bloco 5: Código principal que inicia tudo
# =============================================================================
if __name__ == "__main__":
    print("DEMONSTRAÇÃO DE SISTEMA BANCÁRIO COM PROTEÇÃO CONTRA SOBRECARGA\n")
    demonstrar_sobrecarga_com_protecao()
