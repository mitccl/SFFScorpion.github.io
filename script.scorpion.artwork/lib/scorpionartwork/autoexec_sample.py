# -*- coding: UTF-8 -*-
#######################################################################

# Addon Name: AutoExec for scorpion
# Addon id: script.scorpion.artwork
# Addon Provider: Supremacy

import xbmcvfs,xbmcgui
from scorpionartwork import theme_setter

def main():
    try:
        theme_setter.Apply_Theme('Collusion')
        xbmcvfs.delete('special://userdata/autoexec.py')
    except Exception, e:
        xbmcvfs.delete('special://userdata/autoexec.py')

if __name__ == '__main__':
    main()