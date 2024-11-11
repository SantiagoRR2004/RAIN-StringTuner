import unittest
import guitars
import numpy as np


class test_guitar(unittest.TestCase):
    def test_tune_different_lengths(self):
        """
        Verifica que se puede afinar la guitarra con diferentes longitudes
        y que cada intento termina dentro de un tiempo límite.
        """
        # Valores de longitud para probar
        lengths = [length for length in np.arange(0.25, 1.2, 0.05)]
        tiempo_limite = 5  # tiempo límite por ejecución en segundos
        valores_no_terminados = []  # para almacenar longitudes que fallan

        for length in lengths:
            guitar = guitars.ClassicalGuitar(length=length)
            print(f"Prueba con length {length}")
            try:
                guitar.tune(timeLimit=tiempo_limite)
                print(f"Prueba con length {length} completada en tiempo")
            except TimeoutError:
                valores_no_terminados.append(length)
                print(f"Prueba con length {length} no completada en tiempo")

        if valores_no_terminados:
            self.fail(f"La función no terminó en el tiempo estipulado para los valores: {valores_no_terminados}")
        else:
            print("La función terminó en el tiempo estipulado para todos los valores.")

# Ejecución del test
if __name__ == "__main__":
    unittest.main()
