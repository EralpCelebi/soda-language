def Read(filename):
    with open(filename, "r") as f:
        return f.read()


def Write(filename, data, typ=None):
    temp_type = "w"
    if typ is not None:
        temp_type = typ
    with open(filename, temp_type) as f:
        f.write(data)