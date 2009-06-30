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

import sys, os, wx, time, datetime, re, urllib, thread, traceback, socket
from xml.dom import minidom
from sqlite3 import dbapi2
import version, mainform, gamecard, settings, skin, language, deck, xmlhandler
import network, gameframe, dialogs, updater, keyhandler, cache

def ListDirs(path):
    '''Returns the list of all dirs in path'''
    rd = os.listdir(path)
    dirs = []
    for s in rd:
        dp = os.path.join(path,s)
        if os.path.isdir(dp):
            dirs.append(dp)
    return dirs

def ListFiles(path):
    '''Returns the list of all files in path'''
    rd = os.listdir(path)
    files = []
    for s in rd:
        dp = os.path.join(path,s)
        if os.path.isfile(dp):
            files.append(dp)
    return files

# Main Class of the Application
class Engine():

    def __init__(self):
        # Check development mode
        self._dev = False
        if len(sys.argv) > 1:
            if sys.argv[1] == 'dev':
                self._dev = True

        self.Application = wx.App() # Create App

        # Paths Initializations
        self.BaseDirectory = ''
        found = 0
        if self._dev:
            self.BaseDirectory = os.path.dirname(os.path.realpath(__file__)) # BaseDirectory
            if os.path.exists(os.path.join(self.BaseDirectory,'engine.pyw')):
                found = 1
        if not found:
            if sys.platform == 'win32':
                self.BaseDirectory = os.path.join(os.environ.get('PROGRAMFILES'),'Moose','src')
                if os.path.exists(os.path.join(self.BaseDirectory,'engine.pyw')):
                    found = 1
            elif sys.platform == 'linux2':
                self.BaseDirectory = os.path.join(os.environ.get('HOME'),'.moose','src')
                if os.path.exists(os.path.join(self.BaseDirectory,'engine.pyw')):
                    found = 1
        if not found:
            self.BaseDirectory = os.getcwd()
            if os.path.exists(os.path.join(self.BaseDirectory,'engine.pyw')):
                found = 1
        if not found:
            sys.exit()

        splash = wx.SplashScreen(wx.Bitmap(os.path.join(self.BaseDirectory, 'splash.png'), wx.BITMAP_TYPE_PNG), wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT, 0, None, -1)
        self.SkinsDirectory = os.path.join(self.BaseDirectory, 'Skins') # Skins Directory
        self.LanguagesDirectory = os.path.join(self.BaseDirectory, 'Languages') # Languages Directory
        self.DecksDirectory = os.path.join(self.BaseDirectory, 'Decks') # Decks Directory
        self.ImagesDirectory = os.path.join(self.BaseDirectory, 'Images') # Images Directory
        self.LogPath = os.path.join(self.BaseDirectory,'logs.txt') # Log Path

        # Dirs creation if they don't exists
        if not os.path.exists(self.SkinsDirectory):
            os.mkdir(self.SkinsDirectory)
        if not os.path.exists(self.LanguagesDirectory):
            os.mkdir(self.LanguagesDirectory)
        if not os.path.exists(self.DecksDirectory):
            os.mkdir(self.DecksDirectory)
        if not os.path.exists(self.ImagesDirectory):
            os.mkdir(self.ImagesDirectory)

        splash.Refresh() # Refresh the Splash Screen
    
        self.Settings = settings.LoadSettings(self.BaseDirectory) # Load settings
        self.SaveSettings()

        # Exceptions Report
        if self.GetSetting("Report-Exceptions") == "Yes":
            log = self.ReadLog()
            if log.count('Exception:') > 0:
                thread.start_new_thread(self.SendReport, (log,))
    
        # Log Creation
        self.CreateLog()

        splash.Refresh() # Refresh the Splash Screen

        # Ip Address
        self._ip = ''

        # Update Check
        if self.GetSetting('Update') == 'Yes':
            if updater.CheckVersionUpdate(self.GetVersion()):
                toupdate = updater.CheckUpdate(self.BaseDirectory)
                if len(toupdate) > 0:
                    if wx.MessageDialog(None,'An update is avaible,\nwould you like to update now?','',wx.YES_NO | wx.ICON_QUESTION | wx.YES_DEFAULT).ShowModal() == wx.ID_YES:
                        updater.Update(self.BaseDirectory,toupdate)
                        wx.MessageDialog(None,'Now you can restart the application.','',wx.OK | wx.ICON_INFORMATION).ShowModal()
                        sys.exit()

        splash.Refresh() # Refresh the Splash Screen

        self.Skins = skin.LoadSkins(self.SkinsDirectory) # Carico le skin
        self.Languages = language.LoadLanguages(self.LanguagesDirectory) # Carico i languages
        
        self.DatabaseCardsCount = len(self.GetAllCards()) # Inizializzo una variabile contenente il totale delle carte
        
        splash.Refresh() # Refresh the Splash Screen

        self.Frame = mainform.MainFrame(engine=self, parent=None, title="Moose.Deck",size=(800,640)) #Inizializzo il frame
        self.Frame.SetIcon(wx.IconFromLocation(wx.IconLocation(os.path.join(self.BaseDirectory,'moose16x16.ico'))))
        
        # New Deck
        self.Deck = deck.Deck()
        self.DeckPath = ''

        splash.Refresh() # Refresh the Splash Screen

        # Last Deck Check
        if self.GetSetting('OpenLastDeck') == 'Yes':
            lastdeckpath = self.GetSetting('LastDeckPath')
            if lastdeckpath and os.path.exists(lastdeckpath):
                self.Frame.OnOpen(path=lastdeckpath)

        # Usage statistics
        if self.GetSetting("Usage-Stats") == "Yes":
            thread.start_new_thread(self.SendStats, (self,))

        # Cards' Images Cache
        self._imagecache = cache.Cache()
        self._scaledimagecache = cache.Cache()

        splash.Refresh() # Refresh the Splash Screen
        time.sleep(0.5) # Sleep 0.5 seconds
        splash.Close() # Close the Splash Screen
        self.Frame.Show() # Show the Frame
        self.Application.MainLoop() # Application MainLoop

    def CheckMissingImages(self):
        '''Check for missing images'''
        cards = self.GetAllCards()
        l = self.DownloadImageList()
        m = []
        for c in cards:
            if not os.path.exists(os.path.join(self.ImagesDirectory, c.Name + '.jpg')) and l.count(c.Name + '.jpg') > 0:
                m.append(c.Name)
        return m

    def DownloadImage(self, n):
        '''Download missing images'''
        if not self.CheckConnection():
            return 0
        url = 'http://mooseproject.googlecode.com/svn/branches/images/%s.jpg' % n
        try:
            urllib.urlretrieve(url, os.path.join(self.ImagesDirectory,'%s.jpg'%n))
            return 1
        except: pass
        return 0

    def DownloadImageList(self):
        if not self.CheckConnection():
            return ''
        url = 'http://mooseproject.googlecode.com/svn/branches/images/'
        s = ''
        try: 
            u = urllib.urlopen(url)
            while 1:
                r = u.read()
                if r == '': break
                else: s += r
        except: pass
        return s
        

    def CheckConnection(self):
        '''Checks if an internet connection is avaible'''
        if self.GetIp():
            return True
        else:
            return False

    def SendReport(self, log, *args):
        '''Report the current Log'''
        url = 'http://mooseproject.000webhost.com/rooms/report.php?log=%s'%urllib.quote(log)
        urllib.urlopen(url)

    def TimeStamp(self):
        '''Return the TimeStamp'''
        t = datetime.datetime.now().timetuple()
        return '%s-%s-%s-%s:%s:%s'%(t[0],t[1],t[2],t[3],t[4],t[5])
    
    def DateStamp(self):
        '''Return the DateStamp'''
        t = datetime.datetime.now().timetuple()
        return '%s-%s-%s'%(t[0],t[1],t[2])

    def CreateLog(self):
        '''Create the application log'''
        s = 'Session %s' % self.DateStamp()
        l = self.ReadLog()
        if os.path.exists(self.LogPath) and l.count(s) > 0:
            handle = open(self.LogPath, 'a')
        else:
            handle = open(self.LogPath, 'w')
        handle.write('Session %s\n' % self.TimeStamp())
        handle.close()

    def WriteLog(self, log):
        '''Write to the current log'''
        handle = open(self.LogPath,'a')
        handle.write('%s: %s\n'%(self.TimeStamp(),log))
        handle.close()

    def WriteExceptionLog(self):
        '''Write the last exception to the current log'''
        e = self.FormatException()
        a = ''
        for s in e[2]:
            if a: a += ' '
            a += s
        log = 'Exception: %s - %s - %s\n'%(e[0],e[1],a)
        handle = open(self.LogPath,'a')
        handle.write('%s: %s\n'%(self.TimeStamp(),log))
        handle.close()

    def ReadLog(self):
        '''Return the current log'''
        path = os.path.join(self.BaseDirectory,'logs.txt')
        if os.path.exists(path):
            handle = open(path,'r')
            log = handle.read()
            handle.close()
        else:
            log = ''
        return log

    def FormatException(self, maxtb=5):
        '''Exception Formatting'''
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try: excArgs = exc.__dict__["args"]
        except KeyError: excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxtb)
        return (excName, excArgs, excTb)

    def SendStats(self, *args):
        '''Send the application usage'''
        try: urllib.urlopen('http://mooseproject.000webhost.com/rooms/stats.php')
        except: pass

    def GetIp(self):
        '''Return the current ip'''
        socket.setdefaulttimeout(30)
        if not self._ip:
            try:
                l = re.findall('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', urllib.urlopen("http://checkip.dyndns.org/").read())[0]
                self._ip = '%s.%s.%s.%s' % (l[0],l[1],l[2],l[3])
            except:
                self._ip == ''
        socket.setdefaulttimeout(None)
        return self._ip

    def GetSmile(self, name):
        '''Return the path of a smile'''
        return self.GetSkin().GetPath(name)
        #if os.path.exists(os.path.join(self.SmilesDirectory,name + '.gif')):
        #    return os.path.join(self.SmilesDirectory,name + '.gif')
        #else:
        #    return os.path.join(self.SmilesDirectory,'none.gif')

    def GetName(self):
        return version.GetName()

    def GetVersion(self):
        return version.GetVersion()

    def GetChangelog(self):
        return version.GetChangelog()

    def GetNameVersion(self):
        return '%s %s' % (version.GetName(), version.GetVersion())

    #Metodo che ritorna una carta dato il suo codice
    def FindCardByCode(self, code):
        con = dbapi2.connect(os.path.join(self.BaseDirectory, 'cards.db')) #Mi connetto al db
        c = con.cursor() #Creo un oggetto cursor
        c.execute('SELECT * FROM cards WHERE code="'+code+'"') #Eseguo la query
        row = c.fetchone() #Ottengo i valori trovati
        card = gamecard.GameCard(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]) #Creo la carta
        return card

    #Metodo che ritorna una lista di carte data parte del suo nome
    def FindCardByNameLike(self, name):
        con = dbapi2.connect(os.path.join(self.BaseDirectory, 'cards.db')) #Mi connetto al db
        c = con.cursor() #Creo un oggetto cursor
        c.execute('SELECT * FROM cards WHERE name LIKE "%'+name+'%"') #Eseguo la query
        data = c.fetchall() #Ottengo tutti i valori trovati
        li = list() #Creo la lista che conterra' le carte
        for row in data:
            card = gamecard.GameCard(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]) #Creo la carta
            li.append(card) #Aggiungo alla lista ogni carta
        li.sort(lambda x, y: cmp(x.Name, y.Name))
        return li

    def FindCardByName(self, name):
        con = dbapi2.connect(os.path.join(self.BaseDirectory, 'cards.db')) #Mi connetto al db
        c = con.cursor() #Creo un oggetto cursor
        c.execute('SELECT * FROM cards WHERE name="'+name+'"') #Eseguo la query
        row = c.fetchone() #Ottengo i valori trovati
        card = gamecard.GameCard(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]) #Creo la carta
        return card

    def FinCardByNameAndExp(self, exp, name):
        li = self.FindCardByNameLike(name)
        for c in li:
            if c.Code.upper().count(exp.upper()):
                card = c
                break
        return card

    def AdvancedSearch(self, li):
        if li[0]:
            cards = self.FindCardByNameLike(li[0])
        else:
            cards = self.GetAllCards()
        
        se = []
        if li[1]:
            for c in cards:
                if c.Effect.lower().count(li[1].lower()):
                    se.append(c)
        else:
            se = cards
        
        if li[2] == 'Any':
            return se
        # Monster
        elif li[2] == 'Monster':
            s1 = []
            for c in se:
                if not c.IsMonster():
                    continue
                if li[3] == 'Any':
                    s1.append(c)
                elif li[3] == 'Normal':
                    if not c.Type.count('Effect'):
                        s1.append(c)
                elif li[3] == 'Effect':
                    if c.Type.count('Effect'):
                        s1.append(c)
                elif li[3] == 'Fusion':
                    if c.Type.count('Fusion'):
                        s1.append(c)
                elif li[3] == 'Ritual':
                    if c.Type.count('Ritual'):
                        s1.append(c)
            s2 = []
            if li[4] == 'Any':
                s2 = s1
            else:
                for c in s1:
                    if li[4] == c.Attribute:
                        s2.append(c)
            s3 = []
            if li[5] == '1' and li[6] == '12':
                s3 = s2
            else:
                for c in s2:
                    if int(c.Stars) >= int(li[5]) and int(c.Stars) <= int(li[6]):
                        s3.append(c)
            s4 = []
            if li[7] == '0' and li[8] == '5000':
                s4 = s3
            else:
                for c in s3:
                    if c.Atk.count('?') or c.Atk.count('x') or c.Atk.count('X'):
                        continue
                    if int(c.Atk) >= int(li[7]) and int(c.Atk) <= int(li[8]):
                        s4.append(c)
            s5 = []
            if li[9] == '0' and li[10] == '5000':
                s5 = s4
            else:
                for c in s4:
                    if c.Def.count('?') or c.Def.count('x') or c.Def.count('X'):
                        continue
                    if int(c.Def) >= int(li[9]) and int(c.Def) <= int(li[10]):
                        s5.append(c)
            s6 = []
            if li[11] == 'Any':
                s6 = s5
            else:
                for c in s5:
                    if c.Type.count(li[11]):
                        s6.append(c)
            return s6
        # Spell
        elif li[2] == 'Spell':
            s1 = []
            for c in se:
                if li[3] == 'Any' and c.IsSpell():
                    s1.append(c)
                elif li[3] == c.Type2 and c.IsSpell():
                    s1.append(c)
            return s1
        # Attribute
        elif li[2] == 'Trap':
            s1 = []
            for c in se:
                if li[3] == 'Any' and c.IsTrap():
                    s1.append(c)
                elif li[3] == c.Type2 and c.IsTrap():
                    s1.append(c)
            return s1

    def GetAllCards(self):
        '''Metodo che ritorna la lista completa delle carte'''
        con = dbapi2.connect(os.path.join(self.BaseDirectory, 'cards.db')) #Mi connetto al db
        c = con.cursor() #Creo un oggetto cursor
        c.execute('SELECT * FROM cards') #Eseguo la query
        data = c.fetchall() #Ottengo tutti i valori trovati
        li = list() #Creo la lista che conterra' le carte
        for row in data:
            card = gamecard.GameCard(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]) #Creo la carta
            li.append(card) #Aggiungo alla lista ogni carta
        li.sort(lambda x, y: cmp(x.Name, y.Name))
        return li

    def GetCardImage(self, c):
        p = c.GetCardPosition()
        if p == 2 or p == 3 or p == 4 or p == 5 or p == 6 or p == 9 or p == 10 or p == 11 or p == 12 or p == 13:
            if c.IsTrap():
                return self.GetSkinImage('TrapList')
            elif c.IsRitual():
                return self.GetSkinImage('RitualList')
            elif c.IsSpell():
                return self.GetSkinImage('SpellList')
            elif c.IsFusion():
                return self.GetSkinImage('FusionList')
            elif c.IsNormalMonster():
                return self.GetSkinImage('MonsterList')
            else:
                return self.GetSkinImage('MonsterEffectList')
        if c.IsFaceDown():
            bmp = self.GetSkinImage('CardBack')
            if c.IsHorizontal():
                bmp = self.Rotate90Bitmap(bmp)
            return bmp
        att = c.GetCardAttribute()
        ty = c.GetCardType()
        if att != 'Spell' and att != 'Trap':# Scelgo lo sfondo adatto
            if ty.find('Fusion') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Fusion'), 60, 88)
            elif ty.find('Ritual') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Ritual'), 60, 88)
            elif ty.find('Token') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Token'), 60, 88)
            elif ty.find('Effect') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('MonsterEffect'), 60, 88)
            else:
                b = self.ResizeBitmap(self.GetSkinImage('Monster'), 60, 88)
        elif att == 'Trap':
            b = self.ResizeBitmap(self.GetSkinImage('Trap'), 60, 88)
        elif att == 'Spell':
            b = self.ResizeBitmap(self.GetSkinImage('Spell'), 60, 88)
        bmp = self.GetImageCardScaled(c.GetCardName())
        if not bmp is -1:
            dc = wx.MemoryDC()
            dc.SelectObject(b)
            dc.DrawBitmap(bmp, 8, 19)
        if c.IsHorizontal():
            b = self.Rotate90Bitmap(b)
        return b

    def GetCardGraveImage(self, c):
        att = c.GetCardAttribute()
        ty = c.GetCardType()
        if att != 'Spell' and att != 'Trap':# Scelgo lo sfondo adatto
            if ty.find('Fusion') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Fusion'), 60, 88)
            elif ty.find('Ritual') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Ritual'), 60, 88)
            elif ty.find('Token') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Token'), 60, 88)
            elif ty.find('Effect') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('MonsterEffect'), 60, 88)
            else:
                b = self.ResizeBitmap(self.GetSkinImage('Monster'), 60, 88)
        elif att == 'Trap':
            b = self.ResizeBitmap(self.GetSkinImage('Trap'), 60, 88)
        elif att == 'Spell':
            b = self.ResizeBitmap(self.GetSkinImage('Spell'), 60, 88)
        bmp = self.GetImageCardScaled(c.GetCardName())
        if not bmp is -1:
            dc = wx.MemoryDC()
            dc.SelectObject(b)
            dc.DrawBitmap(bmp, 8, 19)
        return b

    def GetBigCardImage(self, c):
        dc = wx.MemoryDC()
        
        if c.Attribute != 'Spell' and c.Attribute != 'Trap':# Scelgo lo sfondo adatto
            if c.Type.find('Fusion') > -1:
                BackSkin =self.GetSkinImage('Fusion')
            elif c.Type.find('Ritual') > -1:
                BackSkin = self.GetSkinImage('Ritual')
            elif c.Type.find('Token') > -1:
                BackSkin = self.GetSkinImage('Token')
            elif c.Type.find('Effect') > -1:
                BackSkin = self.GetSkinImage('MonsterEffect')
            else:
                BackSkin = self.GetSkinImage('Monster')
        if c.Attribute == 'Trap':
            BackSkin = self.GetSkinImage('Trap')
        if c.Attribute == 'Spell':
            BackSkin = self.GetSkinImage('Spell')
            
        dc.SelectObject(BackSkin) # Carico lo sfondo
        
        dc.SetFont(wx.Font(pointSize=8,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,faceName='Tahoma'))
        dc.DrawText(c.Name[:21], 14,12)# Nome carta, limitato ai primi 20 caratteri
       
        if c.Attribute == 'Light':
            dc.DrawBitmap(self.GetSkinImage('LightIcon'), 110,11, True)
        if c.Attribute == 'Dark':
            dc.DrawBitmap(self.GetSkinImage('DarkIcon'), 110,11, True)
        if c.Attribute == 'Water':
            dc.DrawBitmap(self.GetSkinImage('WaterIcon'), 110,11, True)
        if c.Attribute == 'Fire':
            dc.DrawBitmap(self.GetSkinImage('FireIcon'), 110,11, True)
        if c.Attribute == 'Earth':
            dc.DrawBitmap(self.GetSkinImage('EarthIcon'), 110,11, True)
        if c.Attribute == 'Wind':
            dc.DrawBitmap(self.GetSkinImage('WindIcon'), 110,11, True)
        
        if c.Attribute != 'Trap' and c.Attribute != 'Spell':
            st = 0
            for stelline in range(0, int(c.Stars)):# Assegnazione stelle
                dc.DrawBitmap(self.GetSkinImage('Star'), 110 - st,28, True)
                st += 10
            
        if c.Attribute == 'Trap':
            dc.DrawBitmap(self.GetSkinImage('TrapIcon'), 110,11, True)
            if c.Type2.find('Continuous') > -1: 
                dc.DrawBitmap(self.GetSkinImage('ContinuousIcon'), 90,156, True)
            elif c.Type2.find('Counter') > -1:
                dc.DrawBitmap(self.GetSkinImage('CounterIcon'), 90,156, True)
                
        if c.Attribute == 'Spell':
            dc.DrawBitmap(self.GetSkinImage('SpellIcon'), 110,11)
            if c.Type2.find('Counter') > -1:
                dc.DrawBitmap(self.GetSkinImage('CounterIcon'), 90,156, True)
            elif c.Type2.find('Equip') > -1:
                dc.DrawBitmap(self.GetSkinImage('EquipIcon'), 90,156, True)
            elif c.Type2.find('Field') > -1:
                dc.DrawBitmap(self.GetSkinImage('FieldIcon'), 90,156, True)
            elif c.Type2.find('Ritual') > -1:
                dc.DrawBitmap(self.GetSkinImage('RitualIcon'), 90,156, True)
            elif c.Type2.find('Quick-Play') > -1:
                dc.DrawBitmap(self.GetSkinImage('Quick-PlayIcon'), 90,156, True)
            elif c.Type2.find('Continuous') > -1: 
                dc.DrawBitmap(self.GetSkinImage('ContinuousIcon'), 90,156, True)
        
        cbmp = self.GetImageCard(c.Name)
        if not cbmp is -1:
            dc.DrawBitmap(cbmp, 18, 43)
        
        return dc.GetAsBitmap()

    def ResizeBitmap(self, bmp, w, h, q=wx.IMAGE_QUALITY_HIGH):
        img = wx.ImageFromBitmap(bmp)
        img.Rescale(w, h, q)
        return wx.BitmapFromImage(img)
    
    def Rotate90Bitmap(self, bmp):
        img = wx.ImageFromBitmap(bmp)
        return wx.BitmapFromImage(img.Rotate90())

    def GetImageCardScaled(self, name):
        if self._scaledimagecache.Contains(name):
            img = self._scaledimagecache.GetObj(name)
            return img.GetSubBitmap(wx.Rect(0, 0, img.GetWidth(), img.GetHeight()))
        else:
            path = os.path.join(self.ImagesDirectory, name + '.jpg')
            if os.path.exists(path):
                image = wx.Image(path)
                image.Rescale(45, 45, wx.IMAGE_QUALITY_HIGH)
                bmp = wx.BitmapFromImage(image)
                self._scaledimagecache.AddObj(bmp,name)
                return bmp
        return self.GetSkinImage('none')

    def GetImageCard(self, name):
        if self._imagecache.Contains(name):
            img = self._imagecache.GetObj(name)
            return img.GetSubBitmap(wx.Rect(0, 0, img.GetWidth(), img.GetHeight()))
        else:
            path = os.path.join(self.ImagesDirectory, name + '.jpg')
            if os.path.exists(path):
                img = wx.Bitmap(path)
                self._imagecache.AddObj(img,name)
                return img
        return self.GetSkinImage('none')

    def GetSkin(self): # Metodo che ritorna la skin usata
        key = self.GetSetting('Skin')
        if self.Skins.has_key(key):
            return self.Skins[key]
        else:
            return self.Skins['Default']

    def GetAllSkinName(self):
        li = []
        for sk in self.Skins.keys():
            li.append(sk)
        return li

    def GetSkinName(self):
        return self.GetSetting('Skin')

    def GetLang(self):
        key = self.GetSetting('Language')
        if self.Languages.has_key(key):
            return self.Languages[key]
        else:
            return self.Languages['English']

    def GetAllLangName(self):
        li = []
        for la in self.Languages.keys():
            li.append(la)
        return li

    def GetLangName(self):
        return self.GetSetting('Language')

    def GetAllFonts(self):
        d = {}
        for k in self.Settings.keys():
            if k.startswith('Font-'):
                p = self.Settings[k].split(':')
                
                if p[1] == 'Italic':
                    st = wx.FONTSTYLE_ITALIC
                elif p[1] == 'Max':
                    st = wx.FONTSTYLE_MAX
                elif p[1] == 'Slant':
                    st = wx.FONTSTYLE_SLANT
                else:
                    st = wx.FONTSTYLE_NORMAL
                
                if p[2] == 'Bold':
                    we = wx.FONTWEIGHT_BOLD
                elif p[2] == 'Light':
                    we = wx.FONTWEIGHT_LIGHT
                elif p[2] == 'Max':
                    we = wx.FONTWEIGHT_MAX
                else:
                    we = wx.FONTWEIGHT_NORMAL
                
                f = wx.Font(pointSize=int(p[0]),family=wx.FONTFAMILY_DEFAULT,style=st,weight=we,faceName=p[3])
                d[k[5:]] = f
        return d

    def GetAllFontsName(self):
        l = []
        for k in self.Settings.keys():
            if k.startswith('Font-'):
                l.append(k[5:])
        return l

    def GetAllHotkeys(self):
        d = {}
        for k in self.Settings.keys():
            if k.startswith('Hotkey-'):
                d[k[7:]] = self.Settings[k]
        return d

    def GetAllHotkeysName(self):
        l = []
        for k in self.Settings.keys():
            if k.startswith('Hotkey-'):
                l.append(k[7:])
        return l

    def SetHotkey(self, name, code):
        if self.Settings.has_key('Hotkey-' + name):
            self.Settings['Hotkey-' + name] = code

    def GetHotkeyCode(self, name):
        return self.GetSetting('Hotkey-'+name)

    def GetSkinImage(self, name): # Ritorna un immagine della skin data la sua key
         skin = self.GetSkin()
         if skin.Exists(name):
             return skin.GetImage(name)
         elif self.Skins['Default'].Exists(name):
             return self.Skins['Default'].GetImage(name)
         else:
             return self.Skins['Default'].GetImage('none')

    def GetSetting(self, name):
        if self.Settings.has_key(name):
            return self.Settings[name]
        else:
            return ''

    def SaveSettings(self, st={}):
        for key,value in st.items():
            self.Settings[key] = value
        path = os.path.join(self.BaseDirectory,'settings.xml')
        if os.path.exists(path):
            os.remove(path)
        handle = open(path,'w')
        doc = minidom.Document()
        element = doc.createElement("settings")
        doc.appendChild(element)
        for key,value in self.Settings.items():
            node = doc.createElement("node")
            node.setAttribute('name',key)
            element.appendChild(node)
            node.setAttribute('value',value)
            element.appendChild(node)
        data = doc.toxml()
        handle.write(data)
        handle.close()
        self.Settings = settings.LoadSettings(self.BaseDirectory)

    def GetLangString(self,name, *args):
        lang = self.GetLang()
        if lang.Exists(name):
            s = lang.GetString(name)
        else:
            s = self.Languages['English'].GetString(name)
        for a in args:
            s = s.replace('%s', a, 1)
        return s

    def SaveDeck(self,deck,path):
        handle = open(path,'w')
        doc = minidom.Document()
        element = doc.createElement("deck")
        doc.appendChild(element)
        for c in deck.Cards:
            node = doc.createElement("card")
            node.setAttribute('code',c.Code)
            side = '0'
            if c.IsSide:
                side = '1'
            node.setAttribute('side',side)
            element.appendChild(node)
        data = doc.toxml()
        handle.write(data)
        handle.close()

    def OpenDeck(self,path):
        xmldoc = xmlhandler.LoadXml(path)
        self.Deck = deck.Deck()
        for node in xmldoc.firstChild.childNodes:
            c = self.FindCardByCode(node.getAttribute('code'))
            if node.getAttribute('side') == '1':
                c.IsSide = 1
            self.Deck.Add(c)

    def NewDeck(self):
        self.Deck = deck.Deck()
        self.DeckPath = ''

if __name__ == "__main__":
    e = Engine() # Richiamo il metodo principale dell'applicazione