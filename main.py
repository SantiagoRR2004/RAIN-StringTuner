import guitars
import harplike
import instrument

if __name__ == "__main__":
    guitar = guitars.ClassicalGuitar()
    print(len(guitar.tune(soundEnabled=True)))
