class FileReader():

    def __init__(self, file):
        self.file = file

     def read(self):
        try:
            with open(self.file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ''
