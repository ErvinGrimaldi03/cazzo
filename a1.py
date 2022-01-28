# Ervin Grimaldi
# egrimal1@uci.edu
# 51767760

from pathlib import Path
from os import remove


# The user's input get processed. Divide user input through space. Later, exclude '-' and keep strings that have '\'
def process(string):
    name = ''
    cmd = string[0]
    operations = [i for i in string.split(' ') if '-' in i and '\\' not in i]
    path = [i for i in string.split(' ') if i not in operations][1:]
    path = ' '.join(path)
    if '-s' in operations or '-e' in operations:
        name = ' '.join([i for i in path.split() if '\\' not in i])
        path = ' '.join([i for i in path.split() if i not in name])
        if '-e' in operations:
            name = f'.{name}'
        p = Path(path)
    if cmd == 'C' or cmd == 'D' or cmd == 'R':
        name = ' '.join([i for i in path.split() if '\\' not in i])
        path = ' '.join([i for i in path.split() if i not in name])
    # try:
    #     l = Path(path)
    #     for i in l.iterdir():
    #         pass
    # except FileNotFoundError:
    #     print('Path not found. Try again')
    #     run()
    comand(cmd, operations, path, name)


# Save all the directories seen, check them after the files in a dir and through recursion move to the next dir.
def rec_dirs(operation, path, p, name=None, saved=[]):
    if len(operation) == 1:
        for i in range(len(saved)):
            p1 = Path(saved[i])
            print(p1)
            for element in p1.iterdir():
                if element.is_dir():
                    saved = [i for i in saved[i:]]
                    saved.append(element)
                    rec_dirs(operation, path, p, saved)
                else:
                    print(element)
    if '-f' in operation:
        for i in range(len(saved)):
            p1 = Path(saved[i])
            for element in p1.iterdir():
                if element.is_file():
                    print(element)

    if '-e' in operation:
        for i in range(len(saved)):
            p1 = Path(saved[i])
            for element in p1.iterdir():
                if element.is_file() and element.suffix == name:
                    print(element)

    if '-s' in operation:
        for i in range(len(saved)):
            p1 = Path(saved[i])
            for element in p1.iterdir():
                if element.is_file() and element == p1 / name:
                    print(element)


# Code run only if '-r' option is present. This section check only the files and save the dir for process in rec_dirs()
def recursive(operation, path, p, name=None, saved=[]):
    saved = []
    if len(operation) == 1:
        for file in p.iterdir():
            if file.is_file():
                print(file)
        for dir in p.iterdir():
            if dir.is_dir():
                if dir in saved:
                    pass
                else:
                    saved.append(dir)
        rec_dirs(operation, path, p, name, saved)
    if '-f' in operation:
        for file in p.iterdir():
            if file.is_file():
                print(file)
        for dir in p.iterdir():
            if dir.is_dir():
                if dir in saved:
                    pass
                else:
                    saved.append(dir)
        rec_dirs(operation, path, p, name, saved)

    elif '-s' in operation:
        for file in p.iterdir():
            if file.is_file() and file == p / name:
                print(file)
        for dir in p.iterdir():
            if dir.is_dir():
                if dir in saved:
                    pass
                else:
                    saved.append(dir)
        rec_dirs(operation, path, p, name, saved)

    elif '-e' in operation:
        for file in p.iterdir():
            if file.is_file() and file.suffix == name:
                print(file)
        for dir in p.iterdir():
            if dir.is_dir():
                if dir in saved:
                    pass
                else:
                    saved.append(dir)
        rec_dirs(operation, path, p, name, saved)

    run()


# Block runs only if '-r' is not present. Operate normal conditions
def standard(operation, path, p, name=None):
    if '-f' in operation:
        for element in p.iterdir():
            if element.is_file():
                print(element)
    elif '-s' in operation:
        for element in p.iterdir():
            if element == p / name:
                print(element)
    elif '-e' in operation:
        for element in p.iterdir():
            if element.suffix == name:
                print(element)
    run()


# Block check what files have been inputted
def comand(cmd, operation, path, name=None):
    p = Path(path)
    if cmd == 'L':
        if operation == []:
            for file in p.iterdir():
                if file.is_file():
                    print(file)
            for dir in p.iterdir():
                if dir.is_dir():
                    print(dir)
        else:
            if '-r' in operation:
                recursive(operation, path, p, name)
            else:
                standard(operation, path, p, name)
    elif cmd == 'C':
        create(p, name)
    elif cmd == 'D':
        dell(p, name)
    elif cmd == 'R':
        read(p, name)
    run()


# Check if file exists, if not it creates, otherwise error and ask new input
def create(p, name):
    p1 = p / f'{name}.dsu'
    if not p1.exists():
        p1.touch()
        print(p1)
    else:
        print('EXISTS')
        pass
    run()


# check if file exists and delete it. Otherwhise returns an ERROR message and ask new input
def dell(p, name):
    p1 = p / name
    if not p1.exists():
        print("file doesn't exists")
        pass
    else:
        print(f'{p1} DELETED')
        remove(p1)
    run()


# Check if file exists, otherwise return error. Only .dsu are runned and check if file is empty. Block also strips any superflue new line from the file.
def read(p, name):
    lista = []
    p1 = p
    if not p1.exists() or not p1.suffix == '.dsu':
        print('ERROR')
        run()
    elif p1.exists():
        f = p1.open()
        if p1.stat().st_size == 0:
            print('EMPTY')
        else:
            for i, line in enumerate(f.readlines()):
                lista.append(line)
                if lista[i] == lista[-1]:
                    lista[i] = lista[i][:-1]
            for element in lista:
                print(element)
    else:
        print('ERROR')


# From here we require new input to the user, check if the user wants to quit, otherwise process the input
def run():
    global result
    result = []
    user = input()
    if user == 'Q':
        quit()
    elif len(user) < 3:
        print('ERROR')
        run()
    else:
        process(user)


# L C:\Users\Ervin asdunzi\test -r -s cazzo puzzolente.txt
# C C:\Users\Ervin asdunzi\test pene.png
# D C:\Users\Ervin asdunzi\test pene.png



if __name__ == "__main__":
    #This is usefull only once we start our program for the first time
    run()
