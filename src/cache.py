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

# Classe per la gestione di una semplice cache
# Se size è 0 la dimensione viene autogestita
# delay sono i secondi dopo i quali un oggetto
# viene rimosso dalla cache, se è 0 è disabilitato

import sys, time

class Cache():
    def __init__(self, size=0, delay=30):
        self._size = size
        self._delay = delay

        # Cache è un lista che a sua volta
        # contiene delle liste che hanno questa forma
        # [object,key,time]
        self._cache = []

    # Pulisco la cache
    def ClearCache(self):
        self._cache = []

    # Cambio la dimensione della cache
    def SetSize(self, size):
        self._size = size
        self.SizeCache()

    # Cambio il delay della cache
    def SetDelay(self, size):
        self._delay = delay
        self.TimeCache()

    # Metodo per aggiornare la cache
    def UpdateCache(self):
        if self._delay > 0:
            self.TimeCache()
        if self._size > 0:
            self.SizeCache()

    # Aggiungo un oggetto alla cache
    # obj -> L'oggetto da aggiungere
    # key -> La chiave per riottenerlo
    # replace -> Se esiste un oggetto
    # con la stessa chiave se replace
    # è 1 lo sostituisce, altrimenti
    # si limita ad aggiornarne il time
    def AddObj(self, obj, key, replace=0):
        self.UpdateCache()
        if not replace:
            for o in self._cache:
                if o[1] == key:
                    self.UpdateObj(o)
                    return
        self._cache.append([obj,key,self.GetTime()])

    # Ritorna un oggetto
    # key -> la sua chiave
    # default -> il valore ritornato
    # se la chiave nn viene trovata
    def GetObj(self, key, default=''):
        obj = default
        for o in self._cache:
            if o[1] == key:
                obj = o[0]
                self.UpdateObj(o)
                break
        return obj

    # Aggiorna il time di un oggetto
    def UpdateObj(self, obj):
        obj[2] = self.GetTime()

    # Rimuove un oggetto
    # key -> la chiave dell'oggetto
    def RemoveObj(self, key):
        for o in self._cache:
            if o[1] == key:
                self._cache.remove(o)
                break

    # Ritorna 1 se la chiave è presente
    # altrimenti 0
    def Contains(self, key):
        for o in self._cache:
            if o[1] == key:
                return 1
        return 0

    # Pulisce la cache usando i time
    def TimeCache(self):
        for o in self._cache:
            if (self.GetTime()-o[2])>self._delay:
                self._cache.remove(o)

    # Pulisce la cache usando la size
    def SizeCache(self):
        while len(self._cache)>self._size:
            self._cache.remove(self.GetOldestObj())

    # Ritorna il time attuale
    def GetTime(self):
        return time.time()

    # Ritorna l'oggetto più vecchio
    def GetOldestObj(self):
        oldest = ['','',sys.maxint]
        for o in self._cache:
            if o[2] < oldest[2]:
                oldest = o
        return o