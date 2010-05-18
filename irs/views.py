from django.http import HttpResponse
from PIL import Image
from django.core.cache import cache
from django.conf import settings
import StringIO
from django.views.decorators.http import condition
from irs.storage import *

def resize(img, params):
    '''
    Resizes the provided Image to the specified size.
    params:
        s - small
            Set the maximum value of the smallest side to this value.
            The other side will be adjusted as necessary to maintain
            aspect ratio.
        w - max_width
        h - max_height
            Set either or both of these to set maximum values. Aspect
            ratio will be preserved.
    '''
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
    '''
    Useful for creating square thumbnails. Creates a square image of the size
    specified by params.size. If the requested size is smaller than the original
    image, the thumbnail will be pulled from the center of the image. If you
    request a size that is larger than the width or height of the original
    image, the resulting image will have a black background to fill the blank
    space.
    '''
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

def get_image(request, key):
    'Creates an irs.storage.IRSImage object from the given key'

    backend_module = None
    try:
        backend = settings.IRS_STORAGE_BACKEND
    except AttributeError:
        backend = 'irs.storage.FileImage'

    module = '.'.join(backend.split('.')[0:-1])
    klass = backend.split('.')[-1:][0]
    m = __import__(module, globals(), locals(), [klass], -1)
    return getattr(m, klass)(request, key)

def load_image(request, key):
    'Creates a PIL.Image object from the given key'
    return get_image(request, key).load().image

def build_actions(action_str):
    '''
    Takes the action string (which generally comes from the URL) and
    returns a List of actions to be executed. Each action is a map
    containing the name of the action and the params for the action,
    which is a map.
    '''
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
    'Returns the last modified date for a given image.'
    return get_image(request, path).get_last_modified()

@condition(last_modified_func=last_modified)
def complex_action(request, path, action_str):
    '''
    Handles a request for a complex manipulated image. You might also think
    of it as a "compound" image manipulation. The action string passed in
    (action_str) is a list of manipulations to be made. The manipulations
    will be executed in the order they are found in the action string.

    The action string is formatted as follows:

        ${action_name}[+${single_letter_param_name}${param_value}...]...

    For example, an action string that requests a resize and then a square center
    crop would look like this:

        resize+w100+h150/sccrop+s100

    See also irs.util.ImageURL.
    '''
    cache_key_prefix = '/irs/complex'
    cache_key = "%s/%s/%s" % (cache_key_prefix, path, action_str)
    img_data = cache.get(cache_key)
    if img_data is None:
        actions = build_actions(action_str)
        img = load_image(request, path)
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
