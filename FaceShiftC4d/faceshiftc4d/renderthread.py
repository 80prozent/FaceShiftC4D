# -*- coding: utf-8 -*-

import c4d
from c4d import bitmaps
from c4d import documents
from faceshiftc4d import ids
from c4d.threading import C4DThread


class RenderThread(C4DThread):
    
    _doc = None
    _flags = None
    
    bmp = None
    rd = None
    
    def __init__(self, aDoc, aFlags):
    
        self._doc = aDoc
        self._flags = aFlags
        
        self.rd = self._doc.GetActiveRenderData()
        
        self.bmp = bitmaps.BaseBitmap()
        self.bmp.Init(int(self.rd[c4d.RDATA_XRES_VIRTUAL]), int(self.rd[c4d.RDATA_YRES_VIRTUAL]), depth=24)

    def Main(self):

        result=documents.RenderDocument(self._doc, self.rd.GetData(), self.bmp, self._flags,self.Get())
        #print result
        if result==c4d.RENDERRESULT_OK:
            pass#print "RENDER OK"
        if result==c4d.RENDERRESULT_OUTOFMEMORY:
            pass#print "RENDER OUTOFMEMORY"
        if result==c4d.RENDERRESULT_ASSETMISSING:
            pass#print "RENDER ASSETMISSING"
        if result==c4d.RENDERRESULT_SAVINGFAILED:
            pass#print "RENDER SAVINGFAILED"
        if result==c4d.RENDERRESULT_USERBREAK:
            pass#print "RENDER USERBREAK"
        if result==c4d.RENDERRESULT_GICACHEMISSING:
            pass#print "RENDER GICACHEMISSING"
        c4d.SpecialEventAdd(ids.PLUGINID)