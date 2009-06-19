# -*- coding: utf-8 -*-

#   This file is part of moose.
#
#    Moose is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    Moose is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with moose; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os, sys
import xmlhandler

# Ritorna un Dictionary contenente i settings
# Esempio:
# >>> print settings['Language']
# >>> English

def LoadSettings(path): # Metodo per il caricamento dei settings
    settings = dict()
    xmldoc = xmlhandler.LoadXml(os.path.join(path, 'settings.xml'))
    # Apro il file xml contenente i settings
    if xmldoc == False: # Nel caso non trova il file la funzione ritorna False
        f = open(os.path.join(path, 'settings.xml'),'w')
        f.write(defaultsettings)
        f.close()
        xmldoc = xmlhandler.LoadXml(os.path.join(path, 'settings.xml'))
    for node in xmldoc.firstChild.childNodes:
            settings[node.getAttribute('name')] = node.getAttribute('value')
            # Inserisco nel dizionario i settings leggendo i nodi del xml, es. settings['Language'] = 'English'
    return settings

defaultsettings = '''<?xml version="1.0" ?>
<settings><node name="Hotkey-Next Phase" value="CTRL+SPACE"/><node name="Hotkey-RollD6" value="CTRL+R"/><node name="Language" value="English"/><node name="Hotkey-Reset Game" value="ALT+CTRL+G"/><node name="Hotkey-Flip Coin" value="CTRL+F"/><node name="Hotkey-Draw" value="CTRL+D"/><node name="Hotkey-Draw and Show" value="CTRL+W"/><node name="Update" value="No"/><node name="Nick" value="n00b"/><node name="Hotkey-Shuffle" value="CTRL+S"/><node name="Skin" value="Default"/><node name="Hotkey-End Turn" value="CTRL+E"/><node name="LastDeckPath" value=""/><node name="OpenLastDeck" value="Yes"/><node name="ShowFaceUpCardName" value="Yes"/></settings>'''