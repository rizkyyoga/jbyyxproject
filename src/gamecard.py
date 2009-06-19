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

class GameCard():

    def __init__(self,code,name,type,attribute,stars,type2,atk,df,effect,side=0):
        self.Code=code
        self.Name=name
        self.Type=type
        self.Attribute=attribute
        self.Stars=stars
        self.Type2=type2
        self.Atk=atk
        self.Def=df
        self.Effect=effect
        self.IsSide = side

    def SetIsSide(self, isside):
        self.IsSide = isside

    def IsMonster(self):
        if self.Attribute != 'Spell' and self.Attribute != 'Trap':
            return True
        else:
            return False

    def IsSpell(self):
        if self.Attribute == 'Spell':
            return True
        else:
            return False

    def IsTrap(self):
        if self.Attribute == 'Trap':
            return True
        else:
            return False

    def Duplicate(self):
        return GameCard(self.Code,self.Name,self.Type,self.Attribute,self.Stars,self.Type2,self.Atk,self.Def,self.Effect,self.IsSide)