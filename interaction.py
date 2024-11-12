import logic
import string


aceptance = [
    "sí",
    "vale",
    "ok",
    "afirmativo",
    "correcto",
    "de acuerdo",
    "s",
    "y",
    "si",
    "yes",
]


def ensureNumber(question: str) -> float:

    toret = input(question)

    while toret.isnumeric() == False:
        toret = input("Por favor, introduzca un número: ")

    return float(toret)


if __name__ == "__main__":
    tuner = logic.Tuner()
    print("¡Bienvenido al afinador de cuerdas!")
    print("Este programa te ayudará a afinar su instrumento de cuerda.")

    response = input("¿Quiere afinar una cuerda? ").translate(
        str.maketrans("", "", string.punctuation)
    )

    while response.lower() in aceptance:

        l = ensureNumber("¿Qué longitud tiene la cuerda (en cm)? ") / 100
        f = ensureNumber("¿Qué frecuencia quiere para la cuerda (en Hz)? ")
        f1 = ensureNumber("¿Qué frecuencia tiene la cuerda (en Hz)? ")

        response2 = "s"

        while response2.lower() in aceptance:
            t = tuner.tune(f, f1, l)

            if t >= 0:
                print(f"Aprite la cuerda {t} vueltas.")
            else:
                print(f"Afloje la cuerda {-t} vueltas.")

            response2 = input("¿Quiere seguir afinando esta cuerda? ").translate(
                str.maketrans("", "", string.punctuation)
            )

            if response2.lower() in aceptance:
                f1 = ensureNumber("¿Qué frecuencia tiene la cuerda ahora (en Hz)? ")

        response = input("¿Quiere afinar otra cuerda? ").translate(
            str.maketrans("", "", string.punctuation)
        )

    print("¡Gracias por usar el afinador de cuerdas!")
