import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 moon.py <filename>")
        exit(1)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        source_code = f.read()