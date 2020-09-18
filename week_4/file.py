import tempfile
import os
import random


class File:

    def __init__(self, path_to_file):
        self.curr = 0
        if not os.path.exists(path_to_file):
            with open(path_to_file, 'w') as f:
                f.write('')
        self.path_to_file = path_to_file

    def __str__(self):
        return self.path_to_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path_to_file, 'r') as f:
            f.seek(self.curr)
            s = f.readline()
            if not s:
                self.curr = 0
                raise StopIteration
            self.curr = f.tell()
        return s

    def __add__(self, second_file):
        new_file = File(os.path.join(tempfile.gettempdir(), 'new_file' + str(random.randint(1, 100))))
        new_file.write(self.read() + second_file.read())
        return new_file

    def read(self):
        with open(self.path_to_file, 'r') as f:
            return f.read()

    def write(self, data):
        with open(self.path_to_file, 'w') as f:
            f.write(data)


def main():
    path_to_file = '/home/user1/Документы/Coursera_stage_1/example.txt'
    file1 = File('1')
    file2 = File('2')
    file3 = file1 + file2

    for line in file3:
        print(line)

if __name__ == '__main__':
    main()
