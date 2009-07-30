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
    try:
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
    except: return []

def CheckVersionUpdate(v):
    try:
        res = urllib.urlopen(updateserver + 'versionupdate.xml')
        ret = res.read()
        xmldoc = minidom.parseString(ret)
        nv = xmldoc.firstChild.firstChild.getAttribute('version')
        if v == nv: return 0
        else: return 1
    except: return 0

def GetFilePath(a,b):
    if sys.platform == "win32":
        b = b.replace('/', '\\')
    return os.path.join(a,b)    

def Update(dir,toupdate):
    try:
        for s in toupdate:
            urllib.urlretrieve(updateserver + s, GetFilePath(dir,s))
        urllib.urlcleanup()
    except:pass

def UpdateOne(dir, toupdate):
    try:
        urllib.urlretrieve(updateserver + toupdate, GetFilePath(dir,toupdate))
        urllib.urlcleanup()
    except: pass

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
        pr = (100/l)+1
        pn = 0
        for s in toupdate:
            self.Update(pn,'Downloading %s...' % s)
            UpdateOne(self._engine.BaseDirectory, s)
            pn += pr
        
    def CheckUpdateDialog(self):
        if CheckVersionUpdate(self._engine.GetVersion()):
            toupdate = CheckUpdate(self._engine.BaseDirectory)
            if self._engine.Frame.ShowDialog(self._engine.GetLangString('An update is avaible, would you like to update now?'),'',wx.YES_NO | wx.ICON_QUESTION | wx.YES_DEFAULT, parent=self) == wx.ID_YES:
                self.DoUpdate(toupdate)
                self._engine.Frame.ShowDialog(self._engine.GetLangString('Now you can restart the application.'),'',wx.OK | wx.ICON_INFORMATION, parent=self)
                sys.exit()
        else:
            self._engine.Frame.ShowDialog(self._engine.GetLangString('No update needed. Press NO in the next window.'), '', wx.OK | wx.ICON_INFORMATION, parent=self)
        self.Update(100, self._engine.GetLangString('Done'))


class ImagesUpdateDialog(wx.ProgressDialog):
    def __init__(self, parent, engine):
        self._engine = engine
        wx.ProgressDialog.__init__(self, 'Updater', 'Checking for updates...', 100, parent)
        self.Show()
        self.CheckUpdateDialog()
        
    def CheckUpdateDialog(self):
        m = self._engine.CheckMissingImages()
        d = []
        if len(m) > 0:
            l = len(m)
            pr = (100/l)
            pn = 0
            for n in m:
                if pn > 99: pn = 99
                self.Update(pn,'Downloading %s...' % n)
                if self._engine.DownloadImage(n):
                    d.append(n)
                pn += pr
            self._engine.Frame.ShowDialog(self._engine.GetLangString('Downloaded %s images, %s missing.', str(len(d)), str(len(m)-len(d))), '', wx.OK | wx.ICON_INFORMATION, parent=self)
        else:
            self._engine.Frame.ShowDialog(self._engine.GetLangString('No update needed.'), '', wx.OK | wx.ICON_INFORMATION, parent=self)
        self.Update(100, self._engine.GetLangString('Done'))