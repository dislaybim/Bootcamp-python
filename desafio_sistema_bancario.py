import textwrap

def exibir_menu():
    opcoes_menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes_menu))

def realizar_deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def realizar_saque(*, saldo, valor, extrato, limite, num_saques, limite_saques):
    saldo_insuficiente = valor > saldo
    limite_excedido = valor > limite
    saques_excedidos = num_saques >= limite_saques

    if saldo_insuficiente:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
    elif limite_excedido:
        print("\n@@@ Operação falhou! Valor do saque excede o limite. @@@")
    elif saques_excedidos:
        print("\n@@@ Operação falhou! Limite de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        num_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! Valor informado é inválido. @@@")
    return saldo, extrato

def mostrar_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Nenhuma movimentação registrada." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def adicionar_usuario(lista_usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = encontrar_usuario(cpf, lista_usuarios)

    if usuario_existente:
        print("\n@@@ Usuário com esse CPF já existe! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    lista_usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def encontrar_usuario(cpf, lista_usuarios):
    usuarios_filtrados = [usuario for usuario in lista_usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_nova_conta(agencia, numero_conta, lista_usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = encontrar_usuario(cpf, lista_usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, criação de conta encerrada! @@@")


def listar_todas_contas(lista_contas):
    for conta in lista_contas:
        detalhes = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(detalhes))


def main():
    LIMITE_SAQUES_DIARIO = 3
    AGENCIA_PADRAO = "0001"

    saldo_atual = 0
    limite_saque = 500
    extrato_bancario = ""
    total_saques = 0
    usuarios_cadastrados = []
    contas_bancarias = []

    while True:
        escolha = exibir_menu()

        if escolha == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo_atual, extrato_bancario = realizar_deposito(saldo_atual, valor, extrato_bancario)

        elif escolha == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo_atual, extrato_bancario = realizar_saque(
                saldo=saldo_atual,
                valor=valor,
                extrato=extrato_bancario,
                limite=limite_saque,
                num_saques=total_saques,
                limite_saques=LIMITE_SAQUES_DIARIO,
            )

        elif escolha == "e":
            mostrar_extrato(saldo_atual, extrato=extrato_bancario)

        elif escolha == "nu":
            adicionar_usuario(usuarios_cadastrados)

        elif escolha == "nc":
            numero_nova_conta = len(contas_bancarias) + 1
            nova_conta = criar_nova_conta(AGENCIA_PADRAO, numero_nova_conta, usuarios_cadastrados)

            if nova_conta:
                contas_bancarias.append(nova_conta)

        elif escolha == "lc":
            listar_todas_contas(contas_bancarias)

        elif escolha == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
