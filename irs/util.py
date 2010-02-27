class ImageURL:
    transformations = []
    def __init__(self, image_path_rel):
        self.image_path_rel = image_path_rel
    def resize(self, width=None, height=None, small=None):
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
        self.transformations.append('sccrop+s%d' % (size))
        return self
    def _build_action_str(self):
        return '/'.join(self.transformations)
    def url(self):
        #TODO: use reverse instead of assuming /irs
        return '/irs/%s/p+%s' % (self._build_action_str(), self.image_path_rel)
