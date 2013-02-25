"""
Cinema4D FaceShift Plugin 2013 by 80prozent[a]differentdesign.de

enjoy


"""


import os
import sys
import c4d

folder = os.path.dirname(__file__)
if folder not in sys.path:
    sys.path.insert(0, folder)
    
import c4d
    
from faceshiftc4d import ids
from faceshiftc4d import cmddata
from faceshiftc4d import maindialog
from faceshiftc4d import maindialogCreator
from faceshiftc4d import faceshiftparser

def PluginMessage(id, data):
    if id==c4d.C4DPL_ENDPROGRAM or id==c4d.C4DPL_ENDACTIVITY or id==c4d.C4DPL_RELOADPYTHONPLUGINS:
        if faceshiftparser.sock is not None:
            faceshiftparser.sock.close()
        if maindialog.workerThread is not None:
            maindialog.workerThread.End(False)   
            maindialog.workerThread=None
        return True
    return False
	
maindialog.__res__ = __res__
maindialogCreator.__res__ = __res__

if __name__ == "__main__":

    iconID = 1390382
    icon2 = c4d.bitmaps.BaseBitmap()
    icon2.InitWith(os.path.join(os.path.dirname(__file__), "res", "exporterPic.png"))
    c4d.gui.RegisterIcon(iconID,icon2)

    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(os.path.dirname(__file__), "res", "icon.tif"))
    
    title = c4d.plugins.GeLoadString(ids.STR_TITLE)
        
    c4d.plugins.RegisterCommandPlugin(ids.PLUGINID, title, 0, icon, title, cmddata.CMDData())