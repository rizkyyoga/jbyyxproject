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
         'version.py','Languages/English.xml','Languages/Italiano.xml','Languages/Lietuviu.xml']

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