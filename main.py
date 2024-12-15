import guitars
import harplike
import instrument

if __name__ == "__main__":
    guitar = guitars.ClassicalGuitar()
    guitar.tune(soundEnabled=True, verbose=True, showGraph=True)
