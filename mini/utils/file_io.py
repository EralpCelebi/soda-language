def Read(filename):
    with open(filename, "r") as f:
        return f.read()


def Write(filename, data):
    with open(filename, "w") as f:
        f.write(data)