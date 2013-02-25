# some classes tio help with the dialog management 

import c4d
from faceshiftc4d import ids   
from faceshiftc4d import names   

def createNewTarget(mainDialog):    
    newContainer = c4d.BaseObject(c4d.Onull) 
    newContainer.SetName("FaceShiftData")  
    doc=c4d.documents.GetActiveDocument()
    if doc is not None:
        doc.InsertObject(newContainer) 
    blendShapeNames=names.blendShapeNames
    shapeCount=0
    mainDialog.blendShapeTargets=[]
    while shapeCount<len(blendShapeNames):
        bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
        bc[c4d.DESC_NAME] = blendShapeNames[shapeCount]
        bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_PERCENT
        bc[c4d.DESC_MIN] = 0.0
        bc[c4d.DESC_MAX] = 1.0
        bc[c4d.DESC_STEP] = 0.01
        bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER   
        element = newContainer.AddUserData(bc)     #add userdata container 
        mainDialog.blendShapeTargets.append(element)
        shapeCount+=1
    eyeGazeNames=names.eyeGazeNames
    eyeGazeCount=0
    mainDialog.eyeGazeTargets=[]
    while eyeGazeCount<len(eyeGazeNames):
        bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
        bc[c4d.DESC_NAME] = eyeGazeNames[eyeGazeCount]
        bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_REAL
        bc[c4d.DESC_MIN] = -90.0
        bc[c4d.DESC_MAX] = 90.0
        bc[c4d.DESC_STEP] = 0.01
        bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER   
        element = newContainer.AddUserData(bc)     #add userdata container 
        mainDialog.eyeGazeTargets.append(element)
        eyeGazeCount+=1
    mainDialog.targetLink=newContainer
    mainDialog.linkBox.SetLink(mainDialog.targetLink)
    c4d.EventAdd()  

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
        if mainDialog.faceShiftData[ids.LINK_TARGET]:
            mainDialog.targetLink = mainDialog.faceShiftData[ids.LINK_TARGET]
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
    #mainDialog.faceShiftData.SetBool(ids.LINK_TARGET, mainDialog.targetLink)
    mainDialog.playbackC4d=mainDialog.GetBool(ids.CBOX_PLAYBACK)
    mainDialog.faceShiftData.SetBool(ids.CBOX_PLAYBACK, mainDialog.playbackC4d)
    mainDialog.headPoseMode=mainDialog.GetBool(ids.LONG_HEADPOSE)
    mainDialog.faceShiftData.SetBool(ids.LONG_HEADPOSE, mainDialog.headPoseMode)

    c4d.plugins.SetWorldPluginData(ids.PLUGINID, mainDialog.faceShiftData)  

def enableAll(mainDialog, enableBool):
    pass
