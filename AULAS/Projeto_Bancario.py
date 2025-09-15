class ContaBancaria:
    def __init__(self):
        self.saldo = 0.0
        self.depositos = []
        self.saques = []
        self.saques_hoje = 0
        self.limite_saque = 500.0
        self.max_saques_diarios = 3
    
    def depositar(self, valor):
        if valor <= 0:
            print("❌ Erro: O valor do depósito deve ser positivo.")
            return False
        
        self.saldo += valor
        self.depositos.append(valor)
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True
    
    def sacar(self, valor):
        # Verificar se excedeu o número máximo de saques diários
        if self.saques_hoje >= self.max_saques_diarios:
            print("❌ Erro: Limite máximo de 3 saques diários atingido.")
            return False
        
        # Verificar se o valor excede o limite por saque
        if valor > self.limite_saque:
            print(f"❌ Erro: O valor máximo por saque é R$ {self.limite_saque:.2f}.")
            return False
        
        # Verificar se há saldo suficiente
        if valor > self.saldo:
            print("❌ Erro: Saldo insuficiente para realizar o saque.")
            return False
        
        # Realizar o saque
        self.saldo -= valor
        self.saques.append(valor)
        self.saques_hoje += 1
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        print(f"💰 Saques restantes hoje: {self.max_saques_diarios - self.saques_hoje}")
        return True
    
    def extrato(self):
        print("\n" + "="*50)
        print("📋 EXTRATO BANCÁRIO")
        print("="*50)
        
        # Exibir depósitos
        if self.depositos:
            print("\n📥 DEPÓSITOS:")
            for i, deposito in enumerate(self.depositos, 1):
                print(f"   {i}. R$ {deposito:.2f}")
        else:
            print("\n📥 Nenhum depósito realizado.")
        
        # Exibir saques
        if self.saques:
            print("\n📤 SAQUES:")
            for i, saque in enumerate(self.saques, 1):
                print(f"   {i}. R$ {saque:.2f}")
        else:
            print("\n📤 Nenhum saque realizado.")
        
        # Exibir saldo atual
        print("\n" + "-"*50)
        print(f"💰 SALDO ATUAL: R$ {self.saldo:.2f}")
        print(f"🎯 Saques realizados hoje: {self.saques_hoje}/{self.max_saques_diarios}")
        print("="*50 + "\n")
    
    def menu(self):
        while True:
            print("\n🏦 SISTEMA BANCÁRIO")
            print("1. Depósito")
            print("2. Saque")
            print("3. Extrato")
            print("4. Sair")
            
            opcao = input("\nEscolha uma opção (1-4): ")
            
            if opcao == "1":
                try:
                    valor = float(input("Digite o valor para depósito: R$ "))
                    self.depositar(valor)
                except ValueError:
                    print("❌ Erro: Digite um valor numérico válido.")
            
            elif opcao == "2":
                try:
                    valor = float(input("Digite o valor para saque: R$ "))
                    self.sacar(valor)
                except ValueError:
                    print("❌ Erro: Digite um valor numérico válido.")
            
            elif opcao == "3":
                self.extrato()
            
            elif opcao == "4":
                print("👋 Obrigado por usar nosso sistema bancário!")
                break
            
            else:
                print("❌ Opção inválida. Tente novamente.")

# Função principal
def main():
    print("Bem-vindo ao Sistema Bancário!")
    conta = ContaBancaria()
    conta.menu()

# Executar o programa
if __name__ == "__main__":
    main()