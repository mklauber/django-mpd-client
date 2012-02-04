from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from mpd.mobile import urls

# Ajax Imports
from ajax import add_songs, clear_songs, next, play, prev, remove_songs, repeat, random, save_playlist, status, stop, volume

ajaxPatterns = patterns( '',
    url( r'status', status, name="ajaxStatus" ),
    #Playback Controls
    url( r'play', play, name="ajaxPlay" ),
    url( r'prev', prev, name="ajaxPrev" ),
    url( r'next', next, name="ajaxNext" ),
    url( r'stop', stop, name="ajaxStop" ),
    
    
    url( r'repeat', repeat, name="ajaxRepeat" ),
    url( r'random', random, name="ajaxRandom" ),
    url( r'volume/(?P<volume>\d{1,3})/', volume, name="ajaxVolume" ), 
    
    #Playlist Controls
    url( r'add', add_songs, name="playlistAdd" ),
    url( r'remove', remove_songs, name="playlistRemove" ),
    url( r'clear', clear_songs, name="PlaylistClear" ),
    url( r'save', save_playlist, name="PlaylistSave" ),    
    
    
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpd.views.home', name='home'),
    url( r'', include( urls.urlPatterns ) ),
    url( r'ajax/', include( ajaxPatterns ) ),


     ( r'^m/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': settings.MEDIA_ROOT } ),
)
