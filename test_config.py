from config import *
import unittest


class TestLeerConfig(unittest.TestCase):

    def test_config_vacio(self):
        print("\nTest config vacio\n")  # En este ejemplo dejo solo la seccion default y borro las demas, en caso de borrar totalmente el contenido, lanzaria la misma excepcion
        parsear("config_sin_secciones")

    def test_leer_url_vacia(self):
        print("\nTest url vacia\n")
        parsear("config_url_vacia")

    def test_falta_una_seccion(self):
        print("\nTest falta seccion\n")
        parsear("testFiles/config_falta_seccion")

    def test_falta_un_medio(self):
        print("\nTest borro un medio\n")
        parsear("testFiles/config_borrando_un_medio")

    def test_no_default(self):
        print("\nTest borro seccion default\n")
        tiempoDefault("testFiles/config_sin_default")

    def test_tiempo_default_negativo(self):
        print("\nTest tiempo default negativo\n")
        tiempoDefault("testFiles/config_default_negativo")


if __name__ == '__main__':
    unittest.main()

