
def process_path_to_save(path):
    path = path.split()
    for i in range(len(path)):
        if path[i] == '\\':
            path[i] = '/'


def process_path_to_use(path):
    path = path.split()
    for i in range(len(path)):
        if path[i] == '/':
            path[i] = '\\'

    return path.join()
