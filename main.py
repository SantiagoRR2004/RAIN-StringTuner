import guitars
import harplike

if __name__ == "__main__":
    guitar = guitars.ClassicalGuitar(length=0.85)
    print(len(guitar.tune(verbose=True)))
