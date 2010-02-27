from django.http import HttpResponse
from PIL import Image
from django.core.cache import cache
from django.conf import settings
import StringIO
import os
from django.views.decorators.http import condition
from datetime import datetime

def resize(img, params):
    small = params.get('s', None)
    if small:
        owidth, oheight = img.size
        if owidth < oheight:
            width = small
            height = oheight
        else:
            height = small
            width = owidth
    else:
        width = params.get('w', None)
        height = params.get('h', None)
        if not (width and height):
            owidth, oheight = img.size
            if width:
                height = oheight
            else:
                width = owidth
    width = int(width)
    height = int(height)
    img.thumbnail((width, height), Image.ANTIALIAS)

def square_center_crop(img, params):
    width, height = img.size
    size = None
    try:
        percent = float(params['p'])/100
        print percent
        if width < height:
            size = percent * width
        else:
            size = percent * height
    except:
        size = int(params['s'])
    tlx = (width - size) / 2
    tly = (height - size) / 2
    brx = width - tlx
    bry = height - tly
    box = (tlx, tly, brx, bry)
    region = img.crop(box)
    region.load
    return region

def load_image(path):
    return Image.open(path)

def build_actions(action_str):
    actions = []
    for action in action_str.split('/'):
        action_parts = action.split('+')
        params = {}
        for param in action_parts[1:]:
            k = param[0]
            if len(param) > 1:
                v = param[1:]
            else:
                v = True
            params[k] = v
        actions.append({
            'name': action_parts[0],
            'params': params
        })
    return actions

def last_modified(request, path, action_str):
    path = settings.MEDIA_ROOT + path
    return datetime.fromtimestamp(os.path.getmtime(path))

@condition(last_modified_func=last_modified)
def complex_action(request, path, action_str):
    cache_key_prefix = '/irs/complex'
    cache_key = "%s/%s/%s" % (cache_key_prefix, path, action_str)
    img_data = cache.get(cache_key)
    if img_data is None:
        actions = build_actions(action_str)
        path = settings.MEDIA_ROOT + path
        img = load_image(path)
        for action in actions:
            if action['name'] == 'resize':
                resize(img, action['params'])
            elif action['name'] == 'sccrop':
                img = square_center_crop(img, action['params'])
        out = StringIO.StringIO()
        img.save(out, 'JPEG')
        img_data = out.getvalue()
        cache.set(cache_key, img_data)
    return HttpResponse(img_data, mimetype="image/jpeg")
