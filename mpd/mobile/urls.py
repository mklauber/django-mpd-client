from django.conf.urls.defaults import patterns, url, include

# View imports
from mobile.views import controls

urlPatterns = patterns( '',

    url( r'^$', controls, name="controls" ),
    url( r'^browse$', lambda x: x, name="browse" ),
    # Playlists

    # Browse by artist
    url( r'/artists/$', lambda x: x, name="artists" ),
    url( r'/artist/(?P<artist>[^/]+?)/$', lambda x: x, name="artist" ),
    url( r'/artist/(?P<artist>[^/]+?)/songs/', lambda x: x, name="songs_by_artist" ),
    url( r'/artist/(?P<artist>[^/]+?)/(?P<album>[^/]+?)/$', lambda x: x, name="album_of_artist" ),
    # Browse by albums
    url( r'/album/$', lambda x: x, name="albums" ),
    url( r'/album/(?P<album>[^/]+?)/$', lambda x: x, name="album" ),

    # Include the Ajax patterns
)
