import pickle
import sys
from exceptions import *
from configparser import ConfigParser, NoOptionError, DuplicateOptionError, MissingSectionHeaderError

cfg = ConfigParser()
dicc_portales = {}
tiempo = 0

claves_medios = {}
claves_medios_inv = {}

def parsear(nombre_config):
    global claves_medios
    global claves_medios_inv
    global dicc_portales
    try:
        cfg.read(nombre_config)
        i=1
        if cfg.sections()==[]:
            raise SinSeccionesException
        for medio in cfg.sections():
            dicc_urls = {}


            base = cfg.get(medio, "url_base")
            if base == "":

                raise DireccionVaciaException

            url_ult = cfg.get(medio, "ultimas")
            url_pol = cfg.get(medio, "politica")
            url_eco = cfg.get(medio, "economia")
            url_soc = cfg.get(medio, "sociedad")
            url_int = cfg.get(medio, "internacionales")

            if url_ult == "" or url_pol == "" or url_eco == "" or url_soc=="" or url_int=="":
                raise DireccionVaciaException

            ultimo = base + url_ult
            politica = base + url_pol
            economia = base + url_eco
            sociedad = base + url_soc
            internacionales = base + url_int



            dicc_urls["ultimas"] = ultimo
            dicc_urls["politica"] = politica
            dicc_urls["economia"] = economia
            dicc_urls["sociedad"] = sociedad
            dicc_urls["internacionales"] = internacionales

            claves_medios[medio] = i
            claves_medios_inv[i] = medio
            i+=1
            dicc_portales[medio] = dicc_urls

        pickle.dump(claves_medios,open("claves_medios.p","wb"))
        pickle.dump(claves_medios_inv, open("claves_medios_inv.p", "wb"))

    except OSError:
        print("Error al ingresar el archivo, verifique nombre y ruta")
    except SinSeccionesException:
        print("Debe ingresarse al menos una seccion")
    except DireccionVaciaException:
        print("URL Vacia")
    except TypeError:
        print("Tipo invalido")
    except NoOptionError:
        print("Error:", sys.exc_info()[1])
    except KeyError:
        print("Falta o es invalida una de las claves del dicc_urls")
    except NameError:
        print("Nombre invalido")
    except DuplicateOptionError:
        print("Seccion duplicada o se quito el nombre de un medio")
    except Exception:
        print("Error inesperado")


    return dicc_portales

def tiempoDefault(nombre_config):
    global tiempo
    try:
        cfg.read(nombre_config)

        tiempo = int(cfg.get('DEFAULT', 'query_interval'))
        if tiempo<0:
            raise IntervalMenorQueCero
    except IntervalMenorQueCero:
        tiempo = 400
        print("Query Interval debe ser un numero mayor a 0, por defecto sera 400")
    except MissingSectionHeaderError:
        print("Falta la seccion default")
    return tiempo

claves_secciones = {"ultimas": "1", "politica": "2", "economia": "3", "sociedad": "4", "internacionales": "5"}
claves_secciones_inv = {1: "ultimas", 2:"politica", 3:"economia",4: "sociedad", 5: "internacionales"}
meses = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11,
         "Dec": 12}
