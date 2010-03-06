from django.db import models
from irs.util import ImageURL

class Photo(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='photos')
    def url_small(self):
        return ImageURL(self.image).resize(width=200,height=200).square_center_crop(85).url()
