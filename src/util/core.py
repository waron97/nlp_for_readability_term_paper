def dump_to_file(s: str, fnmae: str):
    with open(fnmae, "w") as f:
        f.write(s)
