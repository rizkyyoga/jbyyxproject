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

import wx

EVT_CONNECT = 3001
EVT_CHAT = 3002
EVT_DECK = 3003
EVT_DRAW = 3004
EVT_SHUFFLE = 3005
EVT_CARDMOVE = 3006
EVT_CARDFLIP = 3007
EVT_LIFECHANGE = 3008
EVT_PHASE = 3009
EVT_ROLL = 3010
EVT_DISCONNECT = 3011
EVT_TARGET = 3012
EVT_FLIPCOIN = 3013
EVT_RESETGAME = 3014
EVT_LOOK = 3015
EVT_CARDACTION = 3016
EVT_CARDCOUNTER = 3017

class PacketConnectEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CONNECT)
        self.data = data

class PacketChatEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CHAT)
        self.data = data

class PacketDeckEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DECK)
        self.data = data

class PacketDrawEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DRAW)
        self.data = data

class PacketShuffleEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SHUFFLE)
        self.data = data

class PacketCardMoveEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CARDMOVE)
        self.data = data

class PacketCardFlipEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CARDFLIP)
        self.data = data

class PacketLifeChangeEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LIFECHANGE)
        self.data = data

class PacketPhaseEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_PHASE)
        self.data = data

class PacketRollEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_ROLL)
        self.data = data

class PacketDisconnectEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DISCONNECT)
        self.data = data

class PacketTargetEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TARGET)
        self.data = data

class PacketFlipCoinEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_FLIPCOIN)
        self.data = data

class PacketResetGameEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESETGAME)
        self.data = data

class PacketLookEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LOOK)
        self.data = data

class PacketCardActionEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CARDACTION)
        self.data = data

class PacketCardCounterEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CARDCOUNTER)
        self.data = data