from django.conf.urls.defaults import patterns, url, include

# View imports
from mobile.views import browse, controls

urlPatterns = patterns( '',

    url( r'^$', controls, name="controls" ),
    url( r'^browse/$', browse, name="browse" ),
    url( r'^search/$', lambda x: x, name="search" ),
    # Playlists

    # Browse by artist
    url( r'browse/artists/$', lambda x: x, name="artists" ),
    url( r'browse/artist/(?P<artist>[^/]+?)/$', lambda x: x, name="artist" ),
    url( r'browse/artist/(?P<artist>[^/]+?)/songs/$', lambda x: x, name="songs_by_artist" ),
    url( r'browse/artist/(?P<artist>[^/]+?)/(?P<album>[^/]+?)/$', lambda x: x, name="album_of_artist" ),
    # Browse by albums
    url( r'browse/album/$', lambda x: x, name="albums" ),
    url( r'browse/album/(?P<album>[^/]+?)/$', lambda x: x, name="album" ),
    # Browse all songs
    url( r'browse/songs/$', lambda x: x, name="songs"),

    # Include the Ajax patterns
)
