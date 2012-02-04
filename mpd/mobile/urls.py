from django.conf.urls.defaults import patterns, url, include
import os

# View imports
from mobile.views import albums, artists, browse, controls, current_playlist, playlists, songs, switch_playlist

urlPatterns = patterns( '',

    url( r'^$', controls, name="controls" ),
    url( r'^browse/$', browse, name="browse" ),
    url( r'^search/$', lambda x: x, name="search" ),

    # Playlists
    url( r'playlist/$', current_playlist, name='playlist' ),
    url( r'playlists/$', playlists, name='playlists' ),
    url( r'switch/(?P<playlist>.+)/$', switch_playlist, name="switch_playlist"),

    # Browse by artist
    url( r'browse/artists/$', artists, name="artists" ),
    url( r'browse/artist/(?P<artist>[^/]+?)/$', albums, name="albums_by_artist" ),
    
    url( r'browse/artist/(?P<artist>[^/]+?)/songs/$', songs, name="songs_by_artist" ),
    url( r'browse/artist/(?P<artist>[^/]+?)/(?P<album>[^/]+?)/$', songs, name="songs_of_artist_album" ),
    # Browse by albums
    url( r'browse/album/$', albums, name="albums" ),
    
    url( r'browse/album/(?P<album>[^/]+?)/$', songs, name="album" ),
    # Browse all songs
    url( r'browse/songs/$', songs, name="songs"),

    # Include the CSS/JS/Media Files
   ( r'^m/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': os.path.join(os.getcwd(), 'mobile/media') } ),
)
