import unittest
from newsCollector import *

arbol_local = etree.parse('testFiles/totalPrueba/' + 'TELAM' + '-' + 'ultimas' + '.xml')
arbol_internet = etree.parse('testFiles/pruebaRepite1/' + 'TELAM' + '-' + 'ultimas' + '.xml')  # Largo 20

lista_noticias_guarda = arbol_local.xpath("//item")
lista_noticias_internet = arbol_internet.xpath("//item")
root = arbol_local.getroot()

class Test_newsCollector(unittest.TestCase):

    def test_eliminarRepetidos(self):


        listaSinRepetidos = eliminarNoticiasRepetidas(lista_noticias_internet,lista_noticias_guarda)


        self.assertEqual(19, len(listaSinRepetidos))

    def test_numerarMedioySeccion(self):

        numerarMedioYSeccion('TELAM','ultimas','testFiles/totalPrueba')
        numeroMedio = root.find("channel/medio")
        texto = numeroMedio.text

        self.assertEqual('1',texto)

    def test_IdNoticias(self):

        idNoticias('TELAM','ultimas','testFiles/totalPrueba')

        numero = lista_noticias_guarda[0].xpath("@id")
        lista = [str(len(lista_noticias_guarda))]

        self.assertEqual(lista,numero)



if __name__ == '__main__':
	unittest.main()
