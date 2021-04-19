#Programa em Python que lê a definição de um AFN de um XML e grava outro XML com o AFD correspondente

import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import Document
import urllib
import itertools


#Classe responsável por armazenar informações do autômato
class automato:
    def __init__(self, simbolos, estados, funcao_programa, estado_inicial, estados_finais):
        self.simbolos = simbolos
        self.estados = estados
        self.funcao_programa = funcao_programa
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais


# Função responsável por ler as informações do AFN de um XML
# Retorna um objeto da classe automato com as informações obtidas
def funcao_leitura(string):
    #ler xml e criar um AFN
    doc = minidom.parse(string)

    simbolos = doc.getElementsByTagName('simbolos')
    estados = doc.getElementsByTagName('estados')
    funcao_programa = doc.getElementsByTagName('funcaoPrograma')
    estado_inicial = doc.getElementsByTagName('estadoInicial')
    estados_finais = doc.getElementsByTagName('estadosFinais')

    a = [] 
    q = [] 
    f = [] 
    p = []

    # lê e armazena os simbolos do automato
    for child in simbolos:
        elements = child.getElementsByTagName('elemento')
        for element in elements:
            a.append(element.getAttribute('valor'))
    
    # lê e armazena os estados do automato
    for child in estados:
        elements = child.getElementsByTagName('elemento')
        for element in elements:
            q.append(element.getAttribute('valor'))
    
    # lê e armazena os estados finais do automato
    for child in estados_finais:
        elements = child.getElementsByTagName('elemento')
        for element in elements:
            f.append(element.getAttribute('valor'))

    # lê e armazena a função programa do automato
    for child in funcao_programa :
        elements = child.getElementsByTagName('elemento')
        for element in elements:
            p.append([element.getAttribute('origem'), element.getAttribute('destino'), element.getAttribute('simbolo')])
    
    # lê e armazena os estados iniciais do automato
    for child in estado_inicial:
        elements = child.getElementsByTagName('elemento')
        for element in elements:
            q1 = element.getAttribute('valor')

    # armazena os dados obtidos em um objeto da classe automato
    aut = automato(a, q, p, q1, f)
    return aut


# Função responsável por escrever em um arquivo XML as 
# informações referentes ao AFD obtido pela conversão do AFN
def funcao_escrita(afd):

    a= afd.simbolos
    q= afd.estados
    f= afd.estados_finais
    p= afd.funcao_programa
    q0= afd.estado_inicial
    
    doc = Document()

    base = doc.createElement('AFD')
    output = open("ADF.xml", "w")
    doc.appendChild(base)


    #escreve o alfabeto no XML
    simbolo = doc.createElement('simbolos')
    simbolosCopy = a.copy()
    for i in a:
        elementosValor = doc.createElement('elemento ')
        elementosValor.setAttribute("valor ", str(simbolosCopy.pop(0)))
        simbolo.appendChild(elementosValor)
    base.appendChild(simbolo)



    #escreve o conjunto de estados no XML
    estado = doc.createElement('estados')
    estadosCopy = q.copy()
    for i in q:
        line = ''.join(estadosCopy.pop(0))
        elementosValor = doc.createElement('elemento ')
        elementosValor.setAttribute("valor ", line)
        estado.appendChild(elementosValor)
    base.appendChild(estado)



    #escreve o conjunto de estados finais no XML
    estados_finais = doc.createElement('estadosFinais')
    estadosFinaisCopy = f.copy()
    for i in f:
        line = ''.join(estadosFinaisCopy.pop(0))
        elementosValor = doc.createElement('elemento ')
        elementosValor.setAttribute("valor " , line)
        estados_finais.appendChild(elementosValor)
    base.appendChild(estados_finais)



    #escreve a função programa no XML
    funcao_programa = doc.createElement('funcaoPrograma')
    funcaoProgramaCopy = p.copy()
    for i in p:
        elementosValor = doc.createElement('elemento ')
        var = funcaoProgramaCopy.pop(0)
        line_origem= ''.join(var[0])
        line_destino= ''.join(var[1])
        elementosValor.setAttribute("origem ", line_origem)
        elementosValor.setAttribute("destino ", line_destino)
        elementosValor.setAttribute("simbolo ", str(var[2]))
        funcao_programa.appendChild(elementosValor)
    base.appendChild(funcao_programa)


    #escreve o estado final no XML
    estadoInicial = doc.createElement('estado inicial ')
    estadoInicial.setAttribute('valor ', q0)
    base.appendChild(estadoInicial)


    doc.writexml(output, " ", " ", "\n", "UTF-8" )
    output.close()


# Função cuja finalidade é a impressão das propriedades de um
# objeto da classe automato
def imprime_automato(automato):
    print(automato.simbolos)
    print(automato.estados)
    print(automato.funcao_programa)
    print(automato.estado_inicial)
    print(automato.estados_finais)
    print('\n\n')


# Gera e retorna uma lista de combinações dos estados do AFN
# necessárias para combinação
def obter_combinacoes(estados):
    combinations = []
    aux = []

    for i in estados:
        aux.append(i)
        combinations.append(aux)
        aux = []

    for l in range(2, len(estados)+1):
        for i in itertools.combinations(estados, l):
            i = list(i)
            combinations.append(i)
    
    return combinations


# Percorre os estados do automato e retorna
# os estados finais
def obter_estados_finais(estados, estados_finais):
    finais = []

    for q in estados:
        for final in estados_finais:
            if final in q:
                finais.append(q)
    return finais


# Responsável por obter a função programa do AFD se baseando na função programa do AFN
# Utiliza como funções auxiliares os métodos:
# processar_simbolo, add_valores_diferentes, confere_estados_iguais
# Percorre os estados processando os resultados provenientes do AFN descartando os estados repetidos
def obter_funcao_programa(estado_inicial, programa, combinacoes, alfabeto):
    funcao_programa = []
    q_ = []
    fila = []
    estado = combinacoes[0]
    
    fila.append(estado)

    for i in range(len(combinacoes)):
        if not fila:
            break
        else:
            if(fila[0] not in q_):
                estado = fila[0]
                q_.append(estado)
                for simbolo in alfabeto:
                    destino = []

                    for local in estado:
                        destino_aux = processar_simbolo(local, simbolo, programa)
                        destino = add_valores_diferentes(destino_aux, destino)

                    if(len(destino) != 0):
                        objetivo = 0
                        while(confere_estados_iguais(destino, combinacoes[objetivo]) == False):
                            objetivo += 1
                        fila.append(combinacoes[objetivo])
                        funcao_programa.append([estado, combinacoes[objetivo], simbolo])
        fila.pop(0)

    return funcao_programa, q_


# Função de auxílio a obtenção da função programa do automato
# Processa o símbolo com relação aos estados do mesmo
def processar_simbolo(origem, simbolo, programa):
    destino = []

    for p in range(len(programa)):
        if(origem == programa[p][0] and simbolo == programa[p][2]):
            destino.append(programa[p][1])
    return destino



# Função de auxílio a obtenção da função programa do automato
# Processa o símbolo com relação aos estados do mesmo
def add_valores_diferentes(list_a, b):
    list_b = b
    for aux in list_a:
        if(aux not in list_b):
            list_b.append(aux)
    return b


# Recebe dois estados e retorna se ambos são ou não iguais
# Tem a finalidade de impedir erros na função programa devido 
# as combinações de estados realizadas
def confere_estados_iguais(a, b):
    aux = list(set(a).intersection(b))

    if((len(a) == len(b)) and (len(a) == len(aux))):
        return True
    else:
        return False


# Funcao responsável por chamar todos os métodos responsáveis pelas
# etapas da conversão de um AFN em AFD
# Recebe um objeto do tipo automato representando um AFN e retorna 
# outro objeto representando o AFD
def converte_afn_afd(afn):
    a_ = afn.simbolos
    q1_ = afn.estado_inicial
    combinacoes = obter_combinacoes(afn.estados)
    p_, q_ = obter_funcao_programa(q1_, afn.funcao_programa, combinacoes, a_)
    f_ = obter_estados_finais(q_, afn.estados_finais)

    afd = automato(a_, q_, p_, q1_, f_)
    return afd


# Função principal do programa, chama os métodos necessários para
# Ler o XML que contém os dados do AFN
# Armazenar os dados obtidos em um objeto da classe automato
# Converter o AFN obtido em um AFD
# Registrar os dados do AFD obtido em um arquivo XML
# Imprimir os dados referentes ao AFN e ao AFD
if __name__ == '__main__':
    afn = funcao_leitura('AFN01.XML')
    imprime_automato(afn)

    afd = converte_afn_afd(afn)
    imprime_automato(afd)

    funcao_escrita(afd)