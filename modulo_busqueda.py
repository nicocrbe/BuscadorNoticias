from inverted_index_BSBI import *
from generadorTermIDdocID import *
from compressed_index import *
from newsCollector import *
from config import *
import collections
import pickle
from nltk import SnowballStemmer

stemmer = SnowballStemmer("spanish")


def buscarPalabra(palabra, compresion):

    if len(palabra)<3:
        return


    pal_norm = normalizarPalabras(palabra)
    pal_stem = stemmer.stem(pal_norm)

    dicc_termID = pickle.load(open("dicc_termID.p", "rb"))
    todasLasPalabras = dicc_termID.keys()


    if pal_stem not in todasLasPalabras:
        print("La palabra "+ palabra +" no esta en ninguna noticia")
        return
    else:
        term_id = dicc_termID[pal_stem]

    if compresion == "sin_comp":

        lista_doc_id = pickle.load(open("doc_id_list.p", "rb"))
        dicc_bsbi = pickle.load(open("dicc_final_bsbi.p", "rb"))

        pos_inicial = dicc_bsbi[term_id][0]
        length = dicc_bsbi[term_id][2]
        pos_final = pos_inicial + length


        doc_id_list_word = UncompressedPostings.decode(lista_doc_id[pos_inicial:pos_final])

    elif compresion == "comp":

        dicc_bsbi_comp = pickle.load(open("dicc_final_bsbi_comp.p", "rb"))
        lista_doc_id_comp = pickle.load(open("doc_id_list_comp.p", "rb"))

        pos_inicial = dicc_bsbi_comp[term_id][0]
        length = dicc_bsbi_comp[term_id][2]
        pos_final = pos_inicial + length


        lista = lista_doc_id_comp[pos_inicial:pos_final].split()
        doc_id_list_word = descomprimirLista(lista)

    return doc_id_list_word

def mostrarDondeEsta(doc_id_list):

    claves_medios_inv = pickle.load(open("claves_medios_inv.p", "rb"))

    list_ret=[]

    if doc_id_list == None:
        return
    else:
        for id in doc_id_list:

            docID = str(id)
            num_medio = docID[0]
            num_seccion = docID[1]
            id_1 = docID[2:]

            id = id_1.lstrip("+0")


            medio = claves_medios_inv[int(num_medio)]
            seccion = claves_secciones_inv[int(num_seccion)]


            carpeta = medio + "/" + seccion

            noticias = etree.parse(carpeta + "/" +medio+"-"+seccion+".xml")

            titulo_noticia_path = noticias.xpath("//item[@id="+id+"]/title")

            fecha_pub_path = noticias.xpath("//item[@id="+id+"]/pubDate")


            titulo = titulo_noticia_path[0].text
            fecha= fecha_pub_path[0].text

            if medio == 'AMBITO-FINANCIERO':
                fecha_creada = str(crearFechaAmbito(fecha))
            else:
                fecha_creada = str(crearFecha(fecha))

            if medio == "LA-VOZ" or medio == "AMBITO-FINANCIERO":
                titulo = titulo.strip()


            retorno = "MEDIO: "+ medio+", SECCION: "+seccion+", ID: "+id+", TITULO: "+titulo+", FECHA Y HORA: "+fecha_creada

            list_ret.append(retorno)

    return list_ret

def buscarYMostrarCadaPalabra(frase,compresion):
    try:
        if frase == "":
            print("No se ingreso ninguna palabra")
            return
        frase = frase.split()

        for palabra in frase:
            if len(palabra)<3:
                raise Exception()
            lista = mostrarDondeEsta(buscarPalabra(palabra,compresion))
            if len(lista) > 1:
                print("La palabra " + palabra + " aparece en las siguientes noticias:\n")
                for x in lista:
                    print(x)
            print("\n ====================================================================================\n")
    except:
        print("Todas las palabras ingresadas deben tener mas de tres caracteres")


def buscarFraseTodaJunta(frase,compresion):
    try:
        if frase == "":
            print("No se ingreso ninguna palabra")
            return
        frase = frase.split()
        listaAux = []
        listaIDiguales = []
        cant_palabras = len(frase)

        for palabra in frase:
            if len(palabra)<3:
                raise Exception()
            lista = mostrarDondeEsta(buscarPalabra(palabra,compresion))
            if lista == None:
                return
            for x in lista:
                listaAux.append(x)

        for x, y in collections.Counter(listaAux).items():
            if y >= cant_palabras:
                listaIDiguales.append(x)

        if len(listaIDiguales) == 0:
            print("No se encontraron coincidencias")
        else:
            print("Los resultados encontrados son: ")

            for noticia in listaIDiguales:
                print(noticia)
    except:
        print("Todas las palabras deben tener mas de 3 caracteres")
