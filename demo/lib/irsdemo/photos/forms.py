from django import forms
from photos.models import *

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
