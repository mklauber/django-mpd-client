from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from utilities.mpd import MPDClient, MPDError
from utilities.viewtools import template_only

@template_only( 'controls.html' )
def controls(request):
    c = RequestContext( request )
    return c
    
@template_only( 'browse.html' )
def browse( request, *args, **keywords ):
    c = RequestContext( request )
    c['breadcrumbs'] = [
        {'text': 'home', 'target':reverse('controls') }
    ]
    with MPDClient().connect("localhost", 6600) as mpd:
        stats = mpd.stats()
        c['num_songs'] = stats['songs']
        c['num_artists'] = stats['artists']
        c['num_albums'] = stats['albums']
    return c
        
