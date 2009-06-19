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

import urllib, os, md5, sys, wx
from xml.dom import minidom

updateserver = 'http://jbyyxproject.googlecode.com/svn/src/'

def CheckUpdate(dir):
    toupdate = []
    res = urllib.urlopen(updateserver + 'update.xml')
    ret = res.read()
    xmldoc = minidom.parseString(ret)
    for node in xmldoc.firstChild.childNodes:
        file = node.getAttribute('name')
        hash = node.getAttribute('value')
        if os.path.exists(GetFilePath(dir,file)):
            hash2 = GetFileSize(dir, file)
            if hash != hash2:
                toupdate.append(file)
        else:
            toupdate.append(file)
    return toupdate

def GetFilePath(a,b):
    if sys.platform == "win32":
        b = b.replace('/', '\\')
    return os.path.join(a,b)    

def Update(dir,toupdate):
    for s in toupdate:
        urllib.urlretrieve(updateserver + s, GetFilePath(dir,s))
    urllib.urlcleanup()

def UpdateOne(dir, toupdate):
    urllib.urlretrieve(updateserver + toupdate, GetFilePath(dir,toupdate))
    urllib.urlcleanup()

def GetFileSize(dir, file):
    return str(os.stat(GetFilePath(dir,file))[6])


class UpdateDialog(wx.ProgressDialog):
    def __init__(self, parent, engine):
        self._engine = engine
        wx.ProgressDialog.__init__(self, 'Updater', 'Checking for updates...', 100, parent)
        self.Show()
        self.CheckUpdateDialog()
     
    def DoUpdate(self, toupdate):
        l = len(toupdate)
        pr = 100/l
        pn = 0
        for s in toupdate:
            self.Update(pn,'Downloading %s...' % s)
            UpdateOne(self._engine.BaseDirectory, s)
            pn += pr
        
    def CheckUpdateDialog(self):
        toupdate = CheckUpdate(self._engine.BaseDirectory)

        if len(toupdate) > 0:
            if self._engine.Frame.ShowDialog(self._engine.GetLangString('An update is avaible, would you like to update now?'),'',wx.YES_NO | wx.ICON_QUESTION | wx.YES_DEFAULT, parent=self) == wx.ID_YES:
                self.DoUpdate(toupdate)
                self._engine.Frame.ShowDialog(self._engine.GetLangString('Now you can restart the application.'),'',wx.OK | wx.ICON_INFORMATION, parent=self)
                sys.exit()
        else:
            self._engine.Frame.ShowDialog(self._engine.GetLangString('No update needed.'), '', wx.OK | wx.ICON_INFORMATION, parent=self)
        self.Update(100, self._engine.GetLangString('Done'))
        
    