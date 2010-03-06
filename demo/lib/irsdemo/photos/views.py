from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from photos.models import *
from photos.forms import *

def show_photos(request):
    t = loader.get_template('show_photos.html')
    c = RequestContext(request, { 'photos': Photo.objects.all() })
    return HttpResponse(t.render(c))

def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(show_photos))
    else:
        form = PhotoForm()
    t = loader.get_template('add_photo.html')
    c = RequestContext(request, { 'form': form })
    return HttpResponse(t.render(c))
