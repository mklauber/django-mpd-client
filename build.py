import os
import os.path as path

BASE = os.getcwd()

APACHE = path.join( BASE, 'apache' )
MPD = path.join( BASE, 'mpd' )
RESOURCES = path.join( BASE, 'resources' )

VERSION = path.join( BASE, 'VERSION' )
version = open( VERSION ) if path.exists( VERSION ) else '0.0'

def xcf2png( file, destination=None ):
	""" Generate final images from xcf resources. """
	command = 'xcf2png %s -o %s' % ( file, destination )
	subprocess.call( command, shell=True )

def create_virtualenv():
	""" Create a virtual environment to use for the site. """
	pass

def activate_virtualenv():
	""" Activate the virtual environment. """
	pass

def install_module( name ):
	""" Install a dependency into the virtual environment. """
	pass

def create_tar():
	""" Create a tar containing the necessary files. """
	pass

def create_rpm():
	""" Create an rpm package installing the necessary files. """
	pass

def create_deb():
	""" Create an deb package installing the necessary files. """
	pass

if __name__ == '__main__':
	pass
