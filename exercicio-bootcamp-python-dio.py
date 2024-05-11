
# Desafio da criação de um sistema Bancário, criando modelo de classes ao invez de dicionário

from abc import ABC, abstractmethod, abstractproperty

class Conta:
    def __init__(self, saldo, numero, agencia, cliente):
        #foram criadas instâncias privadas, que são seguidas do underline.
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()


    # Após isso vamos criar os métodos a serem usados nessa classe :
    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\n Operação Falhou! SALDO INSUFICIENTE')
            
        elif valor > 0:
            self._saldo -= valor
            print('\n  Saque realizado Com  Sucesso!')
            return True
        
        else:
            print('\n Operação falhou! O valor informado é invalido')

        return False
        

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n Depósito realizado com sucesso!')
        
        else:
            print('\n Operação Falhou!')
            return False
        
        return True



class ContaCorrente(Conta): # Esta classe herdará da classe Conta.
    
    def __init__(self,numero,cliente, limite=500, limite_saques=3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques = limite_saques


    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
            )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('\n Operação falhou! Ovalor do saque excede o limite de 500 reais')

        elif excedeu_saques:
            print('\n Operação falhou!, Numero máximo de Saques excedidos, que são 3')

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\ Agência \t{self.agencia}C/C:\t\t{self.numero}Titular:\t{self.cliente.nome}"""
    


class Cliente:
    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = []


    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
        })

class Transacao(ABC):
    

    @property
    @abstractproperty
    def valor(self):
        ...


    @abstractmethod
    def registrar(conta):
        ...


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



    
