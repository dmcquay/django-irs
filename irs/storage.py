from PIL import Image
from django.conf import settings
from datetime import datetime
import os

class IRSImage:
    def __init__(self, request, key):
        self.request = request
        self.key = key
        self.image = None
    def load(self):
        raise Exception('Method "load" not implemented')
    def get_last_modified(self):
        raise Exception('Method "get_last_modified" not implemented')

class FileImage(IRSImage):
    def load(self):
        path = settings.MEDIA_ROOT + self.key
        self.image = Image.open(path)
        return self
    def get_last_modified(self):
        path = settings.MEDIA_ROOT + self.key
        return datetime.fromtimestamp(os.path.getmtime(path))
