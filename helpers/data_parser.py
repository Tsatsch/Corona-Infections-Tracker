
def get_bundeslander():
    bundeslander = []
    for line in open("resources/bundeslander.txt"):
        bundeslander.append(line.replace("\n", "").lower())
    return bundeslander
