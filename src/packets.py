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

import network
import struct

PACKET_CONNECT = 0
PACKET_CHAT = 1
PACKET_DECK = 2
PACKET_DRAW = 3
PACKET_SHUFFLE = 4
PACKET_CARDMOVE = 5
PACKET_CARDFLIP = 6
PACKET_LIFECHANGE = 7
PACKET_PHASE = 8
PACKET_ROLL = 9
PACKET_DISCONNECT = 10
PACKET_TARGET = 11
PACKET_FLIPCOIN = 12
PACKET_RESETGAME = 13
PACKET_LOOK = 14
PACKET_CARDACTION = 15
PACKET_CARDCOUNTER = 16
PACKET_SHUFFLEHAND = 17

class Packet():
    def __init__(self,id):
        self._id = id
        self._buffer = []
        self._fmt = ''

    def GetId(self):
        return self._id

    def Write(self, fmt, data):
        self._fmt += fmt
        self._buffer.append(data)

    def WriteInt(self, data):
        self.Write('i', data)

    def WriteString(self, data):
        """if type(data) is unicode:
            data = data.encode('utf-8')
        elif not type(data) is str:
            data = str(data)
        l = len(data)
        self.WriteInt(l)
        self.Write('%ss' % l, data)"""
        
        if type(data) is unicode:
            data = data.encode('utf-8')
        elif not type(data) is str:
            data = str(data)
        topack = []
        for c in data:
            topack.append(ord(c))
        self.WriteInt(len(topack))
        for b in topack:
            self.WriteInt(b)

    def WriteBool(self, data):
        if data: self.WriteInt(1)
        else: self.WriteInt(0)

    def Build(self):
        self._buffer.insert(0,self._id)
        self._buffer.insert(1,struct.calcsize(self._fmt))
        return struct.pack('>ii'+self._fmt, *self._buffer)

class ConnectPacket(Packet):
    def __init__(self, nickname, version):
        Packet.__init__(self, PACKET_CONNECT) # ID del pacchetto
        self.WriteString(nickname)
        self.WriteString(version)

class ChatPacket(Packet):
    def __init__(self, message):
        Packet.__init__(self, PACKET_CHAT) # ID del pacchetto
        self.WriteString(message)

class DeckPacket(Packet):
    def __init__(self, deck):
        Packet.__init__(self, PACKET_DECK) # ID del pacchetto
        for c in deck:
            self.WriteString(c.Code)
            self.WriteBool(c.IsSide)

class DrawPacket(Packet):
    def __init__(self, reveal):
        Packet.__init__(self, PACKET_DRAW) # ID del pacchetto
        self.WriteBool(reveal)

class ShufflePacket(Packet):
    def __init__(self, deck):
        Packet.__init__(self, PACKET_SHUFFLE) # ID del pacchetto
        for c in deck:
            self.WriteString(c.GetSerial())  

class ShuffleHandPacket(Packet):
    def __init__(self, hand):
        Packet.__init__(self, PACKET_SHUFFLEHAND) # ID del pacchetto
        for c in hand:
            self.WriteString(c.GetSerial())

class CardMovePacket(Packet):
    def __init__(self, serial, dest, dest2=0, x=0, y=0):
        Packet.__init__(self, PACKET_CARDMOVE) # ID del pacchetto
        self.WriteString(serial)
        self.WriteInt(dest)
        self.WriteInt(dest2)
        self.WriteInt(x)
        self.WriteInt(y)

class CardFlipPacket(Packet):
    def __init__(self, serial, state):
        Packet.__init__(self, PACKET_CARDFLIP) # ID del pacchetto
        self.WriteString(serial)
        self.WriteInt(state)

class LifeChangePacket(Packet):
    def __init__(self, offset):
        Packet.__init__(self, PACKET_LIFECHANGE) # ID del pacchetto
        self.WriteInt(offset)

class PhasePacket(Packet):
    def __init__(self, phase):
        Packet.__init__(self, PACKET_PHASE) # ID del pacchetto
        self.WriteInt(phase)

class RollPacket(Packet):
    def __init__(self, faces, n):
        Packet.__init__(self, PACKET_ROLL) # ID del pacchetto
        self.WriteInt(faces)
        self.WriteInt(n)

class DisconnectPacket(Packet):
    def __init__(self):
        Packet.__init__(self, PACKET_DISCONNECT) # ID del pacchetto

class TargetPacket(Packet):
    def __init__(self, p, serial):
        Packet.__init__(self, PACKET_TARGET) # ID del pacchetto
        self.WriteInt(p)
        self.WriteString(serial)

class FlipCoinPacket(Packet):
    def __init__(self, h):
        Packet.__init__(self, PACKET_FLIPCOIN) # ID del pacchetto
        self.WriteBool(h)

class ResetGamePacket(Packet):
    def __init__(self):
        Packet.__init__(self, PACKET_RESETGAME) # ID del pacchetto

class LookPacket(Packet):
    def __init__(self, n):
        Packet.__init__(self, PACKET_LOOK) # ID del pacchetto
        self.WriteInt(n)

class CardActionPacket(Packet):
    def __init__(self, action):
        Packet.__init__(self, PACKET_CARDACTION) # ID del pacchetto
        self.WriteInt(action)

class CardCounterPacket(Packet):
    def __init__(self, serial, action, count):
        Packet.__init__(self, PACKET_CARDCOUNTER) # ID del pacchetto
        self.WriteString(serial)
        self.WriteInt(action)
        self.WriteInt(count)