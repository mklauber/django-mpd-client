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
    logger.info("songs")
    
    commands = []
    c['breadcrumbs'] = [
        { 'text': 'home', 'target': reverse( 'controls' ) },
        { 'text': 'browse', 'target': reverse( 'browse' ) },
    ]
    if artist:
        c['breadcrumbs'].append( {
            'text': 'artists', 
            'target':reverse( 'artists' )
        } )
        commands.extend( ['artist', artist] )
        if album:
            c['breadcrumbs'].append( {
                'text': artist, 
                'target':reverse( 'albums_by_artist', kwargs={ 'artist': artist } )
            } )
    elif album:
        c['breadcrumbs'].append( {
            'text': 'albums', 
            'target':reverse( 'albums' )
        } )
        commands.extend( [ 'album', album ] ) 
    
    else:
        commands = ['any', '']
    logger.info( commands )
    
    with MPDClient().connect("localhost", 6600) as mpd:
        c['songs'] = mpd.find( *commands )
    
    #Cleanup song information
    for song in c['songs']:
        song['filename'] = path.basename( song['file'] )
        song['time'] = formatTime( song['time'] )
    return c
        
@template_only( 'list.html' )
def artists( request, *args, **keywords ):
    c = RequestContext( request )
    logger.info("artists")
        
    c['breadcrumbs'] = [
        {'text': 'home', 'target':reverse('controls') },
        {'text': 'browse', 'target':reverse('browse') },
    ]
    
    with MPDClient().connect('localhost', 6600) as mpd:
        data = mpd.list( 'artist' )
    
    
    c['list'] = []
    for item in [d for d in data if d and '/' not in d ]:
        c['list'].append( { 
            'text': item, 
            'target' : reverse( 'albums_by_artist', kwargs={'artist': item } )  
        } )
    return c

@template_only( 'list.html' )
def albums( request, artist=None, *args, **keywords ):
    c = RequestContext( request )
    logger.info("albums")
    
    c['breadcrumbs'] = [
        {'text': 'home', 'target':reverse('controls') },
        {'text': 'browse', 'target':reverse('browse') },
    ]
    
    if artist:
        c['breadcrumbs'].append( 
            {'text': 'artists', 'target': reverse('artists') }
        )
    
    with MPDClient().connect('localhost', 6600) as mpd:
        data = mpd.list( 'album', artist ) if artist else mpd.list( 'album' )
    
    
    c['list'] = []
    for item in [d for d in data if d and '/' not in d ]:
        c['list'].append( { 
            'text': item, 
            'target' : reverse( 'songs_of_artist_album', kwargs={'album': item, 'artist': artist } ) if artist else reverse( 'album', kwargs={'album': item } )
        } )
    return c


















    
    
    
