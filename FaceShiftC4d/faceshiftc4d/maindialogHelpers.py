# some classes tio help with the dialog management 

import c4d
from faceshiftc4d import ids   
from faceshiftc4d import names   

def addRecording(mainDialog,exchangeData):
    if mainDialog.targetLink is None:
        createNewTarget(mainDialog)
    
    shapetracks=[]
    userDataCount=0
    for id, bc in mainDialog.targetLink.GetUserDataContainer():
        userDataCount+=1
        if userDataCount<=52:
            shapeTrack=mainDialog.targetLink.FindCTrack(id)
            if shapeTrack is None:
                shapeTrack = c4d.CTrack(mainDialog.targetLink, id)
                mainDialog.targetLink.InsertTrackSorted(shapeTrack)
            shapetracks.append(shapeTrack)
    
    IDPOSX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
    IDPOSY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
    IDPOSZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
    IDROTX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
    IDROTY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
    IDROTZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
    
    trackIDS=[IDPOSX,IDPOSY,IDPOSZ,IDROTX,IDROTY,IDROTZ]
    matrixTracks=[]
    
    trackCount=0
    while trackCount<len(trackIDS):
        newTrack=mainDialog.targetLink.FindCTrack(trackIDS[trackCount])
        if newTrack is None:
            newTrack = c4d.CTrack(mainDialog.targetLink, trackIDS[trackCount])
            mainDialog.targetLink.InsertTrackSorted(newTrack)
        matrixTracks.append(newTrack)
        trackCount+=1
    print ("frames to do")+str(len(exchangeData.recordetFrames))
    frameCnt=0
    doc=c4d.documents.GetActiveDocument()
    while frameCnt<len(exchangeData.recordetFrames):
        curFrame=exchangeData.recordetFrames[frameCnt]
        frameCnt+=1
        frameTime=c4d.BaseTime(float(float(exchangeData.startRecTimeC4D)+float(curFrame.frameTime))/1000)

        
        curve=matrixTracks[0].GetCurve()
        key=c4d.CKey()
        matrixTracks[0].FillKey(doc,mainDialog.targetLink,key)
        key.SetTime(curve,frameTime)
        key.SetValue(curve,float(curFrame.headPosition.x))
        curve.InsertKey(key)
        
        curve=matrixTracks[1].GetCurve()
        key=c4d.CKey()
        matrixTracks[1].FillKey(doc,mainDialog.targetLink,key)
        key.SetTime(curve,frameTime)
        key.SetValue(curve,float(curFrame.headPosition.y))
        curve.InsertKey(key)
        
        curve=matrixTracks[2].GetCurve()
        key=c4d.CKey()
        matrixTracks[2].FillKey(doc,mainDialog.targetLink,key)
        key.SetTime(curve,frameTime)
        key.SetValue(curve,float(curFrame.headPosition.z))
        curve.InsertKey(key)
               
        mainDialog.targetLink.SetRelRot(curFrame.headRotation)
              
                
        curve=matrixTracks[3].GetCurve()
        key=c4d.CKey()
        matrixTracks[3].FillKey(doc,mainDialog.targetLink,key)
        key.SetTime(curve,frameTime)
        curve.InsertKey(key)
                
        curve=matrixTracks[4].GetCurve()
        key=c4d.CKey()
        matrixTracks[4].FillKey(doc,mainDialog.targetLink,key)
        key.SetTime(curve,frameTime)
        curve.InsertKey(key)
                
        curve=matrixTracks[5].GetCurve()
        key=c4d.CKey()
        matrixTracks[5].FillKey(doc,mainDialog.targetLink,key)
        key.SetTime(curve,frameTime)
        curve.InsertKey(key)
        
        shapesCounter=0
        while shapesCounter<len(curFrame.blendShapeValues):
            shapeCurve=shapetracks[shapesCounter].GetCurve()
            keyShape=c4d.CKey()
            keyShape.SetTime(shapeCurve,frameTime)
            keyShape.SetValue(shapeCurve,curFrame.blendShapeValues[shapesCounter])
            shapeCurve.InsertKey(keyShape)
            shapesCounter+=1
            
        eyeGazeCounter=48
        eyeGazeCounter2=0
        while eyeGazeCounter2<len(curFrame.eyeGazeValues):
            shapeCurve=shapetracks[eyeGazeCounter].GetCurve()
            keyShape=c4d.CKey()
            keyShape.SetTime(shapeCurve,frameTime)
            keyShape.SetValue(shapeCurve,curFrame.eyeGazeValues[eyeGazeCounter2])
            shapeCurve.InsertKey(keyShape)
            eyeGazeCounter2+=1
            eyeGazeCounter+=1
        
    

def registerNewtarget(mainDialog,targetOBJ):    
    userDataCount=0
    oldBlends=mainDialog.blendShapeTargets
    oldEyes=mainDialog.eyeGazeTargets
    mainDialog.blendShapeTargets=[]
    mainDialog.eyeGazeTargets=[]
    for id, bc in targetOBJ.GetUserDataContainer():
        userDataCount+=1
        if userDataCount<=48:
            print "bc[c4d.DESC_UNIT]  = "+str(targetOBJ[id])+"c4d.DESC_UNIT_PERCENT  /  =  "+str(c4d.DESC_UNIT_PERCENT)
            
            
            if bc[c4d.DESC_UNIT] == c4d.DESC_UNIT_PERCENT:
                print "Could Set Target Object"
                mainDialog.blendShapeTargets.append(id)
            if bc[c4d.DESC_UNIT] != c4d.DESC_UNIT_PERCENT:
                mainDialog.blendShapeTargets=oldBlends
                mainDialog.eyeGazeTargets=oldEyes
                print "Could not set new Target Object"
                return False
        if userDataCount>48:
            if bc[c4d.DESC_UNIT] == c4d.DESC_UNIT_REAL:
                mainDialog.eyeGazeTargets.append(id)
            if bc[c4d.DESC_UNIT] != c4d.DESC_UNIT_REAL:
                mainDialog.blendShapeTargets=oldBlends
                mainDialog.eyeGazeTargets=oldEyes  
                return False   
        if userDataCount>52: 
            break
        
        
    mainDialog.targetLink=targetOBJ
    mainDialog.linkBox.SetLink(mainDialog.targetLink)
    return True
        
        
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
        print (element)
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
