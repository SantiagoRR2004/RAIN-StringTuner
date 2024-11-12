import logic

aceptance = ["sí", "vale", "ok", "afirmativo", "correcto", "de acuerdo", "s", "y", "si"]


if __name__ == "__main__":
    tuner = logic.Tuner()
    print("¡Bienvenido al afinador de cuerdas!")
    print("Este programa te ayudará a afinar su instrumento de cuerda.")

    response = input("¿Quiere afinar una cuerda? ")

    while response.lower() in aceptance:

        l = float(input("¿Qué longitud tiene la cuerda (en cm)? ")) / 100
        f = float(input("¿Qué frecuencia quiere para la cuerda (en Hz)? "))
        f1 = float(input("¿Qué frecuencia tiene la cuerda (en Hz)? "))

        response2 = "s"

        while response2.lower() in aceptance:
            t = tuner.tune(f, f1, l)

            if t >= 0:
                print(f"Aprite la cuerda {t} vueltas.")
            else:
                print(f"Afloje la cuerda {-t} vueltas.")

            response2 = input("¿Quiere seguir afinando esta cuerda?")

            if response2.lower() in aceptance:
                f1 = float(input("¿Qué frecuencia tiene la cuerda ahora (en Hz)? "))

        response = input("¿Quiere afinar otra cuerda? ")

    print("¡Gracias por usar el afinador de cuerdas!")
