import unittest

from generadorTermIDdocID import *


class Test_newsCollector(unittest.TestCase):

    def test_generarIndiceError(self):
        lista = generarIndiceUnaSeccion('CLARIN', 'sociedad','testFiles/errorPrueba') #Se prueba una carpeta que contiene XML con formato incorrecto, devuelve una lista de items vacia y lanza la excepcion

        self.assertEqual([], lista)


if __name__ == '__main__':
	unittest.main()