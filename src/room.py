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

import urllib, threading, wx, sys, md5, re


class OnGetRoomsEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(510001)
        self.data = data

class Login(wx.Dialog):
    def __init__(self, parent, id=-1, title='Login', size=(-1,-1),style=wx.CAPTION):
        self.Frame = parent
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self._vsizer = wx.BoxSizer(wx.VERTICAL)
        self._hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self._hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self._hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self._hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.ServerStaticText = wx.StaticText(self, -1, "Server")
        self.ServerTextCtrl = wx.TextCtrl(self, -1, "http://jproject.xz.lt/")
        self.UserStaticText = wx.StaticText(self, -1, "Username")
        self.UserTextCtrl = wx.TextCtrl(self, -1, self.Frame.Engine.GetSetting('Nick'))
        self.PasswordStaticText = wx.StaticText(self, -1, "Password")
        self.PasswordTextCtrl = wx.TextCtrl(self, -1, "", style = wx.TE_PASSWORD)
        self.PasswordTextCtrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.OkButton = wx.Button(self, wx.ID_OK)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.CreateButton = wx.Button(self, wx.ID_NEW, label='Create an Account')
        self.CreateButton.Bind(wx.EVT_BUTTON, self.OnCreate)
        self.CancelButton = wx.Button(self, wx.ID_CANCEL)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.PasswordTextCtrl.SetFocus()
        
        self._hsizer1.Add(self.ServerStaticText, 1, wx.ALL | wx.EXPAND, 3)
        self._hsizer1.Add(self.ServerTextCtrl, 3, wx.ALL | wx.EXPAND, 3)

        self._hsizer2.Add(self.UserStaticText, 1, wx.ALL | wx.EXPAND, 3)
        self._hsizer2.Add(self.UserTextCtrl, 3, wx.ALL | wx.EXPAND, 3)

        self._hsizer3.Add(self.PasswordStaticText, 1, wx.ALL | wx.EXPAND, 3)
        self._hsizer3.Add(self.PasswordTextCtrl, 3, wx.ALL | wx.EXPAND, 3)

        self._hsizer4.Add(self.CreateButton, 1, wx.ALL | wx.EXPAND, 4)
        self._hsizer4.AddStretchSpacer(1)
        self._hsizer4.Add(self.CancelButton, 1, wx.ALL | wx.EXPAND, 4)
        self._hsizer4.Add(self.OkButton, 1, wx.ALL | wx.EXPAND, 4)

        self._vsizer.Add(self._hsizer1, 6, wx.ALL | wx.EXPAND, 1)
        self._vsizer.Add(self._hsizer2, 6, wx.ALL | wx.EXPAND, 1)
        self._vsizer.Add(self._hsizer3, 6, wx.ALL | wx.EXPAND, 1)
        self._vsizer.Add(self._hsizer4, 7, wx.ALL | wx.EXPAND, 1)
        
        self.SetSizer(self._vsizer)
        self.Layout()
        self.Fit()

    def OnKeyUp(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.OnOk(event)

    def OnCreate(self, event):
        self.Disable()
        user = self.UserTextCtrl.GetValue()
        if (len(user) < 4):
            self.Frame.ShowDialog('The Username must be at least 4 characters.', '!', wx.OK | wx.ICON_ERROR, self)
            self.Enable()
            return
        
        password = self.PasswordTextCtrl.GetValue()
        if (len(password) < 4):
            self.Frame.ShowDialog('The Password must be at least 4 characters.', '!', wx.OK | wx.ICON_ERROR, self)
            self.Enable()
            return

        dialog = wx.TextEntryDialog(self, 'Enter your e-mail address', '')
        if dialog.ShowModal() == wx.ID_OK:
            email = dialog.GetValue()

            match = re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", email)
            if not match:
                self.Frame.ShowDialog('Invalid E-Mail.', '!', wx.OK | wx.ICON_ERROR, self)
                self.Enable()
                return
        else:
            self.Enable()
            return

        server = self.ServerTextCtrl.GetValue()
        if not server.endswith('/'):
            server += '/'
        if not server.startswith('http://'):
            server = 'http://' + server
        password_md5 = md5.new(password).hexdigest()
        url = '%screate.php?user=%s&password=%s&email=%s' % (server,user,password_md5,email)
        res = urllib.urlopen(url)
        ret = res.readline()
        if (ret == '0'):
            self.Frame.ShowDialog('Account Created!', '', wx.OK | wx.ICON_INFORMATION, self)
        elif (ret == '9'):
            self.Frame.ShowDialog('Connection problem.', '!', wx.OK | wx.ICON_ERROR, self)
        elif (ret == '8'):
            self.Frame.ShowDialog('Incorrect parameters.', '!', wx.OK | wx.ICON_ERROR, self)
        elif (ret == '7'):
            self.Frame.ShowDialog('Username already taken.', '!', wx.OK | wx.ICON_ERROR, self)
        elif (ret == '6'):
            self.Frame.ShowDialog('E-Mail already used.', '!', wx.OK | wx.ICON_ERROR, self)
        else:
            self.Frame.ShowDialog('Unknown Error.\n%s' % self.GetError(res, ret), '!', wx.OK | wx.ICON_ERROR, self)
        self.Enable()

    def GetError(self, source, part=''):
        while 1:
            s = source.readline()
            if s == '':
                break
            part += s + '\n'
        return part

    def OnOk(self, event):
        self.OkButton.Disable()
        room = Room(self.Frame)
        room.SetServer(self.ServerTextCtrl.GetValue())
        ret = room.Login(self.UserTextCtrl.GetValue(), self.PasswordTextCtrl.GetValue(), self.Frame.Engine.GetVersion())
        if (ret == '0'):
            self.EndModal(0)
            room.ShowModal()
        elif (ret == '9'):
            self.Frame.ShowDialog('Connection problem.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()
        elif (ret == '8'):
            self.Frame.ShowDialog('Incorrect parameters.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()
        elif (ret == '7'):
            self.Frame.ShowDialog('Wrong username.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()
        elif (ret == '6'):
            self.Frame.ShowDialog('User already connected.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()
        elif (ret == '5'):
            self.Frame.ShowDialog('Wrong password.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()
        elif (ret == '4'):
            self.Frame.ShowDialog('Inactive Account.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()
        else:
            self.Frame.ShowDialog('Unknown Error.', '!', wx.OK | wx.ICON_ERROR, self)
            self.OkButton.Enable()

    def OnCancel(self, event):
        self.EndModal(0)

class Room(wx.Dialog):
    def __init__(self, parent, id=-1, title='Server', size=(330,400),style=wx.CAPTION):
        self._server = ''
        self._user = ''
        self._logged = False
        self._rooms = []
        self._createroom = 0
        self._onlinecount = '?'
        self._timer = threading.Timer(5.0, self.OnTimer)
        self._last = -1
        self.Frame = parent
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        if sys.platform == "win32":
            self.SetSize((330,440))
        self._roomlistctrl = wx.ListCtrl(parent = self, size=(240,395), pos=(0,0), style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_NO_HEADER )
        self._roomlistctrl.InsertColumn(0, '')
        self._roomlistctrl.SetColumnWidth(0, 240)
        self.ConnectButton = wx.Button(self, -1, pos=(245,5), label="Connect")
        self.ConnectButton.Bind(wx.EVT_BUTTON, self.OnConnectButton)
        self.CreateButton = wx.Button(self, -1, pos=(245,40), label="Create")
        self.CreateButton.Bind(wx.EVT_BUTTON, self.OnCreateButton)
        self.DeleteButton = wx.Button(self, -1, pos=(245,75), label="Delete")
        self.DeleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        self.DeleteButton.Disable()
        self.OnlineText = wx.StaticText(self, -1, pos=(245,320), size=(-1,100), label="Online: ???")
        self.ExitButton = wx.Button(self, -1, pos=(245,360), label="Exit")
        self.ExitButton.Bind(wx.EVT_BUTTON, self.OnExitButton)
        self.Connect(-1, -1, 500001, self.OnListen)
        self.Connect(-1, -1, 500002, self.OnListenError)
        self.Connect(-1, -1, 500003, self.OnConnection)
        self.Connect(-1, -1, 500004, self.OnConnectionError)
        self.Connect(-1, -1, 510001, self.GetRooms)

    def EndTimer(self):
        self._timer.cancel()

    def UpdateOnline(self):
        self.OnlineText.SetLabel('Online: %s'%self._onlinecount)

    def OnTimer(self, *args):
        wx.PostEvent(self, OnGetRoomsEvent(''))

    def OnConnection(self, event):
        self._timer.cancel()
        self.EndModal(2)

    def OnConnectionError(self, event):
        self.Frame.ShowDialog('Connection Error', '', wx.OK | wx.ICON_ERROR)

    def OnListen(self, event):
        self._timer.cancel()
        self.EndModal(2)

    def OnListenError(self, event):
        self.DeleteRoom()
        self.Frame.ShowDialog('Listen Error', '', wx.OK | wx.ICON_ERROR)

    def OnConnectButton(self, event):
        if (self._roomlistctrl.GetSelectedItemCount() < 1):
            return
        id = self._roomlistctrl.GetNextItem(-1, state = wx.LIST_STATE_SELECTED)
        if id == -1:
            return
        s = self._rooms[id].split('</field/>')[2]
        self.Frame.Engine.Network.Connect(s, 14120, self._user, self)

    def OnCreateButton(self, event):
        dialog = wx.TextEntryDialog(self, "Insert the room's name.")
        if (dialog.ShowModal() == wx.ID_OK):
            name = dialog.GetValue()
            if not (self.ValidateRoomName(name)):
                self.Frame.ShowDialog("Room's name invalid.\nValid characters:\n a-z 0-9 ;,:._-", '!', wx.OK | wx.ICON_ERROR, self)
            else:
                self.CreateRoom(name)
                self.ConnectButton.Disable()
                self.CreateButton.Disable()
                self.DeleteButton.Enable()

    def ValidateRoomName(self, name):
        match = re.match('[a-z0-9;,:._-]{1,24}$', name, re.IGNORECASE)
        return bool(match)

    def OnDeleteButton(self, event):
        self.DeleteRoom()

    def OnExitButton(self, event):
        self.Logout()
        self.EndModal(0)

    def GetServer(self):
        return self._server

    def SetServer(self, server):
        if not server.endswith('/'):
            server += '/'
        if not server.startswith('http://'):
            server = 'http://' + server
        self._server = server

    def Login(self, user, password, version):
        if (self._logged):
            return
        self._user = user
        password_md5 = md5.new(password).hexdigest()
        url = '%slogin.php?user=%s&password=%s&version=%s' % (self.GetServer(),self._user,password_md5,version)
        res = urllib.urlopen(url)
        ret = res.readline()
        if ( ret == '0'):
            self._logged = True
            self.GetRooms()
        return ret

    def Logout(self):
        if not (self._logged):
            return
        if self._createroom:
            self.DeleteRoom()
        url = '%slogout.php?user=%s' % (self.GetServer(),self._user)
        res = urllib.urlopen(url)
        ret = res.readline()
        if ( ret == '0'):
            self._logged = False
            self._timer.cancel()
            self.Refresh()

    def GetRooms(self, timer=True):
        if not (self._logged):
            return
        url = '%sroom.php?user=%s&action=get' % (self.GetServer(), self._user)
        res = urllib.urlopen(url)
        ret = res.read()
        split = ret.split('/r/')
        id = self._roomlistctrl.GetNextItem(-1, state = wx.LIST_STATE_SELECTED)
        if id != -1:
            self._last = self._roomlistctrl.GetItemText(id)
        else:
            self._lst = ''
        if (split[0] == '0'):
            self._onlinecount = split[1]
            self.UpdateOnline()
            self._rooms = split[2:]
            for r in self._rooms:
                fs = r.split('</field/>')
        if (timer):
            self._timer = threading.Timer(5.0, self.OnTimer)
            self._timer.start()
        self.RefreshRoomList()

    def RefreshRoomList(self):
        self._roomlistctrl.DeleteAllItems()
        n = 0
        for i in self._rooms:
            split = i.split('</field/>')
            s =  "%s | %s" % (split[0], split[1])
            self._roomlistctrl.InsertStringItem(n, s)
            if (self._last != '' and self._last == s):
                self._roomlistctrl.Select(n)
            n += 1

    def CreateRoom(self, name):
        if not (self._logged):
            return
        self._createroom = 1
        url = '%sroom.php?user=%s&action=create&room=%s' % (self.GetServer(),self._user, name)
        res = urllib.urlopen(url)
        ret = res.readline()
        self.Frame.Engine.Network.Listen(14120, self._user, self)
        self.GetRooms(False)

    def DeleteRoom(self):
        if not (self._logged):
            return
        self._createroom = 0
        self.Frame.Engine.Network.StopListen()
        url = '%sroom.php?user=%s&action=delete' % (self.GetServer(),self._user)
        res = urllib.urlopen(url)
        ret = res.readline()
        self.ConnectButton.Enable()
        self.CreateButton.Enable()
        self.DeleteButton.Disable()
        self.GetRooms(False)
    
