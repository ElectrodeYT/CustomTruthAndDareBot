import random


def read_file_lines(file) -> []:
    lines = []
    with open(file) as f:
        file_lines = f.readlines()
        for line in file_lines:
            line = line.strip()
            if line.isspace():
                continue
            lines.append(line)

    return lines


truths = read_file_lines("truths.txt")
dares = read_file_lines("dares.txt")


def generate_truth():
    return random.choice(truths)


def generate_dare():
    return random.choice(dares)