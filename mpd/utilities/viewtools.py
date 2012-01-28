from django.shortcuts import render_to_response
from django.http import HttpResponse
from utilities.mpd import MPDError, ConnectionError
import json

def template_only( template ):
    def decorator( function ):
        def outer( request, *args, **keywords ):
            context = function( request, *args, **keywords )
            return render_to_response( template, context )
        return outer
    return decorator


def as_json( function ):
    def outer( request, *args, **keywords ):
        data = function( request, *args, **keywords )
        # Pass any HttpResponses (server errors?) straight through.
        if isinstance(data, HttpResponse):
            return data
        return HttpResponse( json.dumps( data ) )

    return outer

## Wrap requests in error checking if we use the mpd client.
# 
def using_mpd( function):
    def outer( request, *args, **keywords ):
        try:
            return function( request, *args, **keywords )
       
        except ConnectionError as e:
            logger.Error( "Lost connection to MPD Daemon" )
            logger.Exception( e )
            return HttpResponseServerError( "Lost Connection to server." )
        except MPDError as e:
            logger.Error( "An unknown error occurred" )
            logger.Exception( e )
            return HttpResponseServerError( "And unknown error occurred." )

    return outer

