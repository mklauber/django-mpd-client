from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from utilities.mpd import MPDClient
from utilities.viewtools import as_json, using_mpd
import json
# Confiure Logging
import logging
logger = logging.getLogger(__name__)


@as_json
@using_mpd
def status( request ):
        mpd = MPDClient()
        with mpd.connect(settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT) as mpd:
            data = mpd.status()
            data.update( mpd.currentsong() )
            return data


# Playback Controls
@using_mpd
def play( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        if mpd.status().get('state', None) == 'play':
            mpd.pause()        
        else:
            mpd.play()
    return HttpResponse( "OK" )

@using_mpd
def prev( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        mpd.previous()
    return HttpResponse( "OK" )
    
@using_mpd
def next( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        mpd.next()
    return HttpResponse( "OK" )
    
@using_mpd
def stop( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        mpd.stop()
    return HttpResponse( "OK" )

# General Controls
@using_mpd
def repeat( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        repeat = int( mpd.status()['repeat'] )
        mpd.repeat( 0 if repeat == 1 else 1 )
    return HttpResponse( "Repeat: %s" % repeat )
        

@using_mpd   
def random( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        random = int( mpd.status()['random'] )
        mpd.random( 0 if random == 1 else 1 )
        
    return HttpResponse( "Random: %s" % random )

@using_mpd
def volume( request, volume ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        mpd.setvol(volume)
        volume = mpd.status()['volume']            
    return HttpResponse( "Volume: %s" % volume )
    
# Playlist Controls
@csrf_exempt
@using_mpd
def add_songs( request ):
    post = request.POST
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        for song in json.loads( post['songs'] ):
            mpd.add(song)
    return HttpResponse( "OK" )
    
@csrf_exempt
@using_mpd
def remove_songs( request ):
    post = request.POST
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT ) as mpd:
        for song in json.loads( post['songs'] ):
            song = int(song)
            logger.info( "Deleting: %s", song )
            mpd.deleteid( song )
    return HttpResponse( "OK" )
    

@csrf_exempt
@using_mpd    
def clear_songs( request ):
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT) as mpd:
        mpd.clear()    
    return HttpResponse( "OK" )

@csrf_exempt
@using_mpd    
def save_playlist( request ):
    name = request.POST['name']
    mpd = MPDClient()
    with mpd.connect( settings.MPD_CLIENT_HOST, settings.MPD_CLIENT_PORT) as mpd:
        logger.debug( "Playlist Name: %s", name )
        mpd.rm( name )
        mpd.save( name )    
    return HttpResponse( "OK" )

