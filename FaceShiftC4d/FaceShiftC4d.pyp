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
        
from faceshiftc4d import ids
from faceshiftc4d import cmddata
from faceshiftc4d import maindialog
from faceshiftc4d import maindialogCreator
from faceshiftc4d import canvasShapes

# whenever the plugin recieves a message that suggest all threads should close, we close down all Threads
def PluginMessage(id, data):
    if id==c4d.C4DPL_ENDPROGRAM or id==c4d.C4DPL_ENDACTIVITY or id==c4d.C4DPL_RELOADPYTHONPLUGINS:
        c4d.StopAllThreads()
        return True
    return False

# all modules using the c4d-res system to retrieve text in correct language, needs to init the '__res__' here
maindialog.__res__ = __res__
maindialogCreator.__res__ = __res__
canvasShapes.__res__ = __res__

# registers the plugin. initiates a instance of 'cmddata.CMDData()' 
if __name__ == "__main__":

    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(os.path.dirname(__file__), "res", "icon.tif"))
    
    title = c4d.plugins.GeLoadString(ids.STR_TITLE)
        
    c4d.plugins.RegisterCommandPlugin(ids.PLUGINID, title, 0, icon, title, cmddata.CMDData())