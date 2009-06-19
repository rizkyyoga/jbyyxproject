# -*- coding: utf-8 -*-__appname__ = 'moose'
__version__ = '0.1.3'
__changelog__ = '''0.1.3
In fase di testing il sistema di Rooms.
Rimpicciolito di il campo, ora non ci dovrebbero essere più problemi
causati dall'eccessiva dimensione della finestra con alcune risoluzioni.
Implementati gli smile nella chat, la lista si trova in Help->Smiles.
Implementati i Counters(Segnalini) delle carte.
Nel dialogo Listen ora è presente un pulsante per ottenere il proprio IP.
Opzione per aprire automaticamente l'ultimo mazzo usato all'avvio del programma.
Quando si cambia lingua o skin la maggior parte dei cambiamenti viene applicata subito.
Nuova opzione per scegliere se visualizzare o meno il nome delle carte scoperte.
Ora dovrebbe essere possibile rimettersi in Listen dopo aver fatto Cancel.
Le carte in mano vengono mandate in fondo al mazzo correttamente.
Fixato il problema di visualizzazione delle carte del side sul terreno.
Nella modalità Test il mazzo viene mischiato automaticamente all'avvio
e viene mostrato il nick correttamente.
Ulteriore miglioramento della lettura dei pachetti in entrata.
I dialoghi Settings,Connection,Listen ora usano i Sizer.
'''

def GetName(): return __name__
def GetVersion(): return __version__
def GetChangelog(): return __changelog__