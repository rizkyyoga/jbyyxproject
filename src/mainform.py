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

import wx, sys, os, webbrowser
from wx import richtext
import engine, network, dialogs, gameframe, room, updater
from printer import DeckPrinter

ID_NEW = 10001
ID_OPEN = 10002
ID_SAVE = 10003
ID_SAVEAS = 10004
ID_PRINT = 10005
ID_CLOSE = 10006
ID_ABOUT = 10007
ID_ADD = 10008
ID_ADD_TO_SIDE = 10009
ID_REMOVE = 10010
ID_POPUP_ADD = 10011
ID_POPUP_ADD_TO_SIDE = 10012
ID_CONNECT = 10013
ID_LISTEN = 10014
ID_PLAY = 10015
ID_ADVANCED = 10016
ID_ROOMS = 10017
ID_WEB = 10018
ID_SETTINGS = 10019
ID_UPDATE = 10020

# Frame principale dell'applicazione
class MainFrame(wx.Frame):
    def __init__(self, engine, *args, **kwargs):
        # Inizializzo la classe padre
        wx.Frame.__init__(self, *args, **kwargs)

        self.Centre() # Centro il frame nello screen
        self.Engine = engine # Creo una variabile che punta all'engine
        self.SelectedFromDeck = ''
        self.SelectedFromSide = False
        self.panel = wx.Panel(self) # Creo il Panel che conterrà i controlli ed i sizer
        self.vbox1 = wx.BoxSizer(wx.VERTICAL) # Sizer Verticale n°1
        self.vbox2 = wx.BoxSizer(wx.VERTICAL) # Sizer Verticale n°2
        self.vbox3 = wx.BoxSizer(wx.VERTICAL) # Sizer Verticale n°3
        self.vbox4 = wx.BoxSizer(wx.VERTICAL) # Sizer Verticale n°4
        self.vbox5 = wx.BoxSizer(wx.VERTICAL) # Sizer Verticale n°5
        self.hbox = wx.BoxSizer(wx.HORIZONTAL) # Sizer Orizzontale che contiene quelli verticali
        self.hmbox1 = wx.BoxSizer(wx.HORIZONTAL) # Sizer per la parte centrale
        self.hmbox2 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox3 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox4 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox5 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox6 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox7 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox8 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox9 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox10 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hmbox11 = wx.BoxSizer(wx.HORIZONTAL) # *
        self.hvbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # Menu
        self.Menu = wx.MenuBar() # Inizializzo il menu
        
        # Status Bar
        self.StatusBar = wx.StatusBar(self,-1) # Creo la StatusBar (parent,campi)
        self.SetStatusBar(self.StatusBar) # Assegno la status bar creata al frame
        self.StatusBar.SetStatusText(self.Engine.GetNameVersion(), 0) # Setto il valore del campo 0 della StatusBar (testo,campo)
        # End Status Bar

        # CardSearch Control
        self.CardSearchCtrl = wx.TextCtrl(self.panel, -1, "") # Creo il controllo di testo che servirà per cercarle le carte (parent, id, testo)
        self.CardSearchCtrl.Bind(wx.EVT_TEXT, self.OnSearchInput, self.CardSearchCtrl) # Faccio il Bind dell'input del testo
        # End CardSearch Control

        # CardList Control
        li = self.Engine.GetAllCards() # Ottengo la lista completa delle carte
        self.DatabaseCardCount = len(li)
        self.CardListCtrl = wx.ListCtrl(parent = self.panel, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES ) # Creo il ListCtrl-
        # -che visualizzerà la lista
        self.CardListCtrl.InsertColumn(0, 'Name') # Creo la colonna che visualizzerà i nomi (index,name)
        self.CardListCtrl.InsertColumn(1, 'Code')
        n = 0 # Ciclo la lista
        for c in li:
            idx = self.CardListCtrl.InsertStringItem(n, c.Name) # Inserisco il nome della carta nel ListCtrl (index,string)
            self.CardListCtrl.SetStringItem(idx, 1, c.Code)
            n += 1
        self.CardListCtrl.SetColumnWidth(0, 250) # La larghezza della colonna 0/'Name'
        self.CardListCtrl.SetColumnWidth(1, 0) # La larghezza della colonna 1/'Code'
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnCardSelected)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnCardListItemRClick)
        self.CardListCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnAddCard)
        # End CardList Control
        
        # ListCtrl del Mazzo
        self.MonsterHeaderText = wx.StaticText(self.panel, -1, 'Monsters: 0')
        self.MonsterListCtrl = wx.ListCtrl(self.panel, -1, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.MonsterListCtrl.InsertColumn(0, 'Monsters')
        self.MonsterListCtrl.SetColumnWidth(0, 200)
        self.MonsterListCtrl.InsertColumn(1, 'Code')
        self.MonsterListCtrl.SetColumnWidth(1, 0)
        self.SpellHeaderText = wx.StaticText(self.panel, -1, 'Spells: 0')
        self.SpellListCtrl = wx.ListCtrl(self.panel, -1, style = wx.LC_REPORT |  wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.SpellListCtrl.InsertColumn(0, 'Spells')
        self.SpellListCtrl.SetColumnWidth(0, 200)
        self.SpellListCtrl.InsertColumn(1, 'Code')
        self.SpellListCtrl.SetColumnWidth(1, 0)
        self.TrapHeaderText = wx.StaticText(self.panel, -1, 'Traps: 0')
        self.TrapListCtrl = wx.ListCtrl(self.panel, -1, style = wx.LC_REPORT |  wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.TrapListCtrl.InsertColumn(0, 'Traps')
        self.TrapListCtrl.SetColumnWidth(0, 200)
        self.TrapListCtrl.InsertColumn(1, 'Code')
        self.TrapListCtrl.SetColumnWidth(1, 0)
        self.SideHeaderText = wx.StaticText(self.panel, -1, 'Side Deck: 0')
        self.SideListCtrl = wx.ListCtrl(self.panel, -1, style = wx.LC_REPORT |  wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.SideListCtrl.InsertColumn(0, 'Side-Deck')
        self.SideListCtrl.SetColumnWidth(0, 200)
        self.SideListCtrl.InsertColumn(1, 'Code')
        self.SideListCtrl.SetColumnWidth(1, 0)
        self.FusionHeaderText = wx.StaticText(self.panel, -1, 'Fusion Deck: 0')
        self.FusionListCtrl = wx.ListCtrl(self.panel, -1, style = wx.LC_REPORT |  wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.FusionListCtrl.InsertColumn(0, 'Fusion-Deck')
        self.FusionListCtrl.SetColumnWidth(0, 200)
        self.FusionListCtrl.InsertColumn(1, 'Code')
        self.FusionListCtrl.SetColumnWidth(1, 0)
        self.MonsterListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnMonsterCardSelected)
        self.SpellListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSpellCardSelected)
        self.TrapListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnTrapCardSelected)
        self.FusionListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnFusionCardSelected)
        self.SideListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSideDeckCardSelected)
        self.DeckCountText = wx.StaticText(self.panel, -1, 'Deck: 0')
        # End Listbox

        # Visualizzazione della carta
        self.CardNameCtrl = wx.StaticText(self.panel, -1, style=wx.ALIGN_CENTRE)
        self.CardImageCtrl = wx.StaticBitmap(self.panel, -1, size=(136,200))
        self.CardDescriptionCtrl = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_CENTRE)
        # End
        
        self.BuildUI()

        # Layout
        
        self.vbox1.Add(self.hvbox1, 0, wx.ALL | wx.EXPAND, 2) # Aggiungo il CardSearchCtrl al vbox1 (control,proprortions,styles,margins)
        self.hvbox1.Add(self.CardSearchCtrl, 1, wx.ALL | wx.EXPAND, 2) # Aggiungo il CardSearchCtrl al vbox1 (control,proprortions,styles,margins)
        self.hvbox1.Add(self.CardReloadCtrl, 0, wx.ALL | wx.EXPAND, 2)
        self.vbox1.Add(self.CardListCtrl, 1, wx.ALL | wx.EXPAND, 2) # Aggiungo il CardListCtrl al vbox1 (control,proprortions,styles,margins)

        self.vbox2.Add(self.hmbox1, 0, wx.ALL | wx.EXPAND, 2) # Parte Centrale del Layout
        self.vbox2.Add(self.hmbox2, 1, wx.ALL | wx.EXPAND, 2) # *
        self.vbox3.Add(self.hmbox3, 0, wx.ALL | wx.EXPAND, 2) # *
        self.vbox3.Add(self.hmbox4, 1, wx.ALL | wx.EXPAND, 2) # *
        self.vbox4.Add(self.hmbox5, 0, wx.ALL | wx.EXPAND, 2) # *
        self.vbox4.Add(self.hmbox6, 1, wx.ALL | wx.EXPAND, 2) # *
        self.vbox2.Add(self.hmbox7, 0, wx.ALL | wx.EXPAND, 2) # *
        self.vbox2.Add(self.hmbox8, 1, wx.ALL | wx.EXPAND, 2) # *
        self.vbox3.Add(self.hmbox9, 0, wx.ALL | wx.EXPAND, 2) # *
        self.vbox3.Add(self.hmbox10, 1, wx.ALL | wx.EXPAND, 2) # *
        self.vbox4.Add(self.hmbox11, 1, wx.ALL | wx.EXPAND, 2) # *
        self.vbox4.AddSpacer(25,0) # *
        self.hmbox1.Add(self.MonsterHeaderText, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox2.Add(self.MonsterListCtrl, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox3.Add(self.SpellHeaderText, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox4.Add(self.SpellListCtrl, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox5.Add(self.TrapHeaderText, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox6.Add(self.TrapListCtrl, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox7.Add(self.SideHeaderText, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox8.Add(self.SideListCtrl, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox9.Add(self.FusionHeaderText, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox10.Add(self.FusionListCtrl, 1, wx.ALL | wx.EXPAND, 2) # *
        self.hmbox11.Add(self.DeckCountText, 1, wx.ALL | wx.EXPAND, 2) # *

        self.vbox5.Add(self.CardNameCtrl, 0, wx.ALL | wx.ALIGN_CENTER , 4)
        self.vbox5.Add(self.CardImageCtrl, 0, wx.ALL | wx.ALIGN_CENTER, 4)
        self.vbox5.Add(self.CardDescriptionCtrl, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 4)
        
        self.hbox.Add(self.vbox1, 1, wx.EXPAND | wx.ALL, 2) # Aggiungo il VBox1 al HBox (control,proprortions,styles,margins)
        self.hbox.Add(self.vbox2, 1, wx.EXPAND | wx.ALL, 2) # Aggiungo il VBox2 al HBox (control,proprortions,styles,margins)
        self.hbox.Add(self.vbox3, 1, wx.EXPAND | wx.ALL, 2) # Aggiungo il VBox3 al HBox (control,proprortions,styles,margins)
        self.hbox.Add(self.vbox4, 1, wx.EXPAND | wx.ALL, 2) # Aggiungo il VBox3 al HBox (control,proprortions,styles,margins)
        self.hbox.Add(self.vbox5, 1, wx.EXPAND | wx.ALL, 2) # Aggiungo il VBox3 al HBox (control,proprortions,styles,margins)
        self.panel.SetSizer(self.hbox) # Setto il sizer del panel
        self.panel.Layout() # Layout del panel
        
        # End Layout
        
        self.AdvancedSearchFrame = dialogs.AdvancedSearch(self)
        self.CardSearchCtrl.SetFocus()

    def BuildUI(self, changes=0):
        if changes:
            self.CardReloadCtrl.Destroy()
            self.GetToolBar().Destroy()
            self.CardListPopupMenu.Destroy()
        
        # Menu
        self.Menu = wx.MenuBar() # Inizializzo il menu

        self.mFile = wx.Menu() # Inizializzo il contenuto della barra dei menu
        self.mGame = wx.Menu()
        self.mTools = wx.Menu()
        self.mHelp = wx.Menu()

        # File Menu
        item = wx.MenuItem(self.mFile,ID_NEW,self.Engine.GetLangString('New'))
        item.SetBitmap(self.Engine.GetSkinImage('New'))
        self.Bind(wx.EVT_MENU, self.OnNew, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_OPEN,self.Engine.GetLangString('Open'))
        item.SetBitmap(self.Engine.GetSkinImage('Open'))
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_SAVE,self.Engine.GetLangString('Save'))
        item.SetBitmap(self.Engine.GetSkinImage('Save'))
        self.Bind(wx.EVT_MENU, self.OnSave, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_SAVEAS,self.Engine.GetLangString('SaveAs'))
        item.SetBitmap(self.Engine.GetSkinImage('SaveAs'))
        self.Bind(wx.EVT_MENU, self.OnSaveAs, item)
        self.mFile.AppendItem(item)
        
        item = wx.MenuItem(self.mFile,ID_ADVANCED,self.Engine.GetLangString('Advanced Search'))
        item.SetBitmap(self.Engine.GetSkinImage('Find'))
        self.Bind(wx.EVT_MENU, self.OnAdvancedSearchMenu, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_PRINT,self.Engine.GetLangString('Print'))
        item.SetBitmap(self.Engine.GetSkinImage('Print'))
        self.Bind(wx.EVT_MENU, self.OnPrint, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_CLOSE,self.Engine.GetLangString('Close'))
        item.SetBitmap(self.Engine.GetSkinImage('Close'))
        self.Bind(wx.EVT_MENU, self.OnMenuClose, item)
        self.mFile.AppendItem(item)
        # End File Menu        
         
        # Game Menu
        
        item = self.mGame.Append(ID_CONNECT, text = self.Engine.GetLangString('Connect'))
        self.Bind(wx.EVT_MENU, self.OnConnectMenu, item)
        
        item = self.mGame.Append(ID_LISTEN, text = self.Engine.GetLangString('Listen'))
        self.Bind(wx.EVT_MENU, self.OnListenMenu, item)

        #item = wx.MenuItem(self.mGame,-1,self.Engine.GetLangString('Duel Channel'))
        #item.SetBitmap(self.Engine.GetSkinImage('Chat'))
        #self.Bind(wx.EVT_MENU, self.OnDuelChannelMenu, item)
        #self.mGame.AppendItem(item)

        item = self.mGame.Append(ID_PLAY, text = self.Engine.GetLangString('Test'))
        self.Bind(wx.EVT_MENU, self.OnPlayMenu, item)

        item = wx.MenuItem(self.mGame,-1,self.Engine.GetLangString('Rooms'))
        item.SetBitmap(self.Engine.GetSkinImage('Chat'))
        self.Bind(wx.EVT_MENU, self.OnRoomsMenu, item)
        self.mGame.AppendItem(item)
        # End Game Menu

        # Tools Menu
        
        item = wx.MenuItem(self.mHelp,-1,self.Engine.GetLangString('Import Deck from YVD...'))
        #item.SetBitmap(self.Engine.GetSkinImage('Import'))
        self.Bind(wx.EVT_MENU, self.OnImportDeck, item)
        self.mTools.AppendItem(item)
        
        # End Tools Menu

        # Help
        item = wx.MenuItem(self.mHelp,ID_SETTINGS,self.Engine.GetLangString('Preferences'))
        item.SetBitmap(self.Engine.GetSkinImage('Preferences'))
        self.Bind(wx.EVT_MENU, self.OnSettings, item)
        self.mHelp.AppendItem(item)

        item = wx.MenuItem(self.mHelp,ID_UPDATE,self.Engine.GetLangString('Update'))
        item.SetBitmap(self.Engine.GetSkinImage('Update'))
        self.Bind(wx.EVT_MENU, self.OnUpdate, item)
        self.mHelp.AppendItem(item)

        item = wx.MenuItem(self.mHelp,ID_WEB,self.Engine.GetLangString('J_PROJECT.Web'))
        item.SetBitmap(self.Engine.GetSkinImage('Web'))
        self.Bind(wx.EVT_MENU, self.OnWeb, item)
        self.mHelp.AppendItem(item)



        item = wx.MenuItem(self.mHelp,ID_ABOUT,self.Engine.GetLangString('About'))
        item.SetBitmap(self.Engine.GetSkinImage('About'))
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        self.mHelp.AppendItem(item)
        # End Help Menu

        self.Menu.Append(self.mFile, self.Engine.GetLangString('File')) # Aggiunge alla barra dei menu le voci
        self.Menu.Append(self.mGame, self.Engine.GetLangString('Game'))
        self.Menu.Append(self.mTools, self.Engine.GetLangString('Tools'))
        self.Menu.Append(self.mHelp, self.Engine.GetLangString('Help'))
        self.SetMenuBar(self.Menu)
        
        # ToolBar
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        self.toolbar.AddLabelTool(ID_NEW, 'New', self.Engine.GetSkinImage('New'), shortHelp = self.Engine.GetLangString('New'), longHelp = self.Engine.GetLangString('Create a new deck'))
        self.toolbar.AddLabelTool(ID_OPEN, 'Open', self.Engine.GetSkinImage('Open'), shortHelp = self.Engine.GetLangString('Open'), longHelp = self.Engine.GetLangString('Open an existent deck'))
        self.toolbar.AddLabelTool(ID_SAVE, 'Save', self.Engine.GetSkinImage('Save'), shortHelp = self.Engine.GetLangString('Save'), longHelp = self.Engine.GetLangString('Save current deck'))
        self.toolbar.AddLabelTool(ID_SAVEAS, 'Save As...', self.Engine.GetSkinImage('SaveAs'), shortHelp = self.Engine.GetLangString('Save As...'), longHelp = self.Engine.GetLangString('Save current deck to a new path'))
        self.toolbar.AddLabelTool(ID_PRINT, 'Print', self.Engine.GetSkinImage('Print'), shortHelp = self.Engine.GetLangString('Print'), longHelp = self.Engine.GetLangString('Print current deck'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(ID_ADVANCED, 'Advanced Search', self.Engine.GetSkinImage('Find'), shortHelp = self.Engine.GetLangString('Advanced Search'), longHelp = self.Engine.GetLangString('Open the Advanced Search Form'))
        self.toolbar.AddLabelTool(ID_ADD, 'Add card to current deck', self.Engine.GetSkinImage('Add'), shortHelp = self.Engine.GetLangString('Add'), longHelp = self.Engine.GetLangString('Add selected card to current deck'))
        self.toolbar.AddLabelTool(ID_ADD_TO_SIDE, 'Add card to side deck', self.Engine.GetSkinImage('AddToSide'), shortHelp = self.Engine.GetLangString('Add To Side'), longHelp = self.Engine.GetLangString('Add selected card to current side deck'))
        self.toolbar.AddLabelTool(ID_REMOVE, 'Remove card from deck', self.Engine.GetSkinImage('Remove'), shortHelp = self.Engine.GetLangString('Remove'), longHelp = self.Engine.GetLangString('Remove selected card from current deck'))
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnAddCard, id=ID_ADD)
        self.Bind(wx.EVT_TOOL, self.OnAddCardToSide, id=ID_ADD_TO_SIDE)
        self.Bind(wx.EVT_TOOL, self.OnRemoveCard, id=ID_REMOVE)
        # End ToolBar
        
        # CardReload Control
        self.CardReloadCtrl = wx.BitmapButton(self.panel, -1, self.Engine.GetSkinImage('Reload'))
        self.CardReloadCtrl.SetToolTipString(self.Engine.GetLangString('Reload'))
        self.CardReloadCtrl.Bind(wx.EVT_BUTTON, self.OnCardReload)
        # EndCardRefresh Control
        
        # CardList Popup
        self.CardListPopupMenu = wx.Menu()
        item = wx.MenuItem(self.CardListPopupMenu,ID_POPUP_ADD,self.Engine.GetLangString('Add to deck'))
        item.SetBitmap(self.Engine.GetSkinImage('Add'))
        self.Bind(wx.EVT_MENU, self.OnAddCard, item)
        self.CardListPopupMenu.AppendItem(item)
        item = wx.MenuItem(self.CardListPopupMenu,ID_POPUP_ADD_TO_SIDE,self.Engine.GetLangString('Add to side-deck'))
        item.SetBitmap(self.Engine.GetSkinImage('AddToSide'))
        self.Bind(wx.EVT_MENU, self.OnAddCardToSide, item)
        self.CardListPopupMenu.AppendItem(item)
        
        if changes:
            self.hvbox1.Add(self.CardReloadCtrl, 0, wx.ALL | wx.EXPAND, 2)

    def RefreshCardList(self):
        self.MonsterListCtrl.DeleteAllItems()
        self.SpellListCtrl.DeleteAllItems()
        self.TrapListCtrl.DeleteAllItems()
        self.SideListCtrl.DeleteAllItems()
        self.FusionListCtrl.DeleteAllItems()
        mo = self.Engine.Deck.GetMonsters()
        mo.sort(lambda x, y: cmp(x.Name, y.Name))
        for c in mo:
            idx = self.MonsterListCtrl.InsertStringItem(self.MonsterListCtrl.GetItemCount(), c.Name)
            self.MonsterListCtrl.SetStringItem(idx, 1, c.Code)
        sp = self.Engine.Deck.GetSpells()
        sp.sort(lambda x, y: cmp(x.Name, y.Name))
        for c in sp:
            idx = self.SpellListCtrl.InsertStringItem(self.SpellListCtrl.GetItemCount(), c.Name)
            self.SpellListCtrl.SetStringItem(idx, 1, c.Code)
        tr = self.Engine.Deck.GetTraps()
        tr.sort(lambda x, y: cmp(x.Name, y.Name))
        for c in tr:
            idx = self.TrapListCtrl.InsertStringItem(self.TrapListCtrl.GetItemCount(), c.Name)
            self.TrapListCtrl.SetStringItem(idx, 1, c.Code)
        fs = self.Engine.Deck.GetFusions()
        fs.sort(lambda x, y: cmp(x.Name, y.Name))
        for c in fs:
            idx = self.FusionListCtrl.InsertStringItem(self.FusionListCtrl.GetItemCount(), c.Name)
            self.FusionListCtrl.SetStringItem(idx, 1, c.Code)
        sd = self.Engine.Deck.GetSide()
        sd.sort(lambda x, y: cmp(x.Name, y.Name))
        for c in sd:
            idx = self.SideListCtrl.InsertStringItem(self.SideListCtrl.GetItemCount(), c.Name)
            self.SideListCtrl.SetStringItem(idx, 1, c.Code)
        self.MonsterListCtrl.SetColumnWidth(0, 200)
        self.SpellListCtrl.SetColumnWidth(0, 200)
        self.TrapListCtrl.SetColumnWidth(0, 200)
        self.SideListCtrl.SetColumnWidth(0, 200)
        self.FusionListCtrl.SetColumnWidth(0, 200)
        # TODO: Implementare languages
        self.DeckCountText.SetLabel('Deck: %s' % str(self.MonsterListCtrl.GetItemCount()+self.SpellListCtrl.GetItemCount()+self.TrapListCtrl.GetItemCount()))
        self.MonsterHeaderText.SetLabel('Monsters: ' + str(self.MonsterListCtrl.GetItemCount()))
        self.SpellHeaderText.SetLabel('Spells: ' + str(self.SpellListCtrl.GetItemCount()))
        self.TrapHeaderText.SetLabel('Traps: ' + str(self.TrapListCtrl.GetItemCount()))
        self.SideHeaderText.SetLabel('Side-Deck: ' + str(self.SideListCtrl.GetItemCount()))
        self.FusionHeaderText.SetLabel('Fusion/Extra Deck: ' + str(self.FusionListCtrl.GetItemCount()))

    # Metodo che mostra un dialogo e ritorna la risposta dell'utente
    # message = Il messaggio letto dall'utente
    # title = Il titolo del dialogo
    # style = Gli stili del dialogo, es. (wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    # Pulsanti visualizzati: wx.OK, wx.CANCEL, wx.YES_NO
    # Pulsante di default: wx.YES_DEFAULT, wx.NO_DEFAULT
    # Icona visualizzata: wx.ICON_EXCLAMATION, wx.ICON_ERROR, wx.ICON_HAND, wx.ICON_INFORMATION, wx.ICON_QUESTION
    # return = wx.ID_OK, wx.ID_CANCEL, wx.ID_YES, wx.ID_NO
    def ShowDialog(self, message, title, style, parent=None):
        if parent == None:
            parent = self
        dialog = wx.MessageDialog(parent,message,title,style)
        return dialog.ShowModal()
    
    def OnConnectMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        dialog = dialogs.ConnectionDialog(self)
        dialog.ShowModal()
    
    def OnListenMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        dialog = dialogs.ListenDialog(self)
        dialog.ShowModal()

    def OnPlayMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        self.Engine.Game._nick = self.Engine.GetSetting('Nick')
        self.Engine.Game.Shuffle()
        self.Engine.GameFrame.Show()

    def OnRoomsMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        dialog = room.Login(self)
        dialog.ShowModal()
        try: dialog.EndTimer()
        except: pass
     
    def OnAdvancedSearchMenu(self, event):
        self.AdvancedSearchFrame.Show()
    
    def OnCardListItemRClick(self,event):
        self.panel.PopupMenu(self.CardListPopupMenu)

    # Metodo che visualizza le carte che contengono la stringa di ricerca
    def OnSearchInput(self, event):
        input = self.CardSearchCtrl.GetValue()
        if len(input) < 3:
            return
        li = self.Engine.FindCardByNameLike(input)
        self.CardListCtrl.DeleteAllItems()
        n=0
        for c in li:
            idx = self.CardListCtrl.InsertStringItem(n,c.Name)
            self.CardListCtrl.SetStringItem(idx, 1, c.Code)
            n+=1
    
    def OnCardReload(self, event):
        li = self.Engine.GetAllCards()
        self.CardListCtrl.DeleteAllItems()
        n=0
        for c in li:
            idx = self.CardListCtrl.InsertStringItem(n,c.Name)
            self.CardListCtrl.SetStringItem(idx, 1, c.Code)
            n+=1
        self.CardListCtrl.SetColumnWidth(0, 200)
        self.CardSearchCtrl.SetValue('')

    # Metodo che visualizza la carta selezionata e la assegna ad self.Selected
    def OnCardSelected(self, event):
        code = self.CardListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.FindCardByCode(code)
        self.SelectedFromDeck = code
        self.ShowCardInfo(card)

    # Metodo che visualizza la carta selezionata e la assegna ad self.Selected
    def OnMonsterCardSelected(self, event):
        code = self.MonsterListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.FindCardByCode(code)
        self.SelectedFromDeck = code
        self.ShowCardInfo(card)

    # Metodo che visualizza la carta selezionata e la assegna ad self.Selected
    def OnSpellCardSelected(self, event):
        code = self.SpellListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.FindCardByCode(code)
        self.SelectedFromDeck = code
        self.ShowCardInfo(card)

    # Metodo che visualizza la carta selezionata e la assegna ad self.Selected
    def OnTrapCardSelected(self, event):
        code = self.TrapListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.FindCardByCode(code)
        self.SelectedFromDeck = code
        self.ShowCardInfo(card)

    # Metodo che visualizza la carta selezionata e la assegna ad self.Selected
    def OnFusionCardSelected(self, event):
        code = self.FusionListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.FindCardByCode(code)
        self.SelectedFromDeck = code
        self.ShowCardInfo(card)

    # Quando una carta del side viene selezionata
    def OnSideDeckCardSelected(self, event):
        code = self.SideListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.FindCardByCode(code)
        self.SelectedFromDeck = code
        self.ShowCardInfo(card)
        self.SelectedFromSide = True

    # Visualizza le informazioni della carta nella colonna di destra
    def ShowCardInfo(self,card):
        self.CardNameCtrl.SetLabel(card.Name)
        self.CardImageCtrl.SetBitmap(self.Engine.GetBigCardImage(card))
        desc = card.Type + '\n'
        if len(card.Type2) > 0:
            desc +=  card.Type2 + '\n'
        if card.Attribute != 'Spell' and card.Attribute != 'Trap':
            desc += card.Attribute + '\n'
            stars = int(card.Stars)
            n = 0
            while n < stars:
                desc += ' * '
                n += 1
            desc += '\n' + 'Atk/' + card.Atk + ' Def/' + card.Def + '\n'
        desc +=  card.Code + '\n\n' + card.Effect
        self.CardDescriptionCtrl.SetValue(desc)
        self.panel.SendSizeEvent()

    # Metodo che aggiunge la carta seleziona al deck
    def OnAddCard(self, event):
        if self.SelectedFromDeck == '':
            return
        c = self.Engine.FindCardByCode(self.SelectedFromDeck)
        self.Engine.Deck.Add(c)
        self.RefreshCardList()

    # Metodo che aggiunge la carta seleziona al side
    def OnAddCardToSide(self, event):
        if self.SelectedFromDeck == '':
            return
        c = self.Engine.FindCardByCode(self.SelectedFromDeck)
        if c.Type.find('Fusion') > -1:
            self.ShowDialog("...",'!',wx.OK | wx.ICON_ERROR)
            return
        c.IsSide = 1
        self.Engine.Deck.Add(c)
        self.RefreshCardList()

    # Metodo che rimuove la carta selezionata dal deck/side
    def OnRemoveCard(self, event):
        if self.SelectedFromDeck == '':
            return
        self.Engine.Deck.RemoveCode(self.SelectedFromDeck,self.SelectedFromSide)
        self.SelectedFromDeck = ''
        self.RefreshCardList()

    # Metodo che crea un nuovo deck
    def OnNew(self, event):
        self.Engine.NewDeck()
        self.SelectedFromDeck = ''
        self.RefreshCardList()

    # Metodo che apre un deck
    def OnOpen(self, event=None, path=''):
        if path == '':
            dialog = wx.FileDialog(self, self.Engine.GetLangString('Open...'), "", "", "XML Deck files (*.xml)|*.xml", wx.FD_OPEN)
            dialog.SetPath(os.path.join(self.Engine.DecksDirectory,'deck.xml'))
            if dialog.ShowModal() != wx.ID_OK:
                dialog.Destroy()
                return
            else:
                name = dialog.GetFilename()
                dir = dialog.GetDirectory()
                path = os.path.join(dir,name)
                dialog.Destroy()
        self.Engine.OpenDeck(path)
        self.Engine.DeckPath = path
        self.RefreshCardList()

    # Metodo che salva il deck senza chiedere il percorso se è stato già salvato o aperto
    def OnSave(self, event):
        if self.Engine.DeckPath != '':
            self.Engine.SaveDeck(self.Engine.Deck,self.Engine.DeckPath)
        else:
            self.OnSaveAs(event)

    # Metodo che salva il deck chiedendo sempre il percorso
    def OnSaveAs(self, event):
        dialog = wx.FileDialog(self, self.Engine.GetLangString("Save As..."), "", "", "XML Deck files (*.xml)|*.xml", wx.FD_SAVE)
        dialog.SetPath(os.path.join(self.Engine.DecksDirectory,'deck.xml'))
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetFilename()
            dir = dialog.GetDirectory()
            path = os.path.join(dir,name)
            if not path.endswith('.xml'):
                path += '.xml'
            self.Engine.SaveDeck(self.Engine.Deck,path)
            self.Engine.DeckPath = path
        dialog.Destroy()

    def OnPrint(self, event):
        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_A4)
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        pdd = wx.PrintDialogData(self.printData)
        pdd.SetToPage(1)
        printer = wx.Printer(pdd)
        printout = DeckPrinter(self.Engine.Deck)
        if not printer.Print(self, printout, True):
            pass
        else:
            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        printout.Destroy()

    # Chiude il programma chiedendo conferma all'utente
    def OnMenuClose(self, event):
        self.Close()

    def OnClose(self, event):
        if self.ShowDialog(self.Engine.GetLangString('Are you sure to quit?'), '?', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.ID_YES:
            try: self.Engine.GameFrame.Close()
            except: pass
            self.Engine.SaveSettings({'LastDeckPath':self.Engine.DeckPath})
            sys.exit()

    # Apre il browser predefinito alla homepage di Moose
    def OnWeb(self, event=None):
        try:
            webbrowser.open_new_tab('http://akademija.visiems.lt/')
        except: pass

    def OnDuelChannelMenu(self, event=None):
        try:
            webbrowser.open_new_tab('http://webchat.azzurra.org/irc.cgi?chan=%23moose-duel')
        except: pass

    # Apre il dialogo delle impostazioni
    def OnSettings(self, event=None):
        dialogs.SettingsDialog(self).ShowModal()
        self.BuildUI(1)

    def OnImportDeck(self, event=None):
        dialogs.ImportDeckDialog(self).ShowModal()

    # Update Check
    def OnUpdate(self, event=None):
      print "Feature is disabled"

    # Mostra la finestra About
    def OnAbout(self, event = None):
        info = wx.AboutDialogInfo()
        info.SetName(self.Engine.GetName())
        info.SetWebSite('http://akademija.visiems.lt')
        info.SetVersion(self.Engine.GetVersion())
        info.SetDescription('J_PROJECT is a multi-platform Yu-Gi-Oh! Dueling and Deck Building application written in Python and using wxPython as GUI Library.')
        info.SetLicense("""J_PROJECT is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free Software Foundation; 
either version 2 of the License, or (at your option) any later version.

J_PROJECT is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with J_PROJECT; if not, write to 
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA""")
        info.AddDeveloper("""Michele 'MaZzo' Mazzoni""")
        info.AddDeveloper("""Andrea 'Coil' Bucciotti""")
        info.AddDeveloper("J_BYYX")
        info.AddArtist("""Michele 'MaZzo' Mazzoni""")
        info.AddArtist("Alexandre 'sa-ki' Moore")
        info.AddArtist("J_BYYX")
        info.AddArtist("TheBeast")
        wx.AboutBox(info)