# Tool che crea un file xml salvando nomi dei files 
# ed il loro hash md5 usato per l'update dell'applicazione
# by Michele 'MaZzo' Mazzoni 2007 GPL 2

import sys, os, md5
from xml.dom import minidom

def GetFileSize(dir, file):
    return str(os.stat(GetFilePath(dir,file))[6])

def GetFilePath(a,b):
    if sys.platform == "win32":
        b = b.replace('/', '\\')
    return os.path.join(a,b)  

# Files da includere
files = ['cards.db','deck.py','dialogs.py','engine.pyw',
         'gamecard.py','gamecontrols.py','gameframe.py','language.py', 'keyhandler.py',
         'mainform.py','network.py','packetevents.py','packets.py',
         'printer.py','room.py','settings.py','skin.py','updater.py','xmlhandler.py',
         'version.py','Languages/English.xml','Languages/Italiano.xml',
         'J_.ico', 'moose32x32.ico', 'moose64x64.png',
         'mooseduel16x16.ico', 'mooseduel32x32.ico', 'mooseduel64x64.png',
         'Skins/Default/Add.png','Skins/Default/AddToSide.png',
         'Skins/Default/CardBack.jpg','Skins/Default/Close.png',
         'Skins/Default/ContinuousIcon.png','Skins/Default/CounterIcon.png',
         'Skins/Default/DarkIcon.png','Skins/Default/Deck.png','Skins/Default/EarthIcon.png',
         'Skins/Default/EquipIcon.png','Skins/Default/Field.png',
         'Skins/Default/FieldIcon.png','Skins/Default/Find.png',
         'Skins/Default/FireIcon.png','Skins/Default/Fusion.jpg',
         'Skins/Default/Grave.png','Skins/Default/LightIcon.png',
         'Skins/Default/Monster.jpg','Skins/Default/MonsterEffect.jpg',
         'Skins/Default/New.png','Skins/Default/Note.png','Skins/Default/Open.png',
         'Skins/Default/OpponentField.png','Skins/Default/Phase.png',
         'Skins/Default/Print.png','Skins/Default/Quick-PlayIcon.png',
         'Skins/Default/Reload.png','Skins/Default/Remove.png',
         'Skins/Default/Ritual.jpg','Skins/Default/RitualIcon.png',
         'Skins/Default/Save.png','Skins/Default/SaveAs.png',
         'Skins/Default/Score.png','Skins/Default/Settings.png',
         'Skins/Default/skin.xml','Skins/Default/Spell.jpg',
         'Skins/Default/SpellIcon.png','Skins/Default/Star.png',
         'Skins/Default/Target.png','Skins/Default/Token.jpg',
         'Skins/Default/Trap.jpg','Skins/Default/TrapIcon.png',
         'Skins/Default/WaterIcon.png','Skins/Default/WindIcon.png','Skins/Default/FusionDeck.png','Skins/Default/RFG.png',
         'Skins/Default/(.gif',
         'Skins/Default/).gif',
         'Skins/Default/angel.gif',
         'Skins/Default/baby.gif',
         'Skins/Default/D.gif',
         'Skins/Default/deer.gif',
         'Skins/Default/disgust.gif',
         'Skins/Default/down.gif',
         'Skins/Default/elf.gif',
         'Skins/Default/flame.gif',
         'Skins/Default/girl.gif',
         'Skins/Default/goccia.gif',
         'Skins/Default/hippy.gif',
         'Skins/Default/I.gif',
         'Skins/Default/king.gif',
         'Skins/Default/kiss.gif',
         'Skins/Default/laughs.gif',
         'Skins/Default/lingua.gif',
         'Skins/Default/look.gif',
         'Skins/Default/love.gif',
         'Skins/Default/mad.gif',
         'Skins/Default/metal.gif',
         'Skins/Default/no.gif',
         'Skins/Default/none.gif',
         'Skins/Default/nu.gif',
         'Skins/Default/O.gif',
         'Skins/Default/oink.gif',
         'Skins/Default/omg.gif',
         'Skins/Default/P.gif',
         'Skins/Default/rain.gif',
         'Skins/Default/S.gif',
         'Skins/Default/sad.gif',
         'Skins/Default/saint.gif',
         'Skins/Default/sheep.gif',
         'Skins/Default/shocked.gif',
         'Skins/Default/sigh.gif',
         'Skins/Default/silly.gif',
         'Skins/Default/smoke.gif',
         'Skins/Default/smokin.gif',
         'Skins/Default/sure.gif',
         'Skins/Default/up.gif',
         'Skins/Default/wave.gif',
         'Skins/Default/X.gif',
         'Skins/Default/zzz.gif']

path = os.path.join(os.getcwd(),'update.xml')
if os.path.exists(path):
    os.remove(path)

handle = open(path,'w')
doc = minidom.Document()
element = doc.createElement("update")
doc.appendChild(element)
for s in files:
    node = doc.createElement("node")
    node.setAttribute('name', s)
    node.setAttribute('value', GetFileSize(os.getcwd(),s))
    element.appendChild(node)
data = doc.toxml()
handle.write(data)
handle.close()
sys.exit()