from pysat.formula import IDPool
from pysat.formula import CNF
from pysat.solvers import Glucose3
import pandas

Atom = IDPool()
m = 1
valor = pandas.read_csv("../arquivoCSV/column_bin_3a_2p.csv", sep=',')
valor.index += 1

def EscrevendoValores(a, i, t):
    return (Atom.id(a + '-' + str(i + 1) + '-' + t))


def EscrevendoRegras(i, j):
    return Atom.id('C-' + str(i + 1) + '-' + str(j + 1))

def valoresPacientes(valor):
    pacientes=valor.shape[0]
    valorDasVariaveis = [tuple(x) for x in valor.values]
    valores = list(valor)
    return pacientes,valores,valorDasVariaveis

def regra1(m, valor):
    pacientes,valores,valorAtributos = valoresPacientes(valor)
    valor1 = []
    valor2 = []
    for i in range(m):
        for v in valores:
            if v != 'P':
                valor1=[]
                valor1.append(EscrevendoValores(v, i, 'p'))
                valor1.append(EscrevendoValores(v, i, 'n'))
                valor1.append(EscrevendoValores(v, i, 's'))
                valor2.append(valor1)

                valor1=[]
                valor1.append(-EscrevendoValores(v, i, 'p'))
                valor1.append(-EscrevendoValores(v, i, 'n'))
                valor2.append(valor1)

                valor1=[]
                valor1.append(-EscrevendoValores(v, i, 'p'))
                valor1.append(-EscrevendoValores(v, i, 's'))
                valor2.append(valor1)

                valor1=[]
                valor1.append(-EscrevendoValores(v, i, 'n'))
                valor1.append(-EscrevendoValores(v, i, 's'))
                valor2.append(valor1)

    return valor2

def regra2(m, valor):
    pacientes,valores,valor_atributos = valoresPacientes(valor)
    valor1 = []
    valor2 = []
    for i in range(m):
        valor1 = []
        for v in valores:
            if v != 'P':
                valor1.append(-EscrevendoValores(v, i, 's'))
        valor2.append(valor1)
    
    return valor2

def regra3(m, valor):
    pacientes,valores,valorAtributos = valoresPacientes(valor)
    valor1 = []
    valor2 = []
    for j in range(pacientes):
        if valorAtributos[j][valores.index('P')] == 0:
            for i in range(m):
                valor1 = []
                for v in valores:
                    if v != 'P':
                        if valorAtributos[j][valores.index(str(v))] == 1:
                            valor1.append(EscrevendoValores(v, i, 'n'))
                        else:
                            valor1.append(EscrevendoValores(v, i, 'p'))
                valor2.append(valor1)
    return valor2

def regra4(m, valor):
    pacientes,valores,valorAtributos = valoresPacientes(valor)
    valor1 = []
    valor2 = []
    for j in range(pacientes):
        if valorAtributos[j][valores.index('P')] == 1:
            for i in range(m):
                for v in valores:
                    valor1 = []
                    if v != 'P':
                        if valorAtributos[j][valores.index(str(v))] == 1:
                            valor1.append(-EscrevendoValores(v, i, 'n'))
                            valor1.append(-EscrevendoRegras(i, j))
                        else:
                            valor1.append(-EscrevendoValores(v, i, 'p'))
                            valor1.append(-EscrevendoRegras(i, j))
                        valor2.append(valor1)
    return valor2

def regra5(m, valor):
    pacientes,valores,valorAtributos = valoresPacientes(valor)
    valor1 = []
    valor2 = []
    for j in range(pacientes):
        valor1 = []
        if valorAtributos[j][valores.index('P')] == 1:
          for i in range(m):
                valor1.append(EscrevendoRegras(i, j))
          valor2.append(valor1)
    return valor2

def TodasAsRegras(m, valor, interpretacao):
    pacientes,valores,valorAtributos = valoresPacientes(valor)
    valor1 = []
    valor2 = []
    for i in range(m):
        valor1=[]
        for v in valores:
            if v != 'P':
                if (-EscrevendoValores(v, i, 's') in interpretacao):
                    if (EscrevendoValores(v, i, 'n') in interpretacao):
                        v2 = v.replace("<=", ">")
                        valor1.append(v2)
                    else:
                        valor1.append(v)
        valor2.append(str(valor1) + ' \u21E8 P')
    return valor2

f1 = regra1(m,valor)
f2 = regra2(m,valor)
f3 = regra3(m,valor)
f4 = regra4(m,valor)
f5 = regra5(m,valor)
fr = f1+f2+f3+f4+f5


if m > 0:
    solucao = Glucose3()
    solucao.append_formula(fr)

    if solucao.solve():
        print("Quantidade de regras Suficiente :)")
        Interpretacao = solucao.get_model()
        regras = TodasAsRegras(m,valor,Interpretacao)
        for r in regras:
            print(r)
    else:
        print("Quantidade de resgras Insuficiente :(")
else:
    print("A quantidade de regras tem que ser maior que 0 :(")
