import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

# Interface Transacao
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classes concretas de Transacao
class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Classe Historico
class Historico:
    def __init__(self):
        self._transacoes: List[Transacao] = []
    
    @property
    def transacoes(self) -> List[Transacao]:
        return self._transacoes
    
    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.datetime.now()
        })

# Classe base Cliente
class Cliente(ABC):
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas: List[Conta] = []
    
    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)
    
    @property
    def contas(self) -> List['Conta']:
        return self._contas
    
    @property
    def endereco(self) -> str:
        return self._endereco

# Classe PessoaFisica
class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime.date, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def data_nascimento(self) -> datetime.date:
        return self._data_nascimento
    
    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"

# Classe base Conta
class Conta:
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        return cls(numero, cliente)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def historico(self) -> Historico:
        return self._historico
    
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("❌ Erro: O valor do saque deve ser positivo.")
            return False
        
        if valor > self.saldo:
            print("❌ Erro: Saldo insuficiente para realizar o saque.")
            return False
        
        self._saldo -= valor
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True
    
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("❌ Erro: O valor do depósito deve ser positivo.")
            return False
        
        self._saldo += valor
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

# Classe ContaCorrente (herda de Conta)
class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_hoje = 0
        self._ultima_data = datetime.date.today()
    
    def sacar(self, valor: float) -> bool:
        # Verificar se precisa resetar o contador diário
        hoje = datetime.date.today()
        if hoje > self._ultima_data:
            self._saques_hoje = 0
            self._ultima_data = hoje
        
        # Verificar limite de saques
        if self._saques_hoje >= self._limite_saques:
            print("❌ Erro: Limite máximo de saques diários atingido.")
            return False
        
        # Verificar limite por saque
        if valor > self._limite:
            print(f"❌ Erro: O valor máximo por saque é R$ {self._limite:.2f}.")
            return False
        
        # Chamar método da classe pai
        sucesso = super().sacar(valor)
        if sucesso:
            self._saques_hoje += 1
            print(f"💰 Saques restantes hoje: {self._limite_saques - self._saques_hoje}")
        
        return sucesso
    
    @property
    def limite(self) -> float:
        return self._limite
    
    @property
    def limite_saques(self) -> int:
        return self._limite_saques
    
    @property
    def saques_hoje(self) -> int:
        return self._saques_hoje

# Sistema Bancário
class SistemaBancario:
    def __init__(self):
        self._clientes: List[PessoaFisica] = []
        self._contas: List[Conta] = []
        self._numero_conta_sequencial = 1
    
    def cadastrar_cliente(self, cpf: str, nome: str, data_nascimento: str, endereco: str) -> bool:
        # Verificar se CPF já existe
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        for cliente in self._clientes:
            if cliente.cpf == cpf_limpo:
                print("❌ Erro: Já existe um cliente cadastrado com este CPF.")
                return False
        
        # Converter string para date
        try:
            data = datetime.datetime.strptime(data_nascimento, "%d/%m/%Y").date()
        except ValueError:
            print("❌ Erro: Formato de data inválido. Use DD/MM/AAAA.")
            return False
        
        # Criar novo cliente
        novo_cliente = PessoaFisica(cpf_limpo, nome, data, endereco)
        self._clientes.append(novo_cliente)
        print(f"✅ Cliente {nome} cadastrado com sucesso!")
        return True
    
    def cadastrar_conta_corrente(self, cpf: str) -> bool:
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Encontrar cliente
        cliente_encontrado = None
        for cliente in self._clientes:
            if cliente.cpf == cpf_limpo:
                cliente_encontrado = cliente
                break
        
        if not cliente_encontrado:
            print("❌ Erro: Cliente não encontrado.")
            return False
        
        # Criar nova conta
        nova_conta = ContaCorrente.nova_conta(cliente_encontrado, self._numero_conta_sequencial)
        cliente_encontrado.adicionar_conta(nova_conta)
        self._contas.append(nova_conta)
        
        print(f"✅ Conta {self._numero_conta_sequencial} criada com sucesso para {cliente_encontrado.nome}!")
        self._numero_conta_sequencial += 1
        return True
    
    def encontrar_conta_por_numero(self, numero: int) -> Optional[Conta]:
        for conta in self._contas:
            if conta.numero == numero:
                return conta
        return None
    
    def encontrar_cliente_por_cpf(self, cpf: str) -> Optional[PessoaFisica]:
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        for cliente in self._clientes:
            if cliente.cpf == cpf_limpo:
                return cliente
        return None
    
    def depositar(self, numero_conta: int, valor: float) -> bool:
        conta = self.encontrar_conta_por_numero(numero_conta)
        if not conta:
            print("❌ Erro: Conta não encontrada.")
            return False
        
        deposito = Deposito(valor)
        conta.cliente.realizar_transacao(conta, deposito)
        return True
    
    def sacar(self, numero_conta: int, valor: float) -> bool:
        conta = self.encontrar_conta_por_numero(numero_conta)
        if not conta:
            print("❌ Erro: Conta não encontrada.")
            return False
        
        saque = Saque(valor)
        conta.cliente.realizar_transacao(conta, saque)
        return True
    
    def extrato(self, numero_conta: int):
        conta = self.encontrar_conta_por_numero(numero_conta)
        if not conta:
            print("❌ Erro: Conta não encontrada.")
            return
        
        print("\n" + "="*50)
        print("📋 EXTRATO BANCÁRIO")
        print("="*50)
        print(f"Agência: {conta.agencia} | Conta: {conta.numero}")
        print(f"Cliente: {conta.cliente.nome}")
        
        # Exibir transações
        transacoes = conta.historico.transacoes
        if transacoes:
            print("\n📊 HISTÓRICO DE TRANSAÇÕES:")
            for i, transacao in enumerate(transacoes, 1):
                tipo = "📥 DEPÓSITO" if transacao['tipo'] == 'Deposito' else "📤 SAQUE"
                print(f"   {i}. {tipo} - R$ {transacao['valor']:.2f} - {transacao['data'].strftime('%d/%m/%Y %H:%M')}")
        else:
            print("\n📊 Nenhuma transação realizada.")
        
        print("\n" + "-"*50)
        print(f"💰 SALDO ATUAL: R$ {conta.saldo:.2f}")
        
        if isinstance(conta, ContaCorrente):
            print(f"🎯 Saques realizados hoje: {conta.saques_hoje}/{conta.limite_saques}")
            print(f"📈 Limite por saque: R$ {conta.limite:.2f}")
        
        print("="*50 + "\n")
    
    def listar_clientes(self):
        if not self._clientes:
            print("📝 Nenhum cliente cadastrado.")
            return
        
        print("\n" + "="*50)
        print("👥 CLIENTES CADASTRADOS")
        print("="*50)
        
        for i, cliente in enumerate(self._clientes, 1):
            print(f"\n{i}. Nome: {cliente.nome}")
            print(f"   CPF: {cliente.cpf}")
            print(f"   Data Nasc.: {cliente.data_nascimento.strftime('%d/%m/%Y')}")
            print(f"   Endereço: {cliente.endereco}")
            print(f"   Contas: {len(cliente.contas)}")
    
    def listar_contas(self):
        if not self._contas:
            print("🏦 Nenhuma conta cadastrada.")
            return
        
        print("\n" + "="*50)
        print("🏦 CONTAS CADASTRADAS")
        print("="*50)
        
        for conta in self._contas:
            print(f"\nAgência: {conta.agencia} | Conta: {conta.numero}")
            print(f"Titular: {conta.cliente.nome} (CPF: {conta.cliente.cpf})")
            print(f"Saldo: R$ {conta.saldo:.2f}")
            print(f"Tipo: {'Conta Corrente' if isinstance(conta, ContaCorrente) else 'Conta'}")

    def menu_principal(self):
        while True:
            print("\n" + "="*50)
            print("🏦 SISTEMA BANCÁRIO")
            print("="*50)
            print("1. Cadastrar Cliente")
            print("2. Cadastrar Conta Corrente")
            print("3. Listar Clientes")
            print("4. Listar Contas")
            print("5. Depósito")
            print("6. Saque")
            print("7. Extrato")
            print("8. Sair")
            
            opcao = input("\nEscolha uma opção (1-8): ").strip()
            
            if opcao == "1":
                print("\n📝 CADASTRAR CLIENTE")
                nome = input("Nome completo: ").strip()
                cpf = input("CPF: ").strip()
                data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
                endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()
                self.cadastrar_cliente(cpf, nome, data_nascimento, endereco)
            
            elif opcao == "2":
                print("\n🏦 CADASTRAR CONTA CORRENTE")
                if not self._clientes:
                    print("❌ Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
                    continue
                
                cpf = input("CPF do cliente: ").strip()
                self.cadastrar_conta_corrente(cpf)
            
            elif opcao == "3":
                self.listar_clientes()
            
            elif opcao == "4":
                self.listar_contas()
            
            elif opcao == "5":
                print("\n📥 DEPÓSITO")
                try:
                    numero_conta = int(input("Número da conta: "))
                    valor = float(input("Valor do depósito: R$ "))
                    self.depositar(numero_conta, valor)
                except ValueError:
                    print("❌ Erro: Digite valores numéricos válidos.")
            
            elif opcao == "6":
                print("\n📤 SAQUE")
                try:
                    numero_conta = int(input("Número da conta: "))
                    valor = float(input("Valor do saque: R$ "))
                    self.sacar(numero_conta, valor)
                except ValueError:
                    print("❌ Erro: Digite valores numéricos válidos.")
            
            elif opcao == "7":
                print("\n📋 EXTRATO")
                try:
                    numero_conta = int(input("Número da conta: "))
                    self.extrato(numero_conta)
                except ValueError:
                    print("❌ Erro: Digite um número de conta válido.")
            
            elif opcao == "8":
                print("👋 Obrigado por usar nosso sistema bancário!")
                break
            
            else:
                print("❌ Opção inválida. Tente novamente.")

def main():
    sistema = SistemaBancario()
    print("Bem-vindo ao Sistema Bancário em POO!")
    sistema.menu_principal()

if __name__ == "__main__":
    main()