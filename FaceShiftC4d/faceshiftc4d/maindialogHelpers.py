# some classes tio help with the dialog management 

import c4d
from faceshiftc4d import ids   
from faceshiftc4d import names   

def InitValues(mainDialog): 
        
    mainDialog.faceShiftData = c4d.plugins.GetWorldPluginData(ids.PLUGINID)
    if mainDialog.faceShiftData:

        if mainDialog.faceShiftData[ids.STRING_HOST]:
            mainDialog.host = mainDialog.faceShiftData[ids.STRING_HOST]
        if mainDialog.faceShiftData[ids.LONG_PORT]:
            mainDialog.port = mainDialog.faceShiftData[ids.LONG_PORT]
        if mainDialog.faceShiftData[ids.CBOX_LIVE]:
            mainDialog.live = mainDialog.faceShiftData[ids.CBOX_LIVE]
        if mainDialog.faceShiftData[ids.CBOX_ENABLE_TARGET]:
            mainDialog.enabledUserData = mainDialog.faceShiftData[ids.CBOX_ENABLE_TARGET]
        if mainDialog.faceShiftData.GetObjectLink(ids.LINK_TARGET,c4d.documents.GetActiveDocument()) is not None:
            #print mainDialog.faceShiftData.GetObjectLink(ids.LINK_TARGET,c4d.documents.GetActiveDocument())
            pass#mainDialog.targetLink = mainDialog.faceShiftData.GetObjectLink(ids.LINK_TARGET,c4d.documents.GetActiveDocument())
        if mainDialog.faceShiftData[ids.CBOX_PLAYBACK]:
            mainDialog.playbackC4d = mainDialog.faceShiftData[ids.CBOX_PLAYBACK]
        if mainDialog.faceShiftData[ids.LONG_HEADPOSE]:
            mainDialog.headPoseMode = mainDialog.faceShiftData[ids.LONG_HEADPOSE]

    else:
        mainDialog.faceShiftData = c4d.BaseContainer()
    setUI(mainDialog)
    return True   

def setUI(mainDialog):
    mainDialog.SetString(ids.STRING_HOST, mainDialog.host)
    mainDialog.SetReal(ids.LONG_PORT, mainDialog.port, -99999999, 99999999, 1.0, c4d.FORMAT_LONG)
    mainDialog.SetBool(ids.CBOX_LIVE, mainDialog.live)
    mainDialog.SetBool(ids.CBOX_ENABLE_TARGET, mainDialog.enabledUserData)
    #print "object = "+str(mainDialog.targetLink)
    mainDialog.linkBox.SetLink(mainDialog.targetLink)
    mainDialog.SetBool(ids.CBOX_PLAYBACK, mainDialog.playbackC4d)
    mainDialog.SetBool(ids.LONG_HEADPOSE, mainDialog.headPoseMode)

    return True
    
    
def setValues(mainDialog):
    mainDialog.host=mainDialog.GetString(ids.STRING_HOST)
    mainDialog.faceShiftData.SetString(ids.STRING_HOST, mainDialog.host)
    mainDialog.port=mainDialog.GetReal(ids.LONG_PORT)
    mainDialog.faceShiftData.SetReal(ids.LONG_PORT, mainDialog.port)
    mainDialog.live=mainDialog.GetBool(ids.CBOX_LIVE)
    mainDialog.faceShiftData.SetBool(ids.CBOX_LIVE, mainDialog.live)
    mainDialog.enabledUserData=mainDialog.GetBool(ids.CBOX_ENABLE_TARGET)
    mainDialog.faceShiftData.SetBool(ids.CBOX_ENABLE_TARGET, mainDialog.enabledUserData)
    mainDialog.targetLink=mainDialog.linkBox.GetLink()
    #GetGUID()
    if mainDialog.targetLink is not None:
        print mainDialog.targetLink
        mainDialog.faceShiftData.SetLink(ids.LINK_TARGET, mainDialog.targetLink)
    #print "object 2 = "+str(mainDialog.faceShiftData.GetObjectLink(ids.LINK_TARGET,c4d.documents.GetActiveDocument()))
    #print "object 2 = "+str(mainDialog.faceShiftData[ids.LINK_TARGET])
    mainDialog.playbackC4d=mainDialog.GetBool(ids.CBOX_PLAYBACK)
    mainDialog.faceShiftData.SetBool(ids.CBOX_PLAYBACK, mainDialog.playbackC4d)
    mainDialog.headPoseMode=mainDialog.GetBool(ids.LONG_HEADPOSE)
    mainDialog.faceShiftData.SetBool(ids.LONG_HEADPOSE, mainDialog.headPoseMode)

    c4d.plugins.SetWorldPluginData(ids.PLUGINID, mainDialog.faceShiftData)  

def enableAll(mainDialog, enableBool):
    pass
