import datetime
from typing import List, Dict, Any

# Listas globais para armazenamento
usuarios: List[Dict[str, Any]] = []
contas: List[Dict[str, Any]] = []
numero_conta_sequencial = 1
AGENCIA = "0001"

def cadastrar_usuario(nome: str, data_nascimento: str, cpf: str, endereco: str) -> bool:
    """
    Cadastra um novo usuário (cliente) no sistema.
    
    Args:
        nome: Nome completo do usuário
        data_nascimento: Data de nascimento no formato DD/MM/AAAA
        cpf: CPF (apenas números)
        endereco: Endereço no formato: logradouro, nro - bairro - cidade/sigla estado
    
    Returns:
        bool: True se o usuário foi cadastrado com sucesso, False caso contrário
    """
    global usuarios
    
    # Remover caracteres não numéricos do CPF
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    # Verificar se CPF já existe
    for usuario in usuarios:
        if usuario['cpf'] == cpf_limpo:
            print("❌ Erro: Já existe um usuário cadastrado com este CPF.")
            return False
    
    # Criar novo usuário
    novo_usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf_limpo,
        'endereco': endereco
    }
    
    usuarios.append(novo_usuario)
    print(f"✅ Usuário {nome} cadastrado com sucesso!")
    return True

def cadastrar_conta_bancaria(cpf_usuario: str) -> bool:
    """
    Cadastra uma nova conta corrente para um usuário.
    
    Args:
        cpf_usuario: CPF do usuário para vincular à conta
    
    Returns:
        bool: True se a conta foi cadastrada com sucesso, False caso contrário
    """
    global contas, numero_conta_sequencial
    
    # Remover caracteres não numéricos do CPF
    cpf_limpo = ''.join(filter(str.isdigit, cpf_usuario))
    
    # Verificar se usuário existe
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf_limpo:
            usuario_encontrado = usuario
            break
    
    if not usuario_encontrado:
        print("❌ Erro: Usuário não encontrado. Cadastre o usuário primeiro.")
        return False
    
    # Criar nova conta
    nova_conta = {
        'agencia': AGENCIA,
        'numero_conta': numero_conta_sequencial,
        'usuario': usuario_encontrado,
        'saldo': 0.0,
        'depositos': [],
        'saques': [],
        'saques_hoje': 0,
        'ultima_data': datetime.date.today(),
        'limite_saque': 500.0,
        'max_saques_diarios': 3
    }
    
    contas.append(nova_conta)
    print(f"✅ Conta {numero_conta_sequencial} criada com sucesso para {usuario_encontrado['nome']}!")
    numero_conta_sequencial += 1
    return True

def depositar(valor, /) -> bool:
    """
    Realiza um depósito na conta.
    
    Args (positional only):
        valor: Valor a ser depositado (deve ser positivo)
    
    Returns:
        bool: True se o depósito foi realizado com sucesso, False caso contrário
    """
    if len(contas) == 0:
        print("❌ Erro: Nenhuma conta cadastrada.")
        return False
    
    # Usando a primeira conta (poderia ser extendido para múltiplas contas)
    conta = contas[0]
    
    if valor <= 0:
        print("❌ Erro: O valor do depósito deve ser positivo.")
        return False
    
    conta['saldo'] += valor
    conta['depositos'].append((valor, datetime.datetime.now()))
    print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    return True

def sacar(*, valor) -> bool:
    """
    Realiza um saque na conta.
    
    Args (keyword only):
        valor: Valor a ser sacado
    
    Returns:
        bool: True se o saque foi realizado com sucesso, False caso contrário
    """
    if len(contas) == 0:
        print("❌ Erro: Nenhuma conta cadastrada.")
        return False
    
    conta = contas[0]
    
    # Verificar data para resetar saques diários
    hoje = datetime.date.today()
    if hoje > conta['ultima_data']:
        conta['saques_hoje'] = 0
        conta['ultima_data'] = hoje
    
    # Verificar limites
    if conta['saques_hoje'] >= conta['max_saques_diarios']:
        print("❌ Erro: Limite máximo de 3 saques diários atingido.")
        return False
    
    if valor > conta['limite_saque']:
        print(f"❌ Erro: O valor máximo por saque é R$ {conta['limite_saque']:.2f}.")
        return False
    
    if valor > conta['saldo']:
        print("❌ Erro: Saldo insuficiente para realizar o saque.")
        return False
    
    # Realizar saque
    conta['saldo'] -= valor
    conta['saques'].append((valor, datetime.datetime.now()))
    conta['saques_hoje'] += 1
    print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
    print(f"💰 Saques restantes hoje: {conta['max_saques_diarios'] - conta['saques_hoje']}")
    return True

def extrato(saldo_anterior=0.0, /, *, exibir_detalhes=True) -> tuple:
    """
    Exibe o extrato bancário.
    
    Args:
        saldo_anterior: Saldo anterior para comparação (positional only)
        exibir_detalhes: Se deve exibir detalhes das transações (keyword only)
    
    Returns:
        tuple: (saldo_atual, total_depositos, total_saques)
    """
    if len(contas) == 0:
        print("❌ Erro: Nenhuma conta cadastrada.")
        return (0.0, 0.0, 0.0)
    
    conta = contas[0]
    
    if exibir_detalhes:
        print("\n" + "="*50)
        print("📋 EXTRATO BANCÁRIO")
        print("="*50)
        
        # Depósitos
        if conta['depositos']:
            print("\n📥 DEPÓSITOS:")
            for i, (deposito, data) in enumerate(conta['depositos'], 1):
                print(f"   {i}. R$ {deposito:.2f} - {data.strftime('%d/%m/%Y %H:%M')}")
        else:
            print("\n📥 Nenhum depósito realizado.")
        
        # Saques
        if conta['saques']:
            print("\n📤 SAQUES:")
            for i, (saque, data) in enumerate(conta['saques'], 1):
                print(f"   {i}. R$ {saque:.2f} - {data.strftime('%d/%m/%Y %H:%M')}")
        else:
            print("\n📤 Nenhum saque realizado.")
        
        print("\n" + "-"*50)
    
    saldo_atual = conta['saldo']
    total_depositos = sum(deposito for deposito, _ in conta['depositos'])
    total_saques = sum(saque for saque, _ in conta['saques'])
    
    if exibir_detalhes:
        print(f"💰 SALDO ANTERIOR: R$ {saldo_anterior:.2f}")
        print(f"💰 SALDO ATUAL: R$ {saldo_atual:.2f}")
        print(f"📥 TOTAL DEPÓSITOS: R$ {total_depositos:.2f}")
        print(f"📤 TOTAL SAQUES: R$ {total_saques:.2f}")
        print(f"🎯 Saques realizados hoje: {conta['saques_hoje']}/{conta['max_saques_diarios']}")
        print("="*50 + "\n")
    
    return (saldo_atual, total_depositos, total_saques)

def listar_usuarios():
    """Lista todos os usuários cadastrados."""
    if not usuarios:
        print("📝 Nenhum usuário cadastrado.")
        return
    
    print("\n" + "="*50)
    print("👥 USUÁRIOS CADASTRADOS")
    print("="*50)
    
    for i, usuario in enumerate(usuarios, 1):
        print(f"\n{i}. Nome: {usuario['nome']}")
        print(f"   Data Nasc.: {usuario['data_nascimento']}")
        print(f"   CPF: {usuario['cpf']}")
        print(f"   Endereço: {usuario['endereco']}")

def listar_contas():
    """Lista todas as contas cadastradas."""
    if not contas:
        print("🏦 Nenhuma conta cadastrada.")
        return
    
    print("\n" + "="*50)
    print("🏦 CONTAS CADASTRADAS")
    print("="*50)
    
    for conta in contas:
        print(f"\nAgência: {conta['agencia']} | Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})")
        print(f"Saldo: R$ {conta['saldo']:.2f}")

def menu_principal():
    """Menu principal do sistema bancário."""
    while True:
        print("\n" + "="*50)
        print("🏦 SISTEMA BANCÁRIO")
        print("="*50)
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Conta Bancária")
        print("3. Listar Usuários")
        print("4. Listar Contas")
        print("5. Depósito")
        print("6. Saque")
        print("7. Extrato")
        print("8. Sair")
        
        opcao = input("\nEscolha uma opção (1-8): ").strip()
        
        if opcao == "1":
            print("\n📝 CADASTRAR USUÁRIO")
            nome = input("Nome completo: ").strip()
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
            cpf = input("CPF: ").strip()
            endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()
            cadastrar_usuario(nome, data_nascimento, cpf, endereco)
        
        elif opcao == "2":
            print("\n🏦 CADASTRAR CONTA BANCÁRIA")
            if not usuarios:
                print("❌ Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
                continue
            
            cpf = input("CPF do usuário: ").strip()
            cadastrar_conta_bancaria(cpf)
        
        elif opcao == "3":
            listar_usuarios()
        
        elif opcao == "4":
            listar_contas()
        
        elif opcao == "5":
            print("\n📥 DEPÓSITO")
            try:
                valor = float(input("Valor do depósito: R$ "))
                depositar(valor)  # positional only
            except ValueError:
                print("❌ Erro: Digite um valor numérico válido.")
        
        elif opcao == "6":
            print("\n📤 SAQUE")
            try:
                valor = float(input("Valor do saque: R$ "))
                sacar(valor=valor)  # keyword only
            except ValueError:
                print("❌ Erro: Digite um valor numérico válido.")
        
        elif opcao == "7":
            print("\n📋 EXTRATO")
            # Demonstrando uso dos parâmetros positional only e keyword only
            saldo_anterior = contas[0]['saldo'] if contas else 0.0
            extrato(saldo_anterior, exibir_detalhes=True)  # positional e keyword
        
        elif opcao == "8":
            print("👋 Obrigado por usar nosso sistema bancário!")
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")

def main():
    """Função principal do sistema."""
    print("Bem-vindo ao Sistema Bancário Modularizado!")
    menu_principal()

if __name__ == "__main__":
    main()