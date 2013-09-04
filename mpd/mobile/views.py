from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from os import path

from utilities import formatTime
from utilities.mpd import MPDClient, MPDError
from utilities.viewtools import template_only
from django.conf import settings
#Configure logging
import logging
logger = logging.getLogger( __name__ )

@template_only( 'controls.html' )
def controls( request ):
    c = RequestContext( request )
    return c

@template_only( 'browse.html' )
def browse( request, *args, **keywords ):
    c = RequestContext( request )
    c['breadcrumbs'] = []
    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        stats = mpd.stats()
        c['num_songs'] = stats['songs']
        c['num_artists'] = stats['artists']
        c['num_albums'] = stats['albums']
    return c

@template_only( 'songs.html' )
def songs( request, artist=None, album=None, *args, **keywords ):
    c = RequestContext( request )
    logger.info( "songs" )

    commands = []
    c['breadcrumbs'] = [
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

    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        c['songs'] = mpd.find( *commands )

    #Cleanup song information
    for song in c['songs']:
        song['filename'] = path.basename( song['file'] )
        song['time'] = formatTime( song['time'] )
    return c

@template_only( 'list.html' )
def artists( request, *args, **keywords ):
    c = RequestContext( request )
    logger.info( "artists" )

    c['breadcrumbs'] = [
        {'text': 'browse', 'target':reverse( 'browse' ) },
    ]

    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        data = mpd.list( 'artist' )


    c['list'] = []
    for item in sorted( [d for d in data if d and '/' not in d ] ):
        c['list'].append( {
            'text': item,
            'target' : reverse( 'albums_by_artist', kwargs={'artist': item } )
        } )
    return c

@template_only( 'list.html' )
def albums( request, artist=None, *args, **keywords ):
    c = RequestContext( request )
    logger.info( "albums" )

    c['breadcrumbs'] = [
        {'text': 'browse', 'target':reverse( 'browse' ) },
    ]

    if artist:
        c['breadcrumbs'].append( 
            {'text': 'artists', 'target': reverse( 'artists' ) }
        )

    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        data = mpd.list( 'album', artist ) if artist else mpd.list( 'album' )


    c['list'] = []
    for item in sorted( [d for d in data if d and '/' not in d ] ):
        c['list'].append( {
            'text': item,
            'target' : reverse( 'songs_of_artist_album', kwargs={'album': item, 'artist': artist } ) if artist else reverse( 'album', kwargs={'album': item } )
        } )
    return c

@template_only( 'playlist.html' )
def current_playlist( request, *args, **keywords ):
    c = RequestContext( request )

    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        c['songs'] = mpd.playlistinfo()

    logger.debug( c['songs'] )

    #Cleanup song information
    for song in c['songs']:
        song['filename'] = path.basename( song['file'] )
        song['time'] = formatTime( song.get('time', 0) )
    return c


@template_only( 'list.html' )
def playlists( request, *args, **keywords ):
    c = RequestContext( request )
    logger.info( "playlists" )

    c['breadcrumbs'] = [
        {'text': 'current playlist', 'target':reverse( 'playlist' ) },
    ]

    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        data = mpd.listplaylists()

    logger.debug( "Playlists: %s", data )
    c['list'] = []
    for item  in data:
        pass
        c['list'].append( {
            'text': item['playlist'],
            'target' : reverse( 'switch_playlist', kwargs={'playlist': item['playlist'] } )
        } )
    return c

def switch_playlist( request, playlist, *args, **keywords ):

    with MPDClient().connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        mpd.clear()
        mpd.load( playlist )
    return redirect( 'playlist' )













