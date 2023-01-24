
import pickle
from config import *
from nltk import SnowballStemmer

from UncompressedPostings import UncompressedPostings
from generadorTermIDdocID import generarIndiceTodosLosBloques,guardarEnDisco

stemmer = SnowballStemmer("spanish")
diccionario = parsear("config.ini")
dicc_termID = {}
doc_id_list = []
doc_id_list_comp = ""

def generarIndiceFinal():
    lista_dicc = []

    for medio in diccionario:
        nombre = medio+".p"
        dicc = pickle.load(open(nombre,"rb"))
        lista_dicc.append(dicc)

    dicc_final = mergeDict(lista_dicc)
    guardarEnDisco(dicc_final, "indice_final")

    return dicc_final

def generarTuplasConMetadataYListaFinal(dicc_final):

    global doc_id_list

    dicc_bsbi = {}
    pos_inicial = 0

    for term in dicc_final:
        cant_doc = len(dicc_final[term])
        coded = UncompressedPostings.encode(dicc_final[term])
        long_archivo = len(coded)
        dicc_bsbi[term] = (pos_inicial, cant_doc, long_archivo)
        pos_inicial += long_archivo
        doc_id_list.append(coded)

    doc_id_list = b"".join(doc_id_list)

    guardarEnDisco(dicc_bsbi, "dicc_final_bsbi")
    guardarEnDisco(doc_id_list, "doc_id_list")

def indiceInvertidoListaComprimida(dicc_final_comprimido):

    global doc_id_list_comp

    dicc_bsbi_comp = {}
    pos_inicial = 0

    for term in dicc_final_comprimido:
        cant_doc = len(dicc_final_comprimido[term])
        bloque = " ".join(dicc_final_comprimido[term])
        long_archivo = len(bloque)

        dicc_bsbi_comp[term] = (pos_inicial,cant_doc,long_archivo)
        pos_inicial += long_archivo+1
        doc_id_list_comp+= bloque+ " "

    guardarEnDisco(dicc_bsbi_comp, "dicc_final_bsbi_comp")
    guardarEnDisco(doc_id_list_comp, "doc_id_list_comp")

def mergeDict(dictlist):

    dict_final = {}

    for dict in dictlist:
        for key in dict.keys():

            dict[key] = UncompressedPostings.decode(dict[key])
            dict_final.setdefault(key,[])
            dict_final[key] += dict[key]

    return dict_final
