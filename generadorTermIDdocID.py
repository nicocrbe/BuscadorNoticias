import pickle
import unicodedata
from lxml import etree
import re

from nltk import SnowballStemmer

from config import parsear

from UncompressedPostings import UncompressedPostings

stemmer = SnowballStemmer("spanish")
diccionario = parsear('config.ini')
dicc_termID = {}
doc_id_list = []
doc_id_list_comp = ""

def crearSetStopwords():
    set_stopwords = set()
    for line in open("stopwords_es.txt", "r", encoding="utf8"):
        palabra = line[0:-1]
        set_stopwords.add(palabra)
    return set_stopwords



def normalizarPalabras(palabra):

    pal_standar = ''.join(c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn')
    pal_standar = re.sub(r'\d+', '', pal_standar)
    return pal_standar.lower()


def convertirPalabraAid(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return (h + 0x80000000) & 0xFFFFFFFF - 0x80000000

def guardarEnDisco(indice, nombre_arch):
    pickle.dump(indice, open(nombre_arch+".p","wb"))


def generarTuplaTermIdDocId(item):
    global dicc_termID
    stop_words = crearSetStopwords()

    titulo = item[0].text  # palabras del titulo
    descripcion = item[3].text  # palabras de la descipcion

    if titulo != None and descripcion != None:
        all_words = titulo + " " + descripcion # todas las palabras de cada noticia
    else:
        all_words = ""
    lista_tuplas = []

    if all_words != "":
        for palabra in re.split(r"\W+|\s+", all_words):
            if palabra not in stop_words and len(palabra) >= 3:
                palabra_norm = normalizarPalabras(palabra)
                if palabra_norm != "":
                    palabra_stem = stemmer.stem(palabra_norm)

                    noticiaID = item.get('id')
                    docID = item.getparent().find("medio").text + \
                                     item.getparent().find("seccion").text
                    docID += noticiaID.zfill(6)

                    term_id = convertirPalabraAid(palabra_stem)

                    dicc_termID[palabra_stem] = term_id

                    lista_tuplas.append((term_id, int(docID)))
    return lista_tuplas


def generarIndiceUnaSeccion(bloque,seccion,carpeta):
    lista_tuplas = []

    try:
        tree = etree.parse(carpeta + "/"+bloque + "-" + seccion + ".xml")
        lista_items = tree.xpath("//item")


        for item in lista_items:
            lista_tuplas += generarTuplaTermIdDocId(item)
    except Exception:
        print('Formato XML incorrecto verique',bloque,seccion)


    return lista_tuplas


def generarIndiceUnBloque(bloque):
    lista_final = []
    for seccion in diccionario[bloque]:
        carpeta = bloque + "/" + seccion
        lista_final += generarIndiceUnaSeccion(bloque,seccion,carpeta)
    nombreArchivo = bloque
    return sorted(lista_final), nombreArchivo


def eliminarRepetidos(bloque):
    lista,nombreArchivo = generarIndiceUnBloque(bloque)
    dicc_final = {}
    for tupla in lista:

        term_id = tupla[0]
        doc_id = tupla[1]

        dicc_final.setdefault(term_id,[])
        dicc_final[term_id].append(doc_id)

    for key in dicc_final.keys():
        dicc_final[key] = UncompressedPostings.encode(set(sorted(dicc_final[key])))

    guardarEnDisco(dicc_final,nombreArchivo)

    return dicc_final

def generarIndiceTodosLosBloques():

    for bloque in diccionario:
        eliminarRepetidos(bloque)
    guardarEnDisco(dicc_termID, "dicc_termID")




