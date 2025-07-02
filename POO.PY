from abc import ABC, abstractmethod
from datetime import datetime


# ===================== POO  =====================

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        elif valor <= 0:
            print("Operação falhou! Valor inválido.")
            return False
        else:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            return True
        else:
            print("Operação falhou! Valor inválido.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes
            if t["tipo"] == "Saque"
        ])

        if numero_saques >= self._limite_saques:
            print("Operação falhou! Limite de saques atingido.")
            return False
        elif valor > self._limite:
            print("Operação falhou! Valor acima do limite por saque.")
            return False
        return super().sacar(valor)

    def __str__(self):
        return f"""
Agência: {self.agencia}
Conta: {self.numero}
Titular: {self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": type(transacao).__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# ===================== SISTEMA PRINCIPAL =====================

clientes = []
contas = []

def localizar_cliente(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def criar_usuario():
    cpf = input("CPF (somente números): ").strip()
    if localizar_cliente(cpf):
        print("Já existe um cliente com esse CPF.")
        return

    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    cliente = Cliente(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    print("Usuário criado com sucesso!")


def criar_conta():
    cpf = input("Informe o CPF do cliente: ")
    cliente = localizar_cliente(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(numero_conta, cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("Conta criada com sucesso!")


def depositar():
    cpf = input("CPF do titular: ")
    cliente = localizar_cliente(cpf)

    if not cliente or not cliente.contas:
        print("Cliente não encontrado ou sem conta.")
        return

    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(cliente.contas[0], transacao)


def sacar():
    cpf = input("CPF do titular: ")
    cliente = localizar_cliente(cpf)

    if not cliente or not cliente.contas:
        print("Cliente não encontrado ou sem conta.")
        return

    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(cliente.contas[0], transacao)


def exibir_extrato():
    cpf = input("CPF do titular: ")
    cliente = localizar_cliente(cpf)

    if not cliente or not cliente.contas:
        print("Cliente não encontrado ou sem conta.")
        return

    conta = cliente.contas[0]
    print("\n========= EXTRATO =========")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("===========================\n")


def menu():
    print("""
    ========== BANCO POO ==========
    [1] Criar Usuário
    [2] Criar Conta
    [3] Depositar
    [4] Sacar
    [5] Extrato
    [6] Sair
    ===============================
    """)
    return input("Escolha uma opção: ")


# ===================== PRINCIPAL =====================

while True:
    opcao = menu()

    if opcao == "1":
        criar_usuario()
    elif opcao == "2":
        criar_conta()
    elif opcao == "3":
        depositar()
    elif opcao == "4":
        sacar()
    elif opcao == "5":
        exibir_extrato()
    elif opcao == "6":
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida, tente novamente.")
