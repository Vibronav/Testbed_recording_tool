import argparse
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Tool for testbed recording via raspberryPi")
    parser.add_argument("--data-folder", help="folder with reference chirp file, and output for recorded wavfiles")
    parser.add_argument("--output-filename", help="Filename for recorded wavfile")



def main():
    args = parse_args()
    pass


if __name__ == "__main__":
    main()
