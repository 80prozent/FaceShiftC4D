import c4d
from c4d import documents
import os
from faceshiftc4d import ids
from faceshiftc4d import canvas

from xml.dom import minidom
import xml.dom.minidom as dom

class RecordetFrame(object):
    frameTime=0
    headRotation=None
    headPosition=None
    blendShapeValues=[]
    eyeGazeValues=[]
    markerPositions=[]
    frameSuccess=0
    def __init__(self, _frameTime,frameSuccess):
        self.frameTime=_frameTime
        self.headRotation=c4d.Matrix()
        self.headPosition=c4d.Vector()
        self.blendShapeValues=[]
        self.eyeGazeValues=[]
        self.markerPositions=[]
        self.frameSuccess=frameSuccess
        
class ExchangeData(object): 
    recordetFrames=[]
    startRecTimeC4D=0
    startRecTimeFS=-1
    doneRecTime=0
    isRecording=False
    curC4dTime=0
    
    isNew=True
    
    calcObj=None
    connected=False 
    frameSuccess=0 
    remoteMessage=0 
    rotationVector=None
    positionVector=None
    hasChanged=0 
    frameTime=0
    headMatrix=None
    blendShapes=[]
    eyesTarget=[]
    markers=[]
    host="127.0.0.1"
    port=33433
    registeredHeadTargetsRotation=[] 
    registeredHeadTargetsTranslation=[] 
    registeredMarkerTargets=[] 
    registeredBlendShapeTargets=[]
    registeredBlendShapeNames=[] 
    connected=0
    def __init__(self):  
        self.rotationVector=c4d.Vector()
        self.positionVector=c4d.Vector()
        self.frameSuccess=0 
        self.frameTime=0
        self.calcObj=c4d.BaseObject(c4d.Onull) 
        self.headMatrix=c4d.Matrix()
        self.headTarget=[0,1,2,3,4,5,6]
        self.blendShapes=[]
        self.eyeGazeValues=[]
        self.registeredBlendShapeNames=[] 
        self.connected=0
    
        shapeCnt=0
        while shapeCnt<48:
            shapeCnt+=1
            self.blendShapes.append(0.0)
            self.registeredBlendShapeNames.append("")
        self.eyesTarget=[0,1,2,3]
        self.markers=[]  
		
    def registerTargets(self):
        doc=documents.GetActiveDocument()
        allObjects=doc.GetObjects()
        self.registeredHeadTargetsRotation=[] 
        self.registeredHeadTargetsTranslation=[] 
        self.registeredMarkerTargets=[] 
        self.registeredBlendShapeTargets=[] 
        for i in allObjects:
            self.testObjectForRegister(i)

    def mapMorphTagTargets(self,curObj,mode):
        print "map Morphtag ,mode = "+str(mode)
        registertBlendShapesDIC={}
        if curObj.GetTag(c4d.Tposemorph):#	reset morphtags
            all_tags=curObj.GetTags()#get all tags applied to object
            for morphtag in all_tags:#do for each tag:
                if morphtag.GetType()==c4d.Tposemorph:#do if the tag is a morphtag
                    morphCount=0
                    while morphCount<morphtag.GetMorphCount():
                        registertBlendShapesDIC[str(morphtag.GetMorph(morphCount).GetName())]=morphtag.GetMorph(morphCount);
                        morphCount+=1
                    morphCount=0
                    foundMorphes=0
                    newMorphConection=[]
                    while morphCount<len(self.registeredBlendShapeNames):
                        newMorphconnect=registertBlendShapesDIC[self.registeredBlendShapeNames[morphCount]]
                        newMorphConection.append(newMorphconnect)
                        morphCount+=1
                    print "morphslength = "+str(len(newMorphConection))
                    self.registeredBlendShapeTargets.append(newMorphConection)
        
    def mapUserDataTargets(self,curObj,mode):
        print "map UserData ,mode = "+str(mode)
        newBlendShapeUSERDATA=[]
        newBlendShapeUSERDATA.append(curObj)
        counter=0
        for id, bc in curObj.GetUserDataContainer():
            print id, bc[c4d.DESC_NAME]
            #counter+=1
            
        newBlendShapeUSERDATA.append(counter+1)
        dataCount=0
        #while dataCount<len(self.registeredBlendShapeNames):
         #   bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
          #  bc[c4d.DESC_NAME] = self.registeredBlendShapeNames[dataCount] 
           # element = curObj.AddUserData(bc)     #add userdata container
            #dataCount+=1
        self.registeredBlendShapeTargets.append(newBlendShapeUSERDATA) 
        c4d.EventAdd()
        
    def testObjectForRegister(self,curObj):
    
        if curObj.GetTag(1028937):
            if curObj.GetTag(1028937).GetData().GetBool(1023)==True:
                self.registeredHeadTargetsRotation.append(curObj)
            if curObj.GetTag(1028937).GetData().GetBool(1022)==True:
                self.registeredHeadTargetsTranslation.append(curObj)
            if curObj.GetTag(1028937).GetData().GetLong(1014)>0:
                pass#self.mapMorphTagTargets(curObj,curObj.GetTag(1028937).GetData().GetLong(1014))
            if curObj.GetTag(1028937).GetData().GetLong(1021)>0:
                self.mapUserDataTargets(curObj,curObj.GetTag(1028937).GetData().GetLong(1021))
        if len(curObj.GetChildren())>0:
            for i in curObj.GetChildren():
                self.testObjectForRegister(i)
				