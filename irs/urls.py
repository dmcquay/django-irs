from django.conf.urls.defaults import *

urlpatterns = patterns('synchros.django.irs.views',
    (r'^(?P<action_str>.*)/p\+(?P<path>.*)$', 'complex_action'),
)
