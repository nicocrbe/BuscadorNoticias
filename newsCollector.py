import os
import pickle
from contextlib import contextmanager
from datetime import datetime
import requests
from lxml import etree
from config import parsear ,meses,claves_secciones ,tiempoDefault
import time
from exceptions import *

numerado = False
diccionario = parsear('config.ini')

def crearXmlDeMedios(medio, seccion ,link):
    try:
        resp = requests.get(link) # diccionario[medio][seccion] seria el link
        if resp == "":
            print('vacio')
        folder = os.getcwd() + '/tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)
        with _cd(folder):
            with open(medio + "-" + seccion + '.xml', 'wb') as f:
                 f.write(resp.content)
    except Exception:
        print('Url invalida',link)

def obtener_noticas():
    try:
        if diccionario == {}:
            raise DiccionarioVacioNoticias
        for medio in diccionario:
            for seccion in diccionario[medio]:
                crearXmlDeMedios(medio, seccion, diccionario[medio][seccion])
    except DiccionarioVacioNoticias:
        print('Diccionario vacio verifique el archivo config')


def eliminarNoticiasRepetidas(listaInternet, listaLocal):

    for x in listaLocal[0:200]:
        texto1 = x.findtext('title')
        tituloLocal = texto1.replace(" ", "")

        for y in listaInternet:
            texto2 = y.findtext('title')
            tituloInternet = texto2.replace(" ", "")


            if tituloInternet == tituloLocal:

                indice = listaInternet.index(y)
                listaInternet.__delitem__(indice)


    return listaInternet


@contextmanager
def _cd(newdir):
    prevdir = os.getcwd()

    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def actualizarXML(medio, seccion,carpeta):
    # Descarga las nuevas noticias y las agrega a los xml finales

    try:
        arbol_local = etree.parse(carpeta + '/'+ medio + '-' + seccion + '.xml')
        arbol_internet = etree.parse('tmp/' + medio + '-' + seccion + '.xml')

    except:
        print("No se pudo leer"+ medio + seccion)
        return

    lista_noticias_internet_inicial = arbol_internet.xpath("//item")


    lista_noticias_local = arbol_local.xpath("//item")


    lista_noticias_internet = eliminarNoticiasRepetidas(lista_noticias_internet_inicial, lista_noticias_local)

    if lista_noticias_internet:
        aux_fecha_ultima_noticia_texto = arbol_local.xpath("//item/pubDate")[0].text

        if medio == 'AMBITO-FINANCIERO':
            fecha_ult_noticia = crearFechaAmbito(aux_fecha_ultima_noticia_texto)
        else:
            fecha_ult_noticia = crearFecha(aux_fecha_ultima_noticia_texto)

        prox = lista_noticias_internet[0].find("pubDate").text
        root_local = arbol_local.getroot()

        if medio == 'AMBITO-FINANCIERO':
            fecha_prox = crearFechaAmbito(prox)
            root_local[0][4].text = prox
        else:
            fecha_prox = crearFecha(prox)
            if medio == 'LA-VOZ':
                root_local[0][0].text = prox.lstrip()

        i = 0

        while fecha_ult_noticia < fecha_prox and i <= len(lista_noticias_internet) - 1 :
            item = root_local.findall("channel/item")[i]

            if i == 0:
                item.addprevious(lista_noticias_internet[i])

            else:
                if i == 1:
                    agregar_despues = root_local.findall("channel/item")[0]
                    agregar_despues.addnext(lista_noticias_internet[i])

                else:
                    item.addprevious(lista_noticias_internet[i])

            i += 1
            folder = os.getcwd() + '/' +  carpeta
            if not os.path.exists(folder):
                os.makedirs(folder)
            with _cd(folder):
                arbol_local.write(medio + '-' + seccion + '.xml', encoding="utf8")
            if i != len(lista_noticias_internet) :
                prox = lista_noticias_internet[i].find("pubDate").text
                if medio == 'AMBITO-FINANCIERO':
                    fecha_prox = crearFechaAmbito(prox)
                else:
                    fecha_prox = crearFecha(prox)
        idNoticias(medio, seccion,carpeta)
        numerarMedioYSeccion(medio, seccion,carpeta)

    else:
        print('No hay actualizaciones'+ " "+ medio +" " +  seccion)


def crearFecha(elemento):
        elemento = elemento.lstrip()
        dia = int(elemento[5:7])
        mes = meses[elemento[8:11]]
        anio = int(elemento[12:16])
        horas = int(elemento[17:19])
        minutos = int(elemento[20:22])
        fechaParseada = datetime(anio, mes, dia, horas, minutos)
        return fechaParseada


def actualizarNoticias():
    obtener_noticas()
    for medio in diccionario:
        for seccion in diccionario[medio]:
            carpeta = medio + '/' + seccion
            actualizarXML(medio, seccion,carpeta)

def crearFechaAmbito(elemento):
    dia = int(elemento[8:10])
    mes = int(elemento[5:7])
    anio = int(elemento[0:4])
    horas = int(elemento[11:13])
    minutos = int(elemento[14:16])
    fechaParseada = datetime(anio, mes, dia, horas, minutos)
    return fechaParseada


def numerarMedioYSeccion(nombre_medio, nombre_seccion,carpeta):

    # Agrega en la descripccion el numero de medio y seccion

    claves_medios = pickle.load(open("claves_medios.p","rb"))

    arbol = etree.parse(carpeta + '/'+ nombre_medio + '-' + nombre_seccion + '.xml')
    root = arbol.getroot()
    r = root.find("channel/description")
    r2 = root.find("channel/medio")

    if(r2 == None):

        seccion = etree.Element("seccion")
        seccion.text = claves_secciones[nombre_seccion]
        r.addnext(seccion)
        medio = etree.Element("medio")
        medio.text = claves_medios[nombre_medio]
        r.addnext(medio)
        folder = os.getcwd() + '/' + carpeta
        if not os.path.exists(folder):
            os.makedirs(folder)
        with _cd(folder):
            arbol.write(nombre_medio + "-" + nombre_seccion + ".xml", encoding="utf8")




def inicio_recopilacion():
    actualizarNoticias()
    print("Noticias Actualizadas", time.ctime(), "\n")
    segundos = int(tiempoDefault("config.ini"))
    time.sleep(segundos)
    while True:
        inicio_recopilacion()

def idNoticias(medio, seccion,carpeta):

    # Numera cada noticia con un ID

    tree = etree.parse(carpeta + '/' + medio + '-' + seccion + '.xml')
    root = tree.getroot()
    cant_items = len(tree.xpath("//item"))
    for noticia in root.iter("item"):

        if noticia.xpath("@id") == []:
            noticia.set("id", str(cant_items))
            cant_items -= 1

            folder = os.getcwd() + '/'+carpeta
            if not os.path.exists(folder):
                os.makedirs(folder)
            with _cd(folder):
                tree.write(medio + "-" + seccion + ".xml", encoding="utf-8")
        else:
            return







