from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date, timedelta

def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        results = session.exec(statement).all()
        if results:
            print('Já existe uma conta nesse banco!!')
            return
        session.add(conta)
        session.commit()

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        result = session.exec(statement).first()
        if result.valor > 0:
            raise ValueError('Essa conta ainda possui saldo!!')
        result.status = Status.INATIVO
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_conta_saida)
        conta_saida = session.exec(statement).first()
        if conta_saida.valor < valor:
            raise ValueError('Saldo insuficiente!!')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()

        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        if conta.status == Status.INATIVO:
            raise ValueError('A conta está Inativa!!')
        
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError('Saldo Insuficiente!!')
            conta.valor -= historico.valor
        session.add(historico)
        session.commit()
        return historico

def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        total = 0
        for conta in contas:
            total += conta.valor
        return float(total)

def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        resultados = session.exec(statement).all()
        return resultados

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = [i.banco.value for i in contas]
        total = [i.valor for i in contas]
        import matplotlib.pyplot as plt
        plt.bar(bancos, total)
        plt.show()

    
#conta = Conta(valor=10, banco=Bancos.INTER)    
#criar_conta(conta)
#print(listar_contas())
#desativar_conta(1)
#transferir_saldo(1,2,10)
#historico = Historico(conta_id=1, tipos = Tipos.ENTRADA, valor=10, data=date.today())
#movimentar_dinheiro(historico)
#buscar_historico_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1))
#criar_grafico_por_conta()
