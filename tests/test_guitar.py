import unittest
import guitars
import concurrent.futures
import numpy as np


class test_guitar(unittest.TestCase):
    def test_tune_different_lengths(self):
        """
        Verifica que se puede afinar la guitarra con diferentes longitudes
        y que cada intento termina dentro de un tiempo límite.
        """
        # Valores de longitud para probar
        lengths = [length for length in np.arange(0.3, 0.4, 0.05)]
        tiempo_limite = 5  # tiempo límite por ejecución en segundos
        valores_no_terminados = []  # para almacenar longitudes que fallan

        # Ejecuta cada afinación en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futuros = {
                executor.submit(guitars.ClassicalGuitar(length).tune): length for length in lengths
            }

            # Procesa cada futuro a medida que se complete o falle por tiempo
            for futuro in concurrent.futures.as_completed(futuros):
                valor = futuros[futuro]
                try:
                    futuro.result(timeout=tiempo_limite)
                    print(f"Prueba con length {valor} completada en tiempo")
                except concurrent.futures.TimeoutError:
                    valores_no_terminados.append(valor)
                    print(f"Prueba con length {valor} no completada en tiempo")

        # Verifica si todos los valores terminaron en el tiempo estipulado
        if valores_no_terminados:
            self.fail(f"La función no terminó en el tiempo estipulado para los valores: {valores_no_terminados}")
        else:
            print("La función terminó en el tiempo estipulado para todos los valores.")

# Ejecución del test
if __name__ == "__main__":
    unittest.main()
