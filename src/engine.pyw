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

import sys, os, wx, time, re, urllib
from xml.dom import minidom
from sqlite3 import dbapi2
import version, mainform, gamecard, settings, skin, language, deck, xmlhandler
import network, gameframe, dialogs, updater, keyhandler

def ListDirs(path):
    '''Metodo che ritorna una lista contenente tute le directory trovate in <path>'''
    rd = os.listdir(path) # Ottengo la lista di file nel path dato
    dirs = [] # La lista che conterra' le directory
    for s in rd:
        dp = os.path.join(path,s) # Creo una stringa che rappresenta il path del file/directory
        if os.path.isdir(dp): # Testo se e' una directory
            dirs.append(dp) # La aggiungo alla lista
    return dirs # Ritorno la lista

def ListFiles(path):
    '''Metodo che ritorna una lista contenente tute i files trovati in <path>'''
    rd = os.listdir(path) # Ottengo la lista di file nel path dato
    files = [] # La lista che conterra' le directory
    for s in rd:
        dp = os.path.join(path,s) # Creo una stringa che rappresenta il path del file/directory
        if os.path.isfile(dp): # Testo se e' un file
            files.append(dp) # La aggiungo alla lista
    return files # Ritorno la lista

# Classe engine
class Engine():

    #Metodo principale dell'applicazione
    def __init__(self):
        # Controllo se viene lanciata per lo sviluppo
        self._dev = False
        if len(sys.argv) > 1:
            if sys.argv[1] == 'dev':
                self._dev = True

        self.Application = wx.App() # Inizializzo l'applicazione

        # Inizializzo delle variabili contenenti le path delle varie directory
        self.BaseDirectory = ''
        if self._dev:
            self.BaseDirectory = os.path.dirname(os.path.realpath(__file__)) # BaseDirectory
        elif sys.platform == 'win32':
            self.BaseDirectory = os.path.join(os.environ.get('PROGRAMFILES'),'Moose','src')
        elif sys.platform == 'linux2':
            self.BaseDirectory = os.path.join(os.environ.get('HOME'),'.moose','src')
        else:
            self.BaseDirectory = os.getcwd()

        splash = wx.SplashScreen(wx.Bitmap(os.path.join(self.BaseDirectory, 'splash.png'), wx.BITMAP_TYPE_PNG), wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT, 0, None, -1)
        self.SkinsDirectory = os.path.join(self.BaseDirectory, 'Skins') # Skins Directory
        self.LanguagesDirectory = os.path.join(self.BaseDirectory, 'Languages') # Languages Directory
        self.DecksDirectory = os.path.join(self.BaseDirectory, 'Decks') # Decks Directory
        self.ImagesDirectory = os.path.join(self.BaseDirectory, 'Images') # Images Directory

        #Creo le directory se non esistono
        if not os.path.exists(self.SkinsDirectory):
            os.mkdir(self.SkinsDirectory)
        if not os.path.exists(self.LanguagesDirectory):
            os.mkdir(self.LanguagesDirectory)
        if not os.path.exists(self.DecksDirectory):
            os.mkdir(self.DecksDirectory)
        if not os.path.exists(self.ImagesDirectory):
            os.mkdir(self.ImagesDirectory)

        # Variabile che contiene l'ip
        self._ip = ''
    
        self.Settings = settings.LoadSettings(self.BaseDirectory) # Carico le impostazioni

        # Update Check
        if self.GetSetting('Update') == 'Yes':
            toupdate = updater.CheckUpdate(self.BaseDirectory)
            if len(toupdate) > 0:
                if wx.MessageDialog(None,'An update is avaible,\nwould you like to update now?','',wx.YES_NO | wx.ICON_QUESTION | wx.YES_DEFAULT).ShowModal() == wx.ID_YES:
                    updater.Update(self.BaseDirectory,toupdate)
                    wx.MessageDialog(None,'Now you can restart the application.','',wx.OK | wx.ICON_INFORMATION).ShowModal()
                    sys.exit()

        self.Skins = skin.LoadSkins(self.SkinsDirectory) # Carico le skin
        self.Languages = language.LoadLanguages(self.LanguagesDirectory) # Carico i languages

        # Creo un nuovo deck
        self.Deck = deck.Deck()
        self.DeckPath = ''

        self.DatabaseCardsCount = len(self.GetAllCards()) # Inizializzo una variabile contenente il totale delle carte
        
        self.Frame = mainform.MainFrame(engine=self, parent=None, title="J_PROJECT Deck Construction",size=(800,640)) #Inizializzo il frame
        self.Frame.SetIcon(wx.IconFromLocation(wx.IconLocation(os.path.join(self.BaseDirectory,'J_16x16.ico'))))
        
        if self.GetSetting('OpenLastDeck') == 'Yes':
            lastdeckpath = self.GetSetting('LastDeckPath')
            if lastdeckpath and os.path.exists(lastdeckpath):
                self.Frame.OnOpen(path=lastdeckpath)

        splash.Refresh() # Refresh Splash
        time.sleep(1) # Sleep di 1 secondo per mostrare lo splash :P
        splash.Close() # Chiudo lo splash
        self.Frame.Show() # Mostro il frame
        self.Application.MainLoop() # Loop dell'applicazione
    
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
        url = 'http://jbyyxproject.googlecode.com/svn/src/Images/%s.jpg' % n
        try:
            urllib.urlretrieve(url.replace(" ", "%20").replace("#", "%23"), os.path.join(self.ImagesDirectory,'%s.jpg'%n))
            return 1
        except: pass
        return 0

    def DownloadImageList(self):
        if not self.CheckConnection():
            return ''
        url = 'http://jbyyxproject.googlecode.com/svn/src/Images/'
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
    

    def GetIp(self):
        if not self._ip:
            try:
                l = re.findall('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', urllib.urlopen("http://checkip.dyndns.org/").read())[0]
                self._ip = '%s.%s.%s.%s' % (l[0],l[1],l[2],l[3])
            except:
                self._ip == ''
        return self._ip

    def GetSmile(self, name):
        #if os.path.exists(os.path.join(self.SmilesDirectory,name + '.gif')):
        #    return os.path.join(self.SmilesDirectory,name + '.gif')
        #else:
        #    return os.path.join(self.SmilesDirectory,'none.gif')
        return self.GetSkin().GetPath(name)

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
            print c.Name
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
                elif li[3] == 'Synchro':
                    if c.Type.count('Synchro'):
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
            elif c.IsSynchro():
                return self.GetSkinImage('SynchroList')
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
            elif ty.find('Synchro') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Synchro'), 60, 88)              
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
            elif ty.find('Synchro') > -1:
                b = self.ResizeBitmap(self.GetSkinImage('Synchro'), 60, 88)     
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
            elif c.Type.find('Synchro') > -1:
                BackSkin = self.GetSkinImage('Synchro')
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
        path = os.path.join(self.ImagesDirectory, name + '.jpg')
        if os.path.exists(path):
            image = wx.Image(path)
            image.Rescale(45, 45, wx.IMAGE_QUALITY_HIGH)
            return wx.BitmapFromImage(image)
        return -1

    def GetImageCard(self, name):
        path = os.path.join(self.ImagesDirectory, name + '.jpg')
        if os.path.exists(path):
            return wx.Bitmap(path)
        return -1

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