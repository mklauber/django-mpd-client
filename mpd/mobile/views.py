from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from os import path

from utilities import formatTime
from utilities.mpd import MPDClient, MPDError
from utilities.viewtools import template_only

#Configure logging
import logging
logger = logging.getLogger( __name__ )

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

@template_only( 'songs.html' )
def songs( request, artist=None, album=None, *args, **keywords ):
    c = RequestContext( request )
    c['breadcrumbs'] = [
        {'text': 'home', 'target':reverse('controls') },
        {'text': 'browse', 'target':reverse('browse') },
    ]
    if artist:
        c['breadcrumbs'].append( {
            'text': 'artist', 
            'target':reverse( 'artist',  kwargs={ 'artist': artist } ) 
        } )
    if album:
        c['breadcrumbs'].append( {
            'text': 'album', 
            'target':reverse( 'album', kwargs={ 'album': album } ) 
        } )
    
    # Choose our find query
    commands = []
    if artist: commands.extend(['artist', artist])
    if album:  commands.extend(['album', album]) 
    if not commands: commands.extend(['any', ''])
    
    
    with MPDClient().connect("localhost", 6600) as mpd:
        c['songs'] = mpd.find( *commands )
        logger.debug( "Song: %s", c['songs'][0] )
    for song in c['songs']:
        song['filename'] = path.basename( song['file'] )
        song['time'] = formatTime( song['time'] )
    return c
    
    
    
    
    
    
    
    
    
    
    
