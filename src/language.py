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
import engine, xmlhandler

class language():
    #path = '' # Path del linguaggio
    #name = '' # Nome del linguaggio
    #props = dict() # Dictionary che contiene le proprieta' del linguaggio

    def __init__(self,p):
        self.path = p
        self.props = dict()
        self.name = ''
        xmldoc = xmlhandler.LoadXml(self.path)
        # Apro il file xml contenente le proprieta' della skin
        for node in xmldoc.firstChild.childNodes:
            if not node.getAttribute('name') == 'Name':
                self.props[node.getAttribute('name')] = node.getAttribute('value')
            else:
                self.name = node.getAttribute('value')
    
    def GetString(self,name):
        if not self.props.has_key(name):
            return name
        return self.props[name]

    def Exists(self,name):
        return self.props.has_key(name)

def LoadLanguages(dir):
    '''Metodo per caricare i linguaggi'''
    langs = dict()
    files = engine.ListFiles(dir) # Ottengo la lista delle directory contenute nella cartella Language
    for s in files: # Ciclo le directory delle skin
        ln = language(s) # Creo un oggetto skin per ogni skin
        langs[ln.name] = ln # La aggiungo al dictionary
    return langs