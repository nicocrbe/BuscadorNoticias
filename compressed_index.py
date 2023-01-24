import pickle

def prepend(lista, numero):
    lista.insert(0,numero)

def comprobarYRellenar(numero):

    num_final = ""
    tamanio = len(numero)

    if tamanio<=7:
        num_final += "1" + numero.zfill(7)
    else:
        while not tamanio%8==0:
            tamanio = tamanio+1
        num_final += numero.zfill(tamanio)

    return num_final


def pasarADecimal(numero_adaptado):
    decimal = 0
    for digito in numero_adaptado:
        decimal = decimal*2 + int(digito)
    return decimal

def codificar(numero):

    lista = []
    binario = bin(numero)[2:]

    es_conj_final = True

    for x in reversed(binario):

        if (len(lista)+1)%8 == 0:

            if es_conj_final:
                prepend(lista,"1")
                es_conj_final = False
            else:
                prepend(lista,"0")

        prepend(lista,x)

    numero = "".join(lista)
    numero_adaptado = comprobarYRellenar(numero)

    return numero_adaptado

def decodificar(numero):

    lista = []

    for x in range(0,len(numero)):
        if (x%8)!=0:
            lista.append(numero[x])

    num_a_string = "".join(lista)
    numero_adaptado = num_a_string.lstrip("+0")

    decimal = pasarADecimal(numero_adaptado)

    return int(decimal)

def indiceListaApariciones():
    indice = pickle.load(open("indice_final.p","rb"))
    terminos = indice.keys()

    for term in terminos:
        lista = indice[term]
        indice[term] = comprimirLista(lista)
    guardarEnDisco(indice, "indice_comprimido_aux")
    return indice

def comprimirLista(lista_docs):

    lista_docs.sort()
    lista_comprimida = []

    primer_elemento = lista_docs[0]
    lista_comprimida.append(codificar(primer_elemento))

    for n in range(0, len(lista_docs) - 1):
        salto = (lista_docs[n + 1]) - lista_docs[n]
        lista_comprimida.append(codificar(salto))

    return lista_comprimida

def descomprimirLista(lista):
    lista_dec = []
    primer_elemento = decodificar(lista[0])
    lista_dec.append(primer_elemento)
    salto_acumulado = 0

    for x in range(1,len(lista)):

        salto_acumulado+= decodificar(lista[x])
        numero = primer_elemento + salto_acumulado

        lista_dec.append(numero)
    return lista_dec

def guardarEnDisco(indice, nombre_arch):
    pickle.dump(indice, open(nombre_arch+".p","wb"))
