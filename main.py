import guitars
import harplike
import instrument

if __name__ == "__main__":
    guitar = guitars.ClassicalGuitar(length=0.2)
    guitar.tune(soundEnabled=True, verbose=True, showGraph=True)
