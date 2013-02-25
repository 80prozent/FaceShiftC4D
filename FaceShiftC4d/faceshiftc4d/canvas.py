# -*- coding: utf-8 -*-
"""a custom canvas - draws given data as a barchart into a userarea"""


import c4d
from c4d import documents
from c4d import gui
from c4d import plugins

from faceshiftc4d import ids


class Canvas(gui.GeUserArea):

    # the object list supplied by the worker
    data = []

    # step keeping and length for supersimple animation
    step = 0
    steps = 10

    # width of an item and the text widthin
    curWidth = 0
    fontHeight = 0

    # the index of a clicked item (<0 for none)
    selected = -1

    # called on Redraw()
    def DrawMsg(self, x1, y1, x2, y2, msg):

        # set font height and item with
        self.fontHeight = self.DrawGetFontHeight()
        self.curWidth = self.fontHeight + 2

        # set offscreen to define the whole canvas as clipping region
        #(normally this would suffice for this type of graphic since
        #we will end up drawing on the whole 'screen' anyway - but the
        #text will get a clipping region so it doesn't overlap the outlines)
        self.OffScreenOn()

        self.DrawSetPen(c4d.COLOR_BG)
        self.DrawRectangle(0, 0, x2, y2)

    # starts the redraw
    def draw(self, aData):

        self.data = aData
        self.Redraw()

