from django.conf import settings
from django.template import RequestContext
from utilities.mpd import MPDClient, MPDError
from utilities.viewtools import template_only

@template_only( 'controls.html' )
def controls(request):
    c = RequestContext( request )
    return c
