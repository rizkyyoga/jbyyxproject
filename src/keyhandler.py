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

keys = {wx.WXK_ADD : 'ADD', 
        wx.WXK_ALT : 'ALT', 
        wx.WXK_BACK : 'BACK', 
        wx.WXK_CANCEL : 'CANCEL', 
        wx.WXK_CAPITAL : 'CAPITAL', 
        wx.WXK_CLEAR : 'CLEAR', 
        wx.WXK_COMMAND : 'COMMAND', 
        wx.WXK_CONTROL : 'CONTROL', 
        wx.WXK_DECIMAL : 'DECIMAL', 
        wx.WXK_DELETE : 'DELETE', 
        wx.WXK_DIVIDE : 'DIVIDE', 
        wx.WXK_DOWN : 'DOWN', 
        wx.WXK_END : 'END', 
        wx.WXK_ESCAPE : 'ESCAPE', 
        wx.WXK_EXECUTE : 'EXECUTE', 
        wx.WXK_F1 : 'F1', 
        wx.WXK_F2 : 'F2', 
        wx.WXK_F3 : 'F3', 
        wx.WXK_F4 : 'F4', 
        wx.WXK_F5 : 'F5', 
        wx.WXK_F6 : 'F6', 
        wx.WXK_F7 : 'F7', 
        wx.WXK_F8 : 'F8', 
        wx.WXK_F9 : 'F9', 
        wx.WXK_F10 : 'F10', 
        wx.WXK_F11 : 'F11', 
        wx.WXK_F12 : 'F12', 
        wx.WXK_F13 : 'F13', 
        wx.WXK_F14 : 'F14', 
        wx.WXK_F15 : 'F15', 
        wx.WXK_F16 : 'F16', 
        wx.WXK_F17 : 'F17', 
        wx.WXK_F18 : 'F18', 
        wx.WXK_F19 : 'F19', 
        wx.WXK_F20 : 'F20', 
        wx.WXK_F21 : 'F21', 
        wx.WXK_F22 : 'F22', 
        wx.WXK_F23 : 'F23', 
        wx.WXK_F24 : 'F24', 
        wx.WXK_HELP : 'HELP', 
        wx.WXK_HOME : 'HOME', 
        wx.WXK_INSERT : 'INSERT', 
        wx.WXK_LBUTTON : 'LBUTTON', 
        wx.WXK_LEFT : 'LEFT', 
        wx.WXK_MBUTTON : 'MBUTTON', 
        wx.WXK_MENU : 'MENU', 
        wx.WXK_MULTIPLY : 'MULTIPLY', 
        wx.WXK_NEXT : 'NEXT', 
        wx.WXK_NUMLOCK : 'NUMLOCK', 
        wx.WXK_NUMPAD0 : 'NUMPAD0', 
        wx.WXK_NUMPAD9 : 'NUMPAD9', 
        wx.WXK_NUMPAD1 : 'NUMPAD1', 
        wx.WXK_NUMPAD2 : 'NUMPAD2', 
        wx.WXK_NUMPAD3 : 'NUMPAD3', 
        wx.WXK_NUMPAD4 : 'NUMPAD4', 
        wx.WXK_NUMPAD5 : 'NUMPAD5', 
        wx.WXK_NUMPAD6 : 'NUMPAD6', 
        wx.WXK_NUMPAD7 : 'NUMPAD7', 
        wx.WXK_NUMPAD8 : 'NUMPAD8', 
        wx.WXK_NUMPAD_ADD : 'NUMPAD_ADD', 
        wx.WXK_NUMPAD_BEGIN : 'NUMPAD_BEGIN', 
        wx.WXK_NUMPAD_DECIMAL : 'NUMPAD_DECIMAL',
        wx.WXK_SPACE : 'SPACE'}


def getKey(key):
    if keys.has_key(key):
        return str(keys.get(key))
    else:
        try: return str(chr(key))
        except: return str(key)

def getCode(key, mod):
    if mod == 0: code = ''
    elif mod == 1: code = 'ALT+'
    elif mod == 2: code = 'CTRL+'
    elif mod == 3: code = 'ALT+CTRL+'
    elif mod == 4: code = 'SHIFT+'
    elif mod == 5: code = 'ALT+SHIFT+'
    elif mod == 6: code = 'CTRL+SHIFT+'
    elif mod == 7: code = 'ALT+CTRL+SHIFT+'
    return str(code + getKey(key))

class KeyHandler():
    def __init__(self):
        self._handlers = {}

    def AddHandler(self, code, handler):
        if not self._handlers.has_key(code):
            self._handlers[code] = handler
            return True
        else: return False

    def RemoveHandler(self, code):
        if self._handlers.has_key(code):
            self._handlers.pop(code)
            return True
        else: return False

    def SetHandler(self, code, handler):
        if self._handlers.has_key(code):
            self._handlers[code] = handler
            return True
        else: return False

    def HasHandler(self, code):
        return self._handlers.has_key(code)

    def OnKeyEvent(self, code, mod):
        if code == wx.WXK_ALT or code == wx.WXK_CONTROL or code == wx.WXK_SHIFT: 
            return
        code = getCode(code,mod)
        #try:
        #    code = chr(code)
        #except:
        #    return False
        for c in self._handlers.keys():
            if code == c:
                self._handlers.get(code)()
                return True
        return False
