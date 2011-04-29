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

import wx, sys, os
import engine, keyhandler, deck

class SmilesDialog(wx.Frame):
    def __init__(self, parent, engine, smiles, id=-1, title='Smiles', size=(160,480), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX):
        wx.Frame.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self._scroll = wx.ScrolledWindow(self,-1,(-1,-1),(-1,-1))
        self._scroll.SetScrollbars(0, 1, 0, 100)
        self._engine = engine
        self._smiles = smiles
        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer2 = wx.BoxSizer(wx.VERTICAL)
        
        for smile in self._smiles:
            image = wx.StaticBitmap(self._scroll,-1,wx.Bitmap(self._engine.GetSmile(smile)))
            label = wx.StaticText(self._scroll,-1,':'+smile)
            self._vsizer1.Add(image, 1, wx.ALL | wx.EXPAND, 4)
            self._vsizer2.Add(label, 1, wx.ALL | wx.EXPAND, 4)

        self._hsizer.Add(self._vsizer1, 1, wx.ALL | wx.EXPAND, 4)
        self._hsizer.Add(self._vsizer2, 1, wx.ALL | wx.EXPAND, 4)
        self._scroll.SetSizer(self._hsizer)
        self._scroll.Layout()
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    
    def OnClose(self, event):
        self.Hide()
        

class ConnectionDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title='Connection', size=(-1,-1),style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self.Frame = parent
        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.AddressStaticText = wx.StaticText(self, -1, "Address")
        self.AddressTextCtrl = wx.TextCtrl(self, -1, "127.0.0.1")
        self.PortStaticText = wx.StaticText(self, -1, "Port")
        self.PortTextCtrl = wx.TextCtrl(self, -1, "14120")
        self.NickStaticText = wx.StaticText(self, -1, "Nickname")
        self.NickTextCtrl = wx.TextCtrl(self, -1, self.Frame.Engine.GetSetting('Nick'))
        self.OkButton = wx.Button(self, wx.ID_OK)
        self.CancelButton = wx.Button(self, wx.ID_CANCEL)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.Connect(-1, -1, 500003, self.OnConnection)
        self.Connect(-1, -1, 500004, self.OnConnectionError)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self._vsizer1.Add(self.AddressStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.AddressTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.PortStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.PortTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.NickStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.NickTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.CancelButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.OkButton, 1, wx.ALL | wx.EXPAND, 2)

        self._hsizer.Add(self._vsizer1, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer2, 1, wx.ALL | wx.EXPAND, 2)
        
        self.SetSizer(self._hsizer)
        self.Layout()
        self.Fit()

    def OnClose(self, event):
        return

    def OnOk(self, event):
        self.OkButton.Disable()
        vars = self.GetValues()
        self.Frame.Engine.Network.Connect(vars[0], int(vars[1]), vars[2], self)

    def OnCancel(self, event):
        self.Frame.Engine.Network.StopConnect()
        self.EndModal(0)

    def OnConnection(self, event):
        self.EndModal(2)

    def OnConnectionError(self, event):
        self.Frame.ShowDialog('Connection Error', '', wx.OK | wx.ICON_ERROR, self)
        self.OkButton.Enable()
    
    def GetValues(self):
        vars = []
        vars.append(self.AddressTextCtrl.GetValue())
        vars.append(self.PortTextCtrl.GetValue())
        vars.append(self.NickTextCtrl.GetValue())
        return vars


class ListenDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title='Listen', size=(-1,-1),style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self.CenterOnParent()
        self.Frame = parent
        self._engine = self.Frame.Engine
        self._ipdialog = wx.TextEntryDialog(self, '', '', style=wx.OK, defaultValue='')
        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer2 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer3 = wx.BoxSizer(wx.VERTICAL)
        self.NickStaticText = wx.StaticText(self, -1, "Nickname")
        self.NickTextCtrl = wx.TextCtrl(self, -1, self.Frame.Engine.GetSetting('Nick'))
        self.PortStaticText = wx.StaticText(self, -1, "Port")
        self.PortTextCtrl = wx.TextCtrl(self, -1, "14120")
        self.IpButton = wx.Button(self, -1, label='Get IP')
        self.OkButton = wx.Button(self, wx.ID_OK)
        self.CancelButton = wx.Button(self, wx.ID_CANCEL)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.IpButton.Bind(wx.EVT_BUTTON, self.OnGetIp)
        self.Connect(-1, -1, 500001, self.OnListen)
        self.Connect(-1, -1, 500002, self.OnListenError)

        self._vsizer1.Add(self.PortStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.NickStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.IpButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(2)
        self._vsizer2.Add(self.CancelButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.PortTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.NickTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.OkButton, 1, wx.ALL | wx.EXPAND, 2)

        self._hsizer.Add(self._vsizer1, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer2, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer3, 1, wx.ALL | wx.EXPAND, 2)
        
        self.SetSizer(self._hsizer)
        self.Layout()
        self.Fit()

    def OnGetIp(self, event=None):
        try:
            ip = self._engine.GetIp()
            self._ipdialog.SetValue(ip)
            self._ipdialog.SetTitle(ip)
            self._ipdialog.ShowModal()
        except: pass

    def OnOk(self, event):
        self.OkButton.Disable()
        vars = self.GetValues()
        self.Frame.Engine.Network.Listen(int(vars[0]), vars[1], self)

    def OnCancel(self, event):
        self.Frame.Engine.Network.StopListen()
        self.EndModal(0)

    def OnListen(self, event):
        self.EndModal(2)

    def OnListenError(self, event):
        self.Frame.ShowDialog('Listen Error', '', wx.OK | wx.ICON_ERROR, self)
        self.OkButton.Enable()
    
    def GetValues(self):
        vars = []
        vars.append(self.PortTextCtrl.GetValue())
        vars.append(self.NickTextCtrl.GetValue())
        return vars
    
class AdvancedSearch(wx.Dialog):
    def __init__(self, parent, id = -1, title = 'Advanced Search', size = (400,360)):
        wx.Dialog.__init__(self, parent = parent, id = id, title = title, size = size)
        self._frame = parent
        
        if sys.platform == "win32":
            self.SetSize((400,380))
        
        # Nome Carta
        self.CardNameText = wx.StaticText(self, -1, 'Card Name: ', pos = (12,10))
        self.CardNameCtrl = wx.TextCtrl(self, -1, '', pos = (92,5), size = (140,-1))
        
        # Type
        lista = ['Any','Monster','Spell','Trap']
        self.CardTypeText = wx.StaticText(self, -1, 'Card: ', pos = (12,42))
        self.CardTypeChoice = wx.Choice(self, -1, pos = (90,37), size = (80,-1), choices = lista)
        self.CardTypeChoice.SetStringSelection('Any')
        self.CardTypeChoice.Bind(wx.EVT_CHOICE, self.OnCardTypeChoice)
        
        # SubType
        self.CardSubTypeText = wx.StaticText(self, -1, 'Sub-Type: ', pos = (180, 42))
        self.CardSubTypeText.Hide()
        self.CardSubTypeChoice = wx.Choice(self, -1, pos=(248,37), size=(80,-1), choices=[])
        self.CardSubTypeChoice.Hide()
        
        # Type2
        li = ['Any','Aqua','Beast','Beast-Warrior','Dinosaur','Divine-Beast','Dragon','Fairy','Fiend','Fish','Insect','Machine','Plant','Pyro','Reptile','Rock','Sea Serpent','Spellcaster','Thunder','Warrior','Winged Beast','Zombie','Psychic']
        self.CardType2Text = wx.StaticText(self, -1, 'Type: ', pos = (12, 74))
        self.CardType2Text.Hide()
        self.CardType2Choice = wx.Choice(self, -1, pos=(90,69), size=(80,-1), choices=li)
        self.CardType2Choice.Hide()
        
        # Attributo Mostro
        li = ['Any','Light','Dark','Earth','Wind','Fire','Water','Divine']
        self.CardAttributeText = wx.StaticText(self, -1, 'Attribute: ', pos = (180, 74))
        self.CardAttributeChoice = wx.Choice(self, -1, pos = (248,69), size=(80,-1), choices = li)
        self.CardAttributeChoice.SetStringSelection('Any')
        self.CardAttributeText.Hide()
        self.CardAttributeChoice.Hide()
        
        # Stelle
        self.CardStarsText = wx.StaticText(self, -1, 'Lv:  >=', pos = (12,108))
        self.CardStarsSpin = wx.SpinCtrl(self, -1, '1', pos = (64,103), size =(60,-1), min=1, max=12)
        self.CardStarsText2 = wx.StaticText(self, -1, 'and <=', pos=(134,108))
        self.CardStarsSpin2 = wx.SpinCtrl(self, -1, '12', pos=(184,103), size = (60,-1), min=1, max=12)
        self.CardStarsSpin.Hide()
        self.CardStarsSpin2.Hide()
        self.CardStarsText.Hide()
        self.CardStarsText2.Hide()
        
        # Atk/Def
        self.MonsterAtkText = wx.StaticText(self,-1,'Atk: >=',pos=(12,144))
        self.MonsterAtkSpin = wx.SpinCtrl(self, -1, '0',pos=(64,139),size=(60,-1),min=0,max=5000)
        self.MonsterAtkText2 = wx.StaticText(self,-1,'and <=',pos=(134,144))
        self.MonsterAtkSpin2 = wx.SpinCtrl(self,-1,'5000',pos=(184,139),size=(60,-1),min=0,max=5000)
        self.MonsterAtkSpin.Hide()
        self.MonsterAtkText.Hide()
        self.MonsterAtkSpin2.Hide()
        self.MonsterAtkText2.Hide()
        
        self.MonsterDefText = wx.StaticText(self,-1,'Def: >=',pos=(12,180))
        self.MonsterDefSpin = wx.SpinCtrl(self, -1,'0',pos =(64,175), size = (60,-1),min=0,max=5000)
        self.MonsterDefText2 = wx.StaticText(self,-1,'and <=',pos=(134,180))
        self.MonsterDefSpin2 = wx.SpinCtrl(self, -1,'5000',pos =(184,175), size = (60,-1),min=0,max=5000)
        self.MonsterDefSpin.Hide()
        self.MonsterDefText.Hide()
        self.MonsterDefSpin2.Hide()
        self.MonsterDefText2.Hide()
        
        # Effetto
        self.CardEffect = wx.TextCtrl(self,-1, pos=(24,208),size=(352,100),style = wx.TE_MULTILINE)
        
        # Bottoni
        self.ResetButton = wx.Button(self,-1, 'Reset All Fields',pos=(30,314),size=(-1,-1))
        self.CloseButton = wx.Button(self,-1, 'Close', pos=(160,314),size=(-1,-1))
        self.SearchButton = wx.Button(self,-1,'Search',pos=(280,314),size=(-1,-1))
        
        self.SearchButton.Bind(wx.EVT_BUTTON, self.OnGetAllValue)
        self.CloseButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)
        self.ResetButton.Bind(wx.EVT_BUTTON, self.ResetFields)
        self.Bind(wx.EVT_CLOSE, self.OnCloseButton)

    def OnCardTypeChoice(self, event):
        c = self.CardTypeChoice.GetStringSelection()
        if (c=='Monster'):
            self.CardSubTypeChoice.Clear()
            self.CardSubTypeChoice.AppendItems(['Any','Normal','Effect','Fusion','Ritual','Synchro','Exceed','Toon','Tuner','Gemini','Union'])
            self.CardSubTypeChoice.SetStringSelection('Any')
            self.CardSubTypeText.Show()
            self.CardSubTypeChoice.Show()
            self.CardAttributeChoice.Show()
            self.CardAttributeText.Show()
            self.CardStarsSpin.Show()
            self.CardStarsText.Show()
            self.CardStarsSpin2.Show()
            self.CardStarsText2.Show()
            self.MonsterAtkSpin.Show()
            self.MonsterAtkText.Show()
            self.MonsterAtkSpin2.Show()
            self.MonsterAtkText2.Show()
            self.MonsterDefSpin.Show()
            self.MonsterDefText.Show()
            self.MonsterDefSpin2.Show()
            self.MonsterDefText2.Show()
            self.CardType2Text.Show()
            self.CardType2Choice.Show()
        elif (c == 'Spell'):
            self.CardSubTypeChoice.Clear()
            self.CardSubTypeChoice.AppendItems(['Any','','Continuous','Quick-Play','Equip','Field'])
            self.CardSubTypeChoice.SetStringSelection('Any')
            self.CardSubTypeText.Show()
            self.CardSubTypeChoice.Show()
            self.CardAttributeChoice.Hide()
            self.CardAttributeText.Hide()
            self.CardStarsSpin.Hide()
            self.CardStarsText.Hide()
            self.CardStarsSpin2.Hide()
            self.CardStarsText2.Hide()
            self.MonsterAtkSpin.Hide()
            self.MonsterAtkText.Hide()
            self.MonsterAtkSpin2.Hide()
            self.MonsterAtkText2.Hide()
            self.MonsterDefSpin.Hide()
            self.MonsterDefText.Hide()
            self.MonsterDefSpin2.Hide()
            self.MonsterDefText2.Hide()
            self.CardType2Text.Hide()
            self.CardType2Choice.Hide()
        elif (c == 'Trap'):
            self.CardSubTypeChoice.Clear()
            self.CardSubTypeChoice.AppendItems(['Any','','Continuous','Counter'])
            self.CardSubTypeChoice.SetStringSelection('Any')
            self.CardSubTypeText.Show()
            self.CardSubTypeChoice.Show()
            self.CardAttributeChoice.Hide()
            self.CardAttributeText.Hide()
            self.CardStarsSpin.Hide()
            self.CardStarsText.Hide()
            self.CardStarsSpin2.Hide()
            self.CardStarsText2.Hide()
            self.MonsterAtkSpin.Hide()
            self.MonsterAtkText.Hide()
            self.MonsterAtkSpin2.Hide()
            self.MonsterAtkText2.Hide()
            self.MonsterDefSpin.Hide()
            self.MonsterDefText.Hide()
            self.MonsterDefSpin2.Hide()
            self.MonsterDefText2.Hide()
            self.CardType2Text.Hide()
            self.CardType2Choice.Hide()
        else:
            self.CardSubTypeChoice.Hide()
            self.CardSubTypeText.Hide()
            self.CardAttributeChoice.Hide()
            self.CardAttributeText.Hide()
            self.CardStarsSpin.Hide()
            self.CardStarsText.Hide()
            self.CardStarsSpin2.Hide()
            self.CardStarsText2.Hide()
            self.MonsterAtkSpin.Hide()
            self.MonsterAtkText.Hide()
            self.MonsterAtkSpin2.Hide()
            self.MonsterAtkText2.Hide()
            self.MonsterDefSpin.Hide()
            self.MonsterDefText.Hide()
            self.MonsterDefSpin2.Hide()
            self.MonsterDefText2.Hide()
            self.CardType2Text.Hide()
            self.CardType2Choice.Hide()

    def ResetFields(self, event):
        self.CardNameCtrl.SetValue('')
        self.CardEffect.SetValue('')
        self.CardTypeChoice.SetStringSelection('Any')
        self.CardSubTypeChoice.SetStringSelection('Any')
        self.CardAttributeChoice.SetStringSelection('Any')
        self.CardStarsSpin.SetValue(0)
        self.CardStarsSpin2.SetValue(5000)
        self.MonsterAtkSpin.SetValue(0)
        self.MonsterAtkSpin2.SetValue(5000)
        self.MonsterDefSpin.SetValue(0)
        self.MonsterDefSpin2.SetValue(5000)
        self.OnCardTypeChoice(event)
    
    def OnGetAllValue(self, event):
        li = list()
        li.append(self.CardNameCtrl.GetValue())
        li.append(self.CardEffect.GetValue())
        type = self.CardTypeChoice.GetStringSelection()
        li.append(type)
        if (type == "Monster"):
            li.append(self.CardSubTypeChoice.GetStringSelection())
            li.append(self.CardAttributeChoice.GetStringSelection())
            li.append(self.CardStarsSpin.GetValue())
            li.append(self.CardStarsSpin2.GetValue())
            li.append(self.MonsterAtkSpin.GetValue())
            li.append(self.MonsterAtkSpin2.GetValue())
            li.append(self.MonsterDefSpin.GetValue())
            li.append(self.MonsterDefSpin2.GetValue())
            li.append(self.CardType2Choice.GetStringSelection())
        elif (type == "Spell" or type == "Trap"):
            li.append(self.CardSubTypeChoice.GetStringSelection())
        cards = self._frame.Engine.AdvancedSearch(li)
        self._frame.CardListCtrl.DeleteAllItems()
        n=0
        for c in cards:
            idx = self._frame.CardListCtrl.InsertStringItem(n,c.Name)
            self._frame.CardListCtrl.SetStringItem(idx, 1, c.Code)
            n+=1
        self.Hide()

    def OnCloseButton(self, event):
        self.Hide()

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, frame=None, id=-1, title='Preferences', size=(-1,-1),style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self.CenterOnParent()
        if frame == None: self.Frame = parent
        else: self.Frame = frame

        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer2 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer3 = wx.BoxSizer(wx.VERTICAL)

        self.LanguageText = wx.StaticText(self, -1, "Language:")
        self.LanguageChoice = wx.Choice(self, -1, choices = self.Frame.Engine.GetAllLangName())
        self.LanguageChoice.SetStringSelection(self.Frame.Engine.GetLangName())
        
        self.SkinText = wx.StaticText(self, -1, "Skin:")
        self.SkinChoice = wx.Choice(self, -1, choices = self.Frame.Engine.GetAllSkinName())
        self.SkinChoice.SetStringSelection(self.Frame.Engine.GetSkinName())
        
        self.NickText = wx.StaticText(self, -1, "Nick:")
        self.NickChoice = wx.TextCtrl(self, -1, value=self.Frame.Engine.GetSetting('Nick'))

        self.HotkeysText = wx.StaticText(self, -1, "Hotkeys:")
        self.HotkeysChoice = wx.Choice(self, -1, choices = self.Frame.Engine.GetAllHotkeysName())
        self.HotkeysChoice.SetSelection(0)
        self.HotkeysChoice.Bind(wx.EVT_CHOICE, self.HotkeysChoiceEvent)
        self.HotkeysInput = wx.TextCtrl(self, -1, value=self.Frame.Engine.GetHotkeyCode(self.HotkeysChoice.GetString(self.HotkeysChoice.GetSelection())), style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP)
        self.HotkeysInput.Bind(wx.EVT_KEY_UP, self.OnHotkeysInputKeyUp)

        self.UpdateText = wx.StaticText(self, -1, "Auto-Update:")
        self.UpdateChoice = wx.CheckBox(self, -1, label='', style=wx.ALIGN_RIGHT)
        if self.Frame.Engine.GetSetting('Update') == 'No':
            self.UpdateChoice.SetValue(False)
        else:
            self.UpdateChoice.SetValue(True)

        self.OpenLastDeckText = wx.StaticText(self, -1, "Open Last Deck:")
        self.OpenLastDeckChoice = wx.CheckBox(self, -1, label='', style=wx.ALIGN_RIGHT)
        if self.Frame.Engine.GetSetting('OpenLastDeck') == 'No':
            self.OpenLastDeckChoice.SetValue(False)
        else:
            self.OpenLastDeckChoice.SetValue(True)

        self.ShowFaceUpCardNameText = wx.StaticText(self, -1, "Automatic Images Update:")
        self.ShowFaceUpCardNameChoice = wx.CheckBox(self, -1, label='', style=wx.ALIGN_RIGHT)
        if self.Frame.Engine.GetSetting('ShowFaceUpCardName') == 'No':
            self.ShowFaceUpCardNameChoice.SetValue(False)
        else:
            self.ShowFaceUpCardNameChoice.SetValue(True)

        self.OkButton = wx.Button(self, wx.ID_OK)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk)

        self.CancelButton = wx.Button(self, wx.ID_CANCEL)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        self._vsizer1.Add(self.LanguageText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(1)
        self._vsizer3.Add(self.LanguageChoice, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.Add(self.SkinText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(1)
        self._vsizer3.Add(self.SkinChoice, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.Add(self.NickText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(1)
        self._vsizer3.Add(self.NickChoice, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.Add(self.HotkeysText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.HotkeysChoice, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.HotkeysInput, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.Add(self.UpdateText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(1)
        self._vsizer3.Add(self.UpdateChoice, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.Add(self.OpenLastDeckText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(1)
        self._vsizer3.Add(self.OpenLastDeckChoice, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.Add(self.ShowFaceUpCardNameText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(1)
        self._vsizer3.Add(self.ShowFaceUpCardNameChoice, 1, wx.ALL | wx.EXPAND, 2)

        self._vsizer1.AddStretchSpacer(1)
        self._vsizer2.Add(self.CancelButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.OkButton, 1, wx.ALL | wx.EXPAND, 2)
        
        
        self._hsizer.Add(self._vsizer1, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer2, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer3, 1, wx.ALL | wx.EXPAND, 2)
        self.SetSizer(self._hsizer)
        self.Layout()
        
    def HotkeysChoiceEvent(self, event):
        self.HotkeysInput.SetValue(self.Frame.Engine.GetHotkeyCode(self.HotkeysChoice.GetString(self.HotkeysChoice.GetSelection())))

    def OnHotkeysInputKeyUp(self, event):
        code = event.GetKeyCode()
        mod = event.GetModifiers()
        if code == wx.WXK_ALT or code == wx.WXK_CONTROL or code == wx.WXK_SHIFT or mod == 0: 
            return
        if code == wx.WXK_BACK:
            c = ''
        else:
            c = keyhandler.getCode(code, mod)
        self.HotkeysInput.SetValue(c)
        self.Frame.Engine.SetHotkey(self.HotkeysChoice.GetString(self.HotkeysChoice.GetSelection()), c)

    def OnOk(self, event):
        st = {}
        st['Language'] = self.LanguageChoice.GetString(self.LanguageChoice.GetSelection())
        st['Skin'] = self.SkinChoice.GetString(self.SkinChoice.GetSelection())
        if self.UpdateChoice.IsChecked():
            st['Update'] = 'Yes'
        else:
            st['Update'] = 'No'
        if self.OpenLastDeckChoice.IsChecked():
            st['OpenLastDeck'] = 'Yes'
        else:
            st['OpenLastDeck'] = 'No'
        if self.ShowFaceUpCardNameChoice.IsChecked():
            st['ShowFaceUpCardName'] = 'Yes'
        else:
            st['ShowFaceUpCardName'] = 'No'
        st['Nick'] = self.NickChoice.GetValue()
        self.Frame.Engine.SaveSettings(st)
        self.EndModal(1)

    def OnCancel(self, event):
        self.EndModal(0)

class DeckChooseDialog(wx.Dialog):
    def __init__(self, parent, frame=None, id=-1, title='Deck', size=(500,340),style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self._panel = wx.Panel(self)
        self._hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self._vbox1 = wx.BoxSizer(wx.VERTICAL)
        self._vbox2 = wx.BoxSizer(wx.VERTICAL)
        self._vbox3 = wx.BoxSizer(wx.VERTICAL)
        self._vbox4 = wx.BoxSizer(wx.VERTICAL)

        self._maindecktext = wx.StaticText(self._panel, -1, "Main Deck: 0")
        self._mainlistctrl = wx.ListCtrl(self._panel, -1, style = wx.LC_REPORT |  wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self._tosidebutton = wx.Button(self._panel, -1, '->', size=(-1,32))
        self._tomainbutton = wx.Button(self._panel, -1, '<-', size=(-1,32))
        self._sidelistctrl = wx.ListCtrl(self._panel, -1, style = wx.LC_REPORT |  wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self._sidedecktext = wx.StaticText(self._panel, -1, "Side Deck: 0")
        self._loadbutton = wx.Button(self._panel, -1, 'Load')
        
        self._hbox1.Add(self._vbox1, 4, wx.ALL | wx.EXPAND, 2)
        self._hbox1.Add(self._vbox2, 1, wx.ALL | wx.EXPAND, 2)
        self._hbox1.Add(self._vbox3, 4, wx.ALL | wx.EXPAND, 2)
        self._hbox1.Add(self._vbox4, 2, wx.ALL | wx.EXPAND, 2)

        self._vbox1.Add(self._maindecktext, 0, wx.ALL, 2)
        self._vbox1.Add(self._mainlistctrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vbox2.AddStretchSpacer()
        self._vbox2.Add(self._tosidebutton, 0, wx.ALL | wx.EXPAND, 2)
        self._vbox2.Add(self._tomainbutton, 0, wx.ALL | wx.EXPAND, 2)
        self._vbox2.AddStretchSpacer()
        self._vbox3.Add(self._sidedecktext, 0, wx.ALL, 2)
        self._vbox3.Add(self._sidelistctrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vbox4.AddSpacer(20)
        self._vbox4.Add(self._loadbutton, 0, wx.ALL | wx.EXPAND, 2)
        
        self._panel.SetSizer(self._hbox1)


class ImportDeckDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title='Import a Deck from YVD', size=(600,200), style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=-1, title=title, size=size, style=style)
        self._engine = parent.Engine
        self._inputpath = ''
        self._outputpath = ''
        
        self._vsizer = wx.BoxSizer(wx.VERTICAL)
        self._hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self._hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self._hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        
        self._inputtext = wx.StaticText(self, -1, "Input Path:")
        self._inputctrl = wx.TextCtrl(self, -1, value='', style = wx.TE_READONLY)
        self._inputopen = wx.Button(self, -1, '...')
        self._inputopen.Bind(wx.EVT_BUTTON, self.OnInputOpen)
        
        self._outputtext = wx.StaticText(self, -1, "Output Path:")
        self._outputctrl = wx.TextCtrl(self, -1, value='', style = wx.TE_READONLY)
        self._outputsave = wx.Button(self, -1, '...')
        self._outputsave.Bind(wx.EVT_BUTTON, self.OnOutputSave)

        self._cancelbutton = wx.Button(self, -1, 'Cancel')
        self._cancelbutton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self._importbutton = wx.Button(self, -1, 'Import')
        self._importbutton.Bind(wx.EVT_BUTTON, self.OnImport)
        
        self._hsizer1.Add(self._inputtext, 1, wx.ALL | wx.EXPAND, 4)
        self._hsizer1.Add(self._inputctrl, 3, wx.ALL | wx.EXPAND, 4)
        self._hsizer1.Add(self._inputopen, 0, wx.ALL | wx.EXPAND, 4)
        
        self._hsizer2.Add(self._outputtext, 1, wx.ALL | wx.EXPAND, 4)
        self._hsizer2.Add(self._outputctrl, 3, wx.ALL | wx.EXPAND, 4)
        self._hsizer2.Add(self._outputsave, 0, wx.ALL | wx.EXPAND, 4)
        
        self._hsizer3.AddStretchSpacer(1)
        self._hsizer3.Add(self._cancelbutton, 0, wx.ALL | wx.EXPAND, 4)
        self._hsizer3.Add(self._importbutton, 0, wx.ALL | wx.EXPAND, 4)
        
        self._vsizer.Add(self._hsizer1, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer.Add(self._hsizer2, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer.Add(self._hsizer3, 1, wx.ALL | wx.EXPAND, 2)
        
        self.SetSizer(self._vsizer)
        self.Fit()
    
    def OnInputOpen(self, event):
        dialog = wx.FileDialog(self,'Open...', "", "", "YVD Deck file (*.dek)|*.dek", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetFilename()
            dir = dialog.GetDirectory()
            self._inputpath = os.path.join(dir,name)
            self._inputctrl.SetValue(self._inputpath)
        dialog.Destroy()

    def OnOutputSave(self, event):
        dialog = wx.FileDialog(self, "Save", "", "", "XML Deck file (*.xml)|*.xml", wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetFilename()
            dir = dialog.GetDirectory()
            path = os.path.join(dir,name)
            if not path.endswith('.xml'):
                path += '.xml'
            self._outputpath = path
            self._outputctrl.SetValue(self._outputpath)

    def OnCancel(self, event):
        self.EndModal(0)

    def OnImport(self, event):
        if not os.path.exists(self._inputpath) or not self._outputpath:
            return

        self._cancelbutton.Disable()
        self._importbutton.Disable()
        
        try:
            newdeck = deck.Deck()
            side = 0
            input_handle = open(self._inputpath, 'rb')
            cb = self._engine.GetAllCards()
            while 1:
                line = input_handle.readline()
                line = line.replace('\r\n','')
                if line.endswith(' '):
                    line = line[:len(line)-1]
                line = unicode(line)
                if not line:
                    break
                if line.count('-SIDE DECK-'):
                    side = 1
                else:
                    values = line.split('|')
                    count = int(values[0])
                    for c in cb:
                        if c.Name.upper() == values[2].upper() and c.Code.upper().count(values[1].upper()):
                            cs = c
                            break
                    for i in range(count):
                        card = cs.Duplicate()
                        card.SetIsSide(side)
                        newdeck.Add(card)
            input_handle.close()
            self._engine.SaveDeck(newdeck,self._outputpath)
            self._engine.Frame.ShowDialog('Deck Imported!', '', wx.OK | wx.ICON_INFORMATION, self)
            self.EndModal(1)
        except:
            self._engine.Frame.ShowDialog('Import Error!', '', wx.OK | wx.ICON_ERROR, self)
        self._cancelbutton.Enable()
        self._importbutton.Enable()
            
        