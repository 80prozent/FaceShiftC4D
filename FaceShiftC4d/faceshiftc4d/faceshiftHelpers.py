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
    testobj=c4d.BaseObject(c4d.Onull)
    while frameCnt<len(exchangeData.recordetFrames):
        curFrame=exchangeData.recordetFrames[frameCnt]
        frameCnt+=1
        frameTime=c4d.BaseTime(float(float(exchangeData.startRecTimeC4D)+float(curFrame.frameTime))/1000)

        
        curve=matrixTracks[0].GetCurve()
        key=c4d.CKey()
        key.SetTime(curve,frameTime)
        key.SetValue(curve,float(curFrame.headPosition.x))
        curve.InsertKey(key)
        
        curve=matrixTracks[1].GetCurve()
        key=c4d.CKey()
        key.SetTime(curve,frameTime)
        key.SetValue(curve,float(curFrame.headPosition.y))
        curve.InsertKey(key)
        
        curve=matrixTracks[2].GetCurve()
        key=c4d.CKey()
        key.SetTime(curve,frameTime)
        key.SetValue(curve,float(curFrame.headPosition.z))
        curve.InsertKey(key)
        
        testobj.SetMl(curFrame.headRotation)
        rotationVec=testobj.GetRelRot()
              
        curve=matrixTracks[3].GetCurve()
        key=c4d.CKey()
        key.SetValue(curve,float(rotationVec.x))
        key.SetTime(curve,frameTime)
        curve.InsertKey(key)
                
        curve=matrixTracks[4].GetCurve()
        key=c4d.CKey()
        key.SetValue(curve,float(rotationVec.y))
        key.SetTime(curve,frameTime)
        curve.InsertKey(key)
                
        curve=matrixTracks[5].GetCurve()
        key=c4d.CKey()
        key.SetValue(curve,float(rotationVec.z))
        key.SetTime(curve,frameTime)
        curve.InsertKey(key)
        
        shapesCounter=0
        while shapesCounter<len(curFrame.blendShapeValues):
            if shapesCounter>len(shapetracks):
                break
            if shapesCounter<len(shapetracks):
                shapeCurve=shapetracks[shapesCounter].GetCurve()
                keyShape=c4d.CKey()
                keyShape.SetTime(shapeCurve,frameTime)
                keyShape.SetValue(shapeCurve,curFrame.blendShapeValues[shapesCounter])
                shapeCurve.InsertKey(keyShape)
            shapesCounter+=1
            
        eyeGazeCounter=48
        eyeGazeCounter2=0
        while eyeGazeCounter2<len(curFrame.eyeGazeValues):
            if eyeGazeCounter>len(shapetracks):
                break
            if eyeGazeCounter<len(shapetracks):
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
        if userDataCount<=49 and userDataCount>1:
            #print "bc[c4d.DESC_UNIT]  = "+str(targetOBJ[id])+"c4d.DESC_UNIT_PERCENT  /  =  "+str(c4d.DESC_UNIT_PERCENT)            
            if bc[c4d.DESC_UNIT] == c4d.DESC_UNIT_PERCENT:
                #print "Could Set Target Object"
                mainDialog.blendShapeTargets.append(id)
            if bc[c4d.DESC_UNIT] != c4d.DESC_UNIT_PERCENT:
                mainDialog.blendShapeTargets=oldBlends
                mainDialog.eyeGazeTargets=oldEyes
                print "Could not set new Target Object"
                return False
        if userDataCount>49:
            if bc[c4d.DESC_UNIT] == c4d.DESC_UNIT_REAL:
                mainDialog.eyeGazeTargets.append(id)
            if bc[c4d.DESC_UNIT] != c4d.DESC_UNIT_REAL:
                mainDialog.blendShapeTargets=oldBlends
                mainDialog.eyeGazeTargets=oldEyes  
                return False   
        if userDataCount>53: 
            break
    if userDataCount==0:
        createNewUserData(mainDialog,targetOBJ)
        
    mainDialog.targetLink=targetOBJ
    mainDialog.linkBox.SetLink(mainDialog.targetLink)
    return True
        
        
def createNewTarget(mainDialog):    
    newContainer = c4d.BaseObject(c4d.Onull) 
    newContainer.SetName("FaceShiftData")  
    doc=c4d.documents.GetActiveDocument()
    if doc is not None:
        doc.InsertObject(newContainer) 
    createNewUserData(mainDialog,newContainer)
    mainDialog.targetLink=newContainer
    mainDialog.linkBox.SetLink(mainDialog.targetLink)
    c4d.EventAdd()  
        
def createNewUserData(mainDialog,newContainer):

    newXpressoTag=newContainer.MakeTag(1001149)
    nodemaster = newXpressoTag.GetNodeMaster() #Generates xpresso nodes
    controllerNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=20, y=50) #create condition node and place in X,Y coord
    controllerNode.GetOperatorContainer()
    mainNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=300, y=0) #create condition node and place in X,Y coord
    mainNode.GetOperatorContainer()
    #nodeporst=node1.GetInPorts()
    #node2 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=100, y=200) #create Object node and place in X,Y coord
    #node2.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_POSITION) #add a position input port to the object node
    #node1out=node2.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_POSITION) #add a position output port to the object node
    
    blendShapeNames=names.blendShapeNames
    shapeCount=0
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK) #create default container
    bc[c4d.DESC_NAME] = "ControllerObject"
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_LINKBOX  
    element = newContainer.AddUserData(bc)     #add userdata container 
    newContainer[element]=newContainer
    newPortDataOut=controllerNode.AddPort(c4d.GV_PORT_OUTPUT, element)
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
        newPort=mainNode.AddPort(c4d.GV_PORT_OUTPUT, element) #add a position output port to the object node
        #print (element)
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
        newPort=mainNode.AddPort(c4d.GV_PORT_OUTPUT, element) #add a position output port to the object node
        mainDialog.eyeGazeTargets.append(element)
        eyeGazeCount+=1
    
    c4d.modules.graphview.RedrawMaster(nodemaster)
    nodemaster.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()  

# This Function converts a FaceShift-Quaternion (= 4 Float-Values) into a C4D-Matrix
def quaternionToMatrix(x,y,z,w):
    xx      = x * x;
    xy      = x * y;
    xz      = x * z;
    xw      = x * w;
    yy      = y * y;
    yz      = y * z;
    yw      = y * w;
    zz      = z * z;
    zw      = z * w;
    vec1=c4d.Vector()
    vec2=c4d.Vector()
    vec3=c4d.Vector()
    vecOff=c4d.Vector()
    vec1.x  = 1 - 2 * ( yy + zz );
    vec1.y  =     2 * ( xy - zw );
    vec1.z  =     2 * ( xz + yw );
    vec2.x  =     2 * ( xy + zw );
    vec2.y  = 1 - 2 * ( xx + zz );
    vec2.z  =     2 * ( yz - xw );
    vec3.x  =     2 * ( xz - yw );
    vec3.y  =     2 * ( yz + xw );
    vec3.z = 1 - 2 * ( xx + yy );
    newMatrix=c4d.Matrix(vecOff,vec1,vec2,vec3)        
    return newMatrix