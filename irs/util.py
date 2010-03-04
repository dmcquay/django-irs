class ImageURL:
    '''
    Utility to build image urls using django-irs. Usage will look something like this:

        from irs.util import ImageURL
        image_path = 'portraits/dustin.jpg'
        url = ImageURL(image_path).resize(width=100, height=100).url()

    "resize" is one of the maniuplations you can perform on an image. Here are all the
    available manipulations:

        * resize
        * square_center_crop
    '''
    def __init__(self, image_path_rel):
        '''
        Object constructor. Must pass the image path relative to MEDIA_ROOT as
        defined in your django settings module.
        '''
        self.image_path_rel = image_path_rel
        self.transformations = []
    def resize(self, width=None, height=None, small=None):
        '''
        Resizes the image to the maximum dimensions provided.

            small - the max dimension for the smallest original dimension
            width - the maximum width
            height - the maximum height

        Only one must be specified. small will trump width & height. In all cases the aspect ratio of the image will be preserved.
        '''
        if (small == None and width == None and height == None):
            raise Exception, 'At least one of small, width, height must be specified'
        if small == None:
            if width == None:
                self.transformations.append('resize+w%d' % (width))
            elif height == None:
                self.transformations.append('resize+h%d' % (height))
            else:
                self.transformations.append('resize+w%d+h%d' % (width, height))
        else:
                self.transformations.append('resize+s%d' % (small))
        return self
    def square_center_crop(self, size=0):
        '''
        Creates a square image of the given size. It will be taken from the center of the original image. It is often useful to resize the image before doing this to ensure the result is not an incredibly small piece of the image. For example, taking a 200px square center crop out of a 1200px image would probably look bad.
        '''
        self.transformations.append('sccrop+s%d' % (size))
        return self
    def _build_action_str(self):
        'Private method used to bild the action string.'
        return '/'.join(self.transformations)
    def url(self):
        '''
        The final method which should be called to generate the url.
        '''
        #TODO: use reverse instead of assuming /irs
        return '/irs/%s/p+%s' % (self._build_action_str(), self.image_path_rel)
    def __unicode__(self):
        return self.url()
