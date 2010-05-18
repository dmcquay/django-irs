from PIL import Image

class IRSImage:
    def __init__(self, id):
        self.id = id
        self.image = None
    def load(self):
        raise Exception('Method "load" not implemented')

class FileImage(IRSImage):
    def load(self):
        self.image = Image.open(self.id)
        return self
