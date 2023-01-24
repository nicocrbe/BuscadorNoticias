import signal
from modulo_busqueda import *
from compressed_index import *
from os import remove

indice_inv_creado = False
indice_inv_comp_creado = False
compresion_creada = False
noticias_procesadas = False


def menu_principal():

    global indice_inv_creado
    global indice_inv_comp_creado
    global compresion_creada
    global noticias_procesadas

    print("===========================================\n")
    print("Menú del sistema de noticias.", "\n")
    print("===========================================\n")
    print(" 1. Recolectar noticias")
    print(" 2. Procesar noticias")
    print(" 3. Crear indice invertido sin comprimir")
    print(" 4. Buscar palabras en noticias (Busqueda booleana OR)")
    print(" 5. Buscar palabras en noticias (Busqueda booleana AND)")
    print(" 6. Comprimir lista de apariciones")
    print(" 7. Crear indice invertido comprimido")
    print(" 8. Salir")
    print("\n")

    opcion = input("Ingrese un numero de opción: ")

    try:
        if int(opcion) in range(1,9):
            if opcion == "1":
                inicio_recopilacion()
                menu_principal()
            if opcion == "2":
                if noticias_procesadas == False:
                    print("Se estan procesando las noticias, el proceso tardara unos minutos\n")
                    generarIndiceTodosLosBloques()
                    generarIndiceFinal()
                    noticias_procesadas = True
                    print("Noticias procesadas con exito")
                    menu_principal()
                else:
                    print("Ya se procesaron las noticias")
                    menu_principal()
            if opcion == "3":
                if noticias_procesadas:
                    dicc_final = pickle.load(open("indice_final.p","rb"))
                    generarTuplasConMetadataYListaFinal(dicc_final)
                    indice_inv_creado = True
                    print("Indice creado con exito")
                    menu_principal()
                else:
                    print("Deben procesarse las noticias antes de crear el indice")
                    menu_principal()

            if opcion == "4":
                if indice_inv_creado or indice_inv_comp_creado:
                    eleccion_comp = input("¿Desea buscar utilizando indice invertido comprimido? (si/no)")
                    if eleccion_comp == "si":
                        if indice_inv_comp_creado:
                            compresion = "comp"
                            frase = input("Ingrese palabras a buscar, separadas por espacios")
                            buscarYMostrarCadaPalabra(frase,compresion)
                            menu_principal()
                        else:
                            print("No se creo un indice invertido comprimido")
                            menu_principal()
                    elif eleccion_comp=="no":
                        if indice_inv_creado:
                            compresion= "sin_comp"
                            frase = input("Ingrese palabras a buscar, separadas por espacios")
                            buscarYMostrarCadaPalabra(frase,compresion)
                            menu_principal()
                        else:
                            print("No se creo un indice invertido sin comprimir")
                            menu_principal()
                    else:
                        print("Opcion invalida, debe ingresarse si o no")
                        menu_principal()
                else:
                    print("No se crearon los indices invertidos")
                    menu_principal()
            if opcion == "5":
                if indice_inv_creado or indice_inv_comp_creado:
                    eleccion_comp = input("¿Desea buscar utilizando indice invertido comprimido? (si/no)")
                    if eleccion_comp == "si":
                        if indice_inv_comp_creado:
                            compresion = "comp"
                            frase = input("Ingrese palabras a buscar, separadas por espacios")
                            buscarFraseTodaJunta(frase, compresion)
                            menu_principal()
                        else:
                            print("No se creo un indice invertido comprimido")
                            menu_principal()
                    elif eleccion_comp == "no":
                        if indice_inv_creado:
                            compresion = "sin_comp"
                            frase = input("Ingrese palabras a buscar, separadas por espacios")
                            buscarFraseTodaJunta(frase, compresion)
                            menu_principal()
                        else:
                            print("No se creo un indice invertido sin comprimir")
                            menu_principal()
                    else:
                        print("Opcion invalida, debe ingresarse si o no")
                        menu_principal()
                else:
                    print("No se crearon los indices invertidos")
                    menu_principal()
            if opcion == "6":
                if noticias_procesadas:
                    indiceListaApariciones()
                    compresion_creada = True
                    print("Compresion realizada con exito")
                    menu_principal()
                else:
                    print("Deben procesarse las noticias antes de comprimir la lista")
                    menu_principal()
            if opcion == "7":
                if compresion_creada:
                    indice = pickle.load(open("indice_comprimido_aux.p", "rb"))
                    indiceInvertidoListaComprimida(indice)
                    indice_inv_comp_creado = True
                    print("Indice creado con exito")
                    menu_principal()
                else:
                    print("Debe comprimirse la lista de apariciones")
                    menu_principal()
            if opcion == "8":
                if noticias_procesadas:
                    remove("AMBITO-FINANCIERO.p")
                    remove("CLARIN.p")
                    remove("PERFIL.p")
                    remove("LA-VOZ.p")
                    remove("TELAM.p")
                    remove("dicc_termID.p")
                    remove("indice_final.p")
                if indice_inv_creado:
                    remove("dicc_final_bsbi.p")
                    remove("doc_id_list.p")
                if indice_inv_comp_creado:
                    remove("dicc_final_bsbi_comp.p")
                    remove("doc_id_list_comp.p")
                if compresion_creada:
                    remove("indice_comprimido_aux.p")
                return
        else:
            print('\n', "Opción inválida. Inténtelo de nuevo e ingrese el número de la opción que desea elegir.", "\n")
            menu_principal()
    except:
        print("Ocurrió un error al procesar la operación. Asegúrese de haber introducido los datos correctamente." + "\n")
        menu_principal()


def keyboard_interrupt(signal, frame):

    menu_principal()

    sys.exit(0)

signal.signal(signal.SIGINT, keyboard_interrupt)

if __name__ == "__main__":


    menu_principal()


