# -*- coding: utf-8 -*-
"""a custom canvas - draws given data as a barchart into a userarea"""


import c4d
from c4d import documents
from c4d import gui
from c4d import plugins

from faceshiftc4d import ids




class CanvasShapes(gui.GeUserArea):

    # the object list supplied by the worker
    data = []

    # step keeping and length for supersimple animation
    step = 0
    steps = 10

    # width of an item and the text widthin
    blockWidth = 0
    fontHeight = 0

    # the index of a clicked item (<0 for none)
    selected = 0
    trainedPoses=[]
    newHeight=0
    renderer=None
    controller=None
    controllData=[]
    controllTag=None
    def __init__(self,renderer):
        self.renderer=renderer
        self.controller=self.renderer._doc.GetObjects()[0]
        self.controllData=[]
        self.controllTag=self.controller.GetTag(1024237)
        if self.controllTag:
            allMorphs=self.controllTag.GetMorphCount()
            morphCnt=1
            while morphCnt<allMorphs:
                self.controllData.append(self.controllTag.GetMorphID(morphCnt))
                morphCnt+=1
        
    
    def GetHeight(self):
        #do a calculation here
        h=self.newHeight
        return h
    def updateControllerData(self, index):
        shapeCnt=0
        while shapeCnt<len(self.controllData):
            if shapeCnt<48:
                self.controllTag[self.controllData[shapeCnt]] =  0.0             
            shapeCnt+=1
        index-=1
        if index>=0:
            self.controllTag[self.controllData[index]]=1.0
        self.renderer._doc.SetChanged()
        self.renderer.Start()
        
    # called on Redraw()
    def DrawMsg(self, x1, y1, x2, y2, msg):

        # set font height and item with
        self.fontHeight = self.DrawGetFontHeight()
        self.blockWidth = self.fontHeight + 2
        print "Height2 = "+str(y2)
        # set offscreen to define the whole canvas as clipping region
        #(normally this would suffice for this type of graphic since
        #we will end up drawing on the whole 'screen' anyway - but the
        #text will get a clipping region so it doesn't overlap the outlines)
        self.OffScreenOn()

        # draw a brackground
        self.DrawSetPen(c4d.COLOR_BG_DARK2)
        self.DrawRectangle(x1,  y1, x2, y2)

        # display a notification of there were no objects found and return
        if len(self.data) < 1:
            txt = "nothing Loadet"# c4d.plugins.GeLoadString(ids.STR_NOOBJECTS_FOUND)
            self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)
            self.DrawText(txt,
                          x2 / 2 - self.DrawGetTextWidth(txt) / 2,
                          y2 / 2 - self.fontHeight / 2)

            return

        # rotate the text-alignment (DONT! forget to reset this)
        #self.DrawSetTextRotation(-90)

        # offsets for text position and a small border
        txtOffsetY = 5
        fillBorder = 1

        # the max polycount
        maxValue = 100#self.data[0][0]

        # iterate all objects...
        for i, dat in enumerate(self.data):
            # (re) set the text color to black
            if len(self.trainedPoses)<i+1:
                self.trainedPoses.append(0)
            self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)

            # scale the actual poly-value to the animation progress
            value = 50#float(dat[0]) / self.steps * self.step

            # the columns offset
            tmpOffsetY = i * 16

            # stop drawing if the element is outside of the visible area
            #if tmpOffsetX > x2: break
            
            # set the clipping region to the column we work on
            self.SetClippingRegion(0, tmpOffsetY,160,tmpOffsetY+16)

            # draw an orange border for this column
            self.DrawBorder(c4d.BORDER_BLACK, 0,tmpOffsetY,160,tmpOffsetY+15)

            # determine offsets and height for an inner, colored bar  
            innerHeight = y2 - fillBorder * 2 - 1
            ty = int(innerHeight - (float(innerHeight) / maxValue * value))
            
            # tint the bar with a color range from yellow to red
            #channelValue = 1.0 / maxValue * value
            self.DrawSetPen(c4d.Vector(0.8, 0.5, 0.5))
            if self.trainedPoses[i]==1:
                self.DrawSetPen(c4d.Vector(0.3, 0.8, 0.3))
                
            self.DrawSetTextCol(c4d.Vector(0, 0, 0),c4d.COLOR_TRANS)
            if i == self.selected:
                self.DrawSetPen(c4d.Vector(0, 0, 0))
                self.DrawSetTextCol(c4d.Vector(1, 0, 0),c4d.COLOR_TRANS)
                if self.trainedPoses[i]==1:
                    self.DrawSetTextCol(c4d.Vector(0, 1, 0),c4d.COLOR_TRANS)
            if i==0:
                self.DrawSetTextCol(c4d.Vector(0.8 , 0.8, 0.8),c4d.COLOR_TRANS)
                self.DrawSetPen(c4d.Vector(0.3, 0.3, 0.3))
                if i == self.selected:
                    self.DrawSetTextCol(c4d.Vector(1, 1, 1),c4d.COLOR_TRANS)
            
            # draw the value bar
            self.DrawRectangle(0 + fillBorder, tmpOffsetY + fillBorder, 160 - fillBorder,tmpOffsetY +16 - fillBorder - 1)

            # clip the text a pixel earlier so it doesn't overlap the outline 
            self.SetClippingRegion(1, tmpOffsetY,160,tmpOffsetY+16)
            
            # draw poly cound and object name 
            self.DrawText(dat,  1,tmpOffsetY+1)
        self.newHeight=tmpOffsetY+16
        print "Height = "+str( self.newHeight)
        # ...remember?
        #self.DrawSetTextRotation(0)

    def InputEvent(self, msg):
        print "Jes"
        # get the input device id
        dev = msg.GetLong(c4d.BFM_INPUT_DEVICE)

        # we dont hadle keyboard-...
        if dev == c4d.BFM_INPUT_KEYBOARD:
            return False
        
        # ...but mouse events
        if dev == c4d.BFM_INPUT_MOUSE:
            return self.HandleMouseEvents(msg)

        return False

    def HandleMouseEvents(self, msg):

        # get the input channel - we need this to...
        chn = msg.GetLong(c4d.BFM_INPUT_CHANNEL)

        # ...check for the left mouse button
        if chn == c4d.BFM_INPUT_MOUSELEFT:
            # get the mouse position and transform it into the canvas space
            mx = msg.GetLong(c4d.BFM_INPUT_X)
            my = msg.GetLong(c4d.BFM_INPUT_Y)    
            mx = mx - self.Local2Global()['x']
            my = my - self.Local2Global()['y']
            
            if mx < len(self.data) * self.blockWidth:
                # get the corresponding element to the clicked column
                index = int(my / 16)
                dat = self.data[index]
    
                # the object was removed since the last update - > return
                #if not dat[2].IsAlive(): return False
        
                # select the clicked object
                doc = documents.GetActiveDocument()
                if doc is None: return False
    
                #doc.SetActiveObject(dat[2])
                c4d.EventAdd()
                
                # mark this object as selected...
                self.selected = index
                self.updateControllerData(index)
                # ...and force a redraw to highlight it
                self.Redraw()
                
                # queue another redraw via the timer to unhighlight it 
                #self.SetTimer(100)
                
                return True

        return False

    # starts the animation
    def draw(self, aData):

        self.data = aData
        self.step = 0


