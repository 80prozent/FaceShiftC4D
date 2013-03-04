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
    typeOfRender=0
    continious=False
    def __init__(self, aDoc, typeOfRender,aFlags,continious=False):
    
        self.continious = continious
        self._doc = aDoc
        self.typeOfRender=typeOfRender
        self._flags = aFlags
        
        self.rd = self._doc.GetActiveRenderData()
        
        self.bmp = bitmaps.BaseBitmap()
        self.bmp.Init(int(self.rd[c4d.RDATA_XRES_VIRTUAL]), int(self.rd[c4d.RDATA_YRES_VIRTUAL]), depth=24)

    def Main(self):
        result=c4d.RENDERRESULT_OK
        if self.continious==False:
            result=documents.RenderDocument(self._doc, self.rd.GetData(), self.bmp, self._flags,self.Get())
            if self.typeOfRender==ids.TABGRP_LIVESTREAM:
                c4d.SpecialEventAdd(ids.EVT_FINISHEDRENDER1)
            if self.typeOfRender==ids.TABGRP_EXPRESSIONMAPPING:
                c4d.SpecialEventAdd(ids.EVT_FINISHEDRENDER2)
        if self.continious==True:
            while result==c4d.RENDERRESULT_OK:
                if self.TestBreak():
                    return
                result=documents.RenderDocument(self._doc, self.rd.GetData(), self.bmp, self._flags,self.Get())
            #print result
                if self.typeOfRender==ids.TABGRP_LIVESTREAM:
                    c4d.SpecialEventAdd(ids.EVT_FINISHEDRENDER1)
                if self.typeOfRender==ids.TABGRP_EXPRESSIONMAPPING:
                    c4d.SpecialEventAdd(ids.EVT_FINISHEDRENDER2)
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