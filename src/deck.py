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

class Deck():
    def __init__(self):
        self.Cards = []

    def Add(self,card):
        self.Cards.append(card)

    def Remove(self,card):
        if self.Cards.count(card) > 0:
            self.Cards.remove(card)

    def RemoveId(self,id):
        if len(self.Cards)-1 >= id:
            self.Cards.pop(id)

    def RemoveName(self,name,side=False):
        i = 0
        for c in self.Cards:
            if c.Name == name and c.IsSide == side:
                self.Cards.remove(c)
                return
            i += 1

    def RemoveCode(self,code,side=False):
        i = 0
        for c in self.Cards:
            if c.Code == code and c.IsSide == side:
                self.Cards.remove(c)
                return
            i += 1

    def GetMonsters(self):
        li = []
        for c in self.Cards:
            if not c.IsSide and c.Type != 'Spell Card' and c.Type != 'Trap Card' and c.Type.find('Fusion') == -1 and c.Type.find('Synchro') == -1 and c.Type.find('Token') == -1:
                li.append(c)
        return li

    def GetSpells(self):
        li = []
        for c in self.Cards:
            if not c.IsSide and c.Type == 'Spell Card':
                li.append(c)
        return li

    def GetTraps(self):
        li = []
        for c in self.Cards:
            if not c.IsSide and c.Type == 'Trap Card':
                li.append(c)
        return li

    def GetCards(self):
        return self.Cards

    def GetGameCards(self):
        li = []
        for c in self.Cards:
            if c.IsSide == False and c.Type.find('Fusion') == -1 and c.Type.find('Synchro') == -1 and c.Type.find('Token') == -1:
                li.append(c)
        return li

    def GetFusions(self):
        li = []
        for c in self.Cards:
            if c.Type.find('Fusion') > -1 or c.Type.find('Synchro') > -1 or c.Type.find('Token') > -1:
                li.append(c)
        return li

    def GetSide(self):
        li = []
        for c in self.Cards:
            if c.IsSide:
                li.append(c)
        return li