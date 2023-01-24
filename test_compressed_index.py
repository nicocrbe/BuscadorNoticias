from compressed_index import *
import unittest

class TestCompresion(unittest.TestCase):

    def test_codificar_numero_que_entra_en_siete_bits(self):
        numero1 = 5
        print("\n Test codificar numero "+str(numero1)+"\n")
        self.assertEqual("10000101", codificar(numero1))

    def test_codificar_numero_que_requiere_mas_de_7_bits(self):
        numero2 = 214577
        print("\n Test codificar numero " + str(numero2) + "\n")
        self.assertEqual("000011010000110010110001",codificar(numero2))

    def test_decodificar_numero_que_requiere_7_bits(self):
        numero3="10000101"
        print("\n Test decodificar numero " + numero3 + "\n")
        self.assertEqual(5,decodificar(numero3))


    def test_decodificar_numero_que_requiere_mas_de_7_bits(self):
        numero4="000011010000110010110001"
        print("\n Test decodificar numero " + numero4+ "\n")
        self.assertEqual(214577,decodificar(numero4))

    def test_comprimir_lista(self):
        lista = [100, 130, 180, 2156, 2495]
        print("\n Test codificar y comprimir lista " + str(lista) + "\n")
        self.assertEqual(['11100100', '10011110', '10110010', '0000111110111000', '0000001011010011'],comprimirLista(lista))

    def test_descomprimir_lista(self):
        lista = ['11100100', '10011110', '10110010', '0000111110111000', '0000001011010011']
        print("\n Test decodificar y descomprimir lista " + str(lista) + "\n")
        self.assertEqual([100, 130, 180, 2156, 2495],descomprimirLista(lista))


if __name__ == '__main__':
    unittest.main()