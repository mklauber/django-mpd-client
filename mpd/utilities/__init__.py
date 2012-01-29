def formatTime( time ):
    time = int(time)
    seconds = time % 60;
    minutes = time / 60;
    return "%d:%02d" % ( minutes, seconds )
