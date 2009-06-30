# Tool che facilita la traduzione dei linguaggi by MaZzo

import sys, os, wx
from xml.dom import minidom

class MainFrame(wx.Frame):
    def __init__(self, basepath):
        self._names = []
        self._values = []
        self._basepath = basepath
        self._dir = ''

        wx.Frame.__init__(self, parent=None, title="Moose.LangTool",size=(480,420))
        self._panel = wx.Panel(self)
        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)

        self._menubar = wx.MenuBar()
        self._menufile = wx.Menu()
        
        item = wx.MenuItem(self._menufile,-1,'New Label')
        self.Bind(wx.EVT_MENU, self.OnNewLabel, item)
        self._menufile.AppendItem(item)
        
        item = wx.MenuItem(self._menufile,-1,'Open')
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        self._menufile.AppendItem(item)
        
        item = wx.MenuItem(self._menufile,-1,'Save')
        self.Bind(wx.EVT_MENU, self.OnSave, item)
        self._menufile.AppendItem(item)

        self._menubar.Append(self._menufile, 'File')
        self.SetMenuBar(self._menubar)
        
        self._namelist = wx.ListCtrl(self._panel, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS )
        self._namelist.InsertColumn(0, 'Names')
        self._namelist.SetColumnWidth(0, 80)
        self._namelist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnNameSelected)
        self._namelist.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnNameEdit)

        self._valuelist = wx.ListCtrl(self._panel, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS )
        self._valuelist.InsertColumn(0, 'Values')
        self._valuelist.SetColumnWidth(0, 80)
        self._valuelist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnValueSelected)
        self._valuelist.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnValueEdit)

        self._hsizer.Add(self._namelist, 1, wx.ALL | wx.EXPAND, 4)
        self._hsizer.Add(self._valuelist, 1, wx.ALL | wx.EXPAND, 4)
        
        self._panel.SetSizer(self._hsizer)
        self._panel.Layout()

        self.CenterOnScreen()
        self.Show()

    def OnValueEdit(self, event):
        self._values[event.GetIndex()] = event.GetText()

    def OnNameEdit(self, event):
        self._names[event.GetIndex()] = event.GetText()

    def OnNameSelected(self, event):
        self._valuelist.EnsureVisible(event.GetIndex())
        self._valuelist.Select(event.GetIndex())

    def OnValueSelected(self, event):
        self._namelist.EnsureVisible(event.GetIndex())
        self._namelist.Select(event.GetIndex())

    def OnNewLabel(self, event):
        self._names.append('New Label')
        self._values.append('New Value')
        self._namelist.InsertStringItem(sys.maxint, 'New Label')
        self._valuelist.InsertStringItem(sys.maxint, 'New Value')

    def OnOpen(self, event):
        dialog = wx.FileDialog(self,'Open...', "", "", "XML Language files (*.xml)|*.xml", wx.FD_OPEN)
        dialog.SetPath(self._basepath)
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetFilename()
            dir = dialog.GetDirectory()
            path = os.path.join(dir,name)
            self._dir = dir
            
            self._namelist.DeleteAllItems()
            self._valuelist.DeleteAllItems()

            self._names = []
            self._values = []

            xmldoc = minidom.parse(path)
            for node in xmldoc.firstChild.childNodes:
                name = node.getAttribute('name')
                value = node.getAttribute('value')
                self._names.append(name)
                self._values.append(value)
                self._namelist.InsertStringItem(sys.maxint, name)
                self._valuelist.InsertStringItem(sys.maxint, value)
            
            self._namelist.SetColumnWidth(0,-1)
            self._valuelist.SetColumnWidth(0,-1)
        dialog.Destroy()

    def OnSave(self, event):
        dialog = wx.FileDialog(self, "Save", "", "", "XML Language files (*.xml)|*.xml", wx.FD_SAVE)
        dialog.SetPath(self._dir)
        dialog.SetFilename(self._values[0]+'.xml')
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetFilename()
            dir = dialog.GetDirectory()
            path = os.path.join(dir,name)
            if not path.endswith('.xml'):
                path += '.xml'
            if os.path.exists(path):
                os.remove(path)
            handle = open(path,'w')
            doc = minidom.Document()
            element = doc.createElement("language")
            doc.appendChild(element)
            for i in range(len(self._names)):
                node = doc.createElement("node")
                node.setAttribute('name',self._names[i])
                element.appendChild(node)
                node.setAttribute('value',self._values[i])
                element.appendChild(node)
            data = doc.toxml('utf-8')
            handle.write(data)
            handle.close()
        dialog.Destroy()


if __name__ == '__main__':
    app = wx.App()
    MainFrame()
    app.MainLoop()