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

import os, sys, wx
import xmlhandler, engine

class skin():
    #path = '' # Directory della skin
    #name = '' # Nome della skin
    #props = dict() # Dictionary che contiene le proprieta' della skin
    # Es. props['Background'] = 'background.jpg'

    def __init__(self,p):
        self.path = p
        self.images = dict()
        self.props = dict()
        self.name = ''
        xmldoc = xmlhandler.LoadXml(os.path.join(self.path,'skin.xml'))
        # Apro il file xml contenente le proprieta' della skin
        for node in xmldoc.firstChild.childNodes:
            if not node.getAttribute('name') == 'Name':
                self.props[node.getAttribute('name')] = node.getAttribute('value')
                #self.images[node.getAttribute('name')] = wx.Bitmap(os.path.join(self.path, node.getAttribute('value')))
            else:
                self.name = node.getAttribute('value')
    
    def GetImage(self,name):
        if self.images.has_key(name): 
            return self.images[name].GetSubBitmap(wx.Rect(0, 0, self.images[name].GetWidth(), self.images[name].GetHeight()))
        elif self.props.has_key(name):
            self.images[name] = wx.Bitmap(self.GetPath(name))
            return self.images[name].GetSubBitmap(wx.Rect(0, 0, self.images[name].GetWidth(), self.images[name].GetHeight()))
        else: return self.GetImage('none')

    def GetPath(self,name):
        file = os.path.join(self.path, self.props[name])
        return os.path.join(self.path,file)

    def Exists(self,name):
        return self.props.has_key(name)

def LoadSkins(path):
    '''Metodo per caricare le skin'''
    skins = dict()
    dirs = engine.ListDirs(path) # Ottengo la lista delle directory contenute nella cartella Skin
    for s in dirs:
        if not os.path.exists(os.path.join(s,'skin.xml')): # Testo se contengono il file skin.xml
            dirs.remove(s) # Se non lo hanno le tolgo dalla lista
    for s in dirs: # Ciclo le directory delle skin
        sn = skin(s) # Creo un oggetto skin per ogni skin
        skins[sn.name] = sn # La aggiungo al dictionary
        # Es. skins['Default'] = <Riferimento_ad_un_oggetto_skin>
    return skins