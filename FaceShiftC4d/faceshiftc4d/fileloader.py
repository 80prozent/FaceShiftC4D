import c4d
import os
import struct
from c4d import gui
#Welcome to the world of Python

class FileImporter(object):
    allTracksDic={}
    blendshapesNames=[]
    shapeTracks=[]
    newTrackROTX = None
    newTrackROTY = None
    newTrackROTZ = None
    newTrackPOSX = None
    newTrackPOSY = None
    newTrackPOSZ = None
    newContainer = None
    newkeyTime=0
    newKeyTimeOffset=0
    firstFrame=False
    def __init__(self,fileName):
        self.allTracksDic={}
        self.blendshapesNames=[]
        self.blendshapesNames.append("EyeBlink_L") 
        self.blendshapesNames.append("EyeBlink_R") 
        self.blendshapesNames.append("EyeSquint_L") 
        self.blendshapesNames.append("EyeSquint_R") 
        self.blendshapesNames.append("EyeDown_L") 
        self.blendshapesNames.append("EyeDown_R") 
        self.blendshapesNames.append("EyeIn_L") 
        self.blendshapesNames.append("EyeIn_R") 
        self.blendshapesNames.append("EyeOpen_L")
        self.blendshapesNames.append("EyeOpen_R") 
        self.blendshapesNames.append("EyeOut_L") 
        self.blendshapesNames.append("EyeOut_R") 
        self.blendshapesNames.append("EyeUp_L") 
        self.blendshapesNames.append("EyeUp_R")  
        self.blendshapesNames.append("BrowsDown_L") 
        self.blendshapesNames.append("BrowsDown_R") 
        self.blendshapesNames.append("BrowsUp_C") 
        self.blendshapesNames.append("BrowsUp_L") 
        self.blendshapesNames.append("BrowsUp_R") 
        self.blendshapesNames.append("Jaw_Fwd") 
        self.blendshapesNames.append("Jaw_L") 
        self.blendshapesNames.append("Jaw_Open")
        self.blendshapesNames.append("Jaw_Chew") 
        self.blendshapesNames.append("Jaw_R")  
        self.blendshapesNames.append("Mouth_L")  
        self.blendshapesNames.append("Mouth_R") 
        self.blendshapesNames.append("MouthFrown_L") 
        self.blendshapesNames.append("MouthFrown_R") 
        self.blendshapesNames.append("MouthSmile_L") 
        self.blendshapesNames.append("MouthSmile_R") 
        self.blendshapesNames.append("MouthDimple_L") 
        self.blendshapesNames.append("MouthDimple_R")
        self.blendshapesNames.append("LipsStretch_L") 
        self.blendshapesNames.append("LipsStretch_R")
        self.blendshapesNames.append("LipsUpperClose") 
        self.blendshapesNames.append("LipsLowerClose")
        self.blendshapesNames.append("LipsUpperUp") 
        self.blendshapesNames.append("LipsLowerDown")
        self.blendshapesNames.append("LipsUpperOpen")
        self.blendshapesNames.append("LipsLowerOpen")
        self.blendshapesNames.append("LipsFunnel")
        self.blendshapesNames.append("LipsPucker")
        self.blendshapesNames.append("ChinLowerRaise")
        self.blendshapesNames.append("ChinUpperRaise")
        self.blendshapesNames.append("Sneer")
        self.blendshapesNames.append("Puff")
        self.blendshapesNames.append("CheckSquint_L")
        self.blendshapesNames.append("CheckSquint_R")
        self.blendshapesNames.append("Eye_L_Ver")
        self.blendshapesNames.append("Eye_L_Hor")
        self.blendshapesNames.append("Eye_R_Ver")
        self.blendshapesNames.append("Eye_R_Hor")
        
        self.newContainer = c4d.BaseObject(c4d.Onull) 
        self.newContainer.SetName(fileName)  
        doc=c4d.documents.GetActiveDocument()
        if doc is not None:
            doc.InsertObject(self.newContainer) 
        if doc is None:
            return
            
        self.shapeTracks=[]   
        dataCount=0
        while dataCount<len(self.blendshapesNames):
            if dataCount<48:
                bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
                bc[c4d.DESC_NAME] = self.blendshapesNames[dataCount]
                bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_PERCENT
                bc[c4d.DESC_MIN] = 0.0
                bc[c4d.DESC_MAX] = 1.0
                bc[c4d.DESC_STEP] = 0.01
                bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER    
            if dataCount>=48:     
                bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
                bc[c4d.DESC_NAME] = self.blendshapesNames[dataCount]
                bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_REAL
                bc[c4d.DESC_MIN] = -90.0
                bc[c4d.DESC_MAX] = 90.0
                bc[c4d.DESC_STEP] = 0.01
                bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER   
            element = self.newContainer.AddUserData(bc)     #add userdata container
            newTrackShapeValue = c4d.CTrack(self.newContainer,element)
            self.newContainer.InsertTrackSorted(newTrackShapeValue)
            self.shapeTracks.append(newTrackShapeValue)
            dataCount+=1
                
        IDPOSX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
        IDPOSY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
        IDPOSZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
        IDROTX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
        IDROTY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
        IDROTZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
                 
        self.newTrackROTX = c4d.CTrack(self.newContainer,IDROTX)
        self.newTrackROTY = c4d.CTrack(self.newContainer,IDROTY)
        self.newTrackROTZ = c4d.CTrack(self.newContainer,IDROTZ)
        self.newContainer.InsertTrackSorted(self.newTrackROTX)
        self.newContainer.InsertTrackSorted(self.newTrackROTY)
        self.newContainer.InsertTrackSorted(self.newTrackROTZ)
        self.newTrackPOSX = c4d.CTrack(self.newContainer,IDPOSX)
        self.newTrackPOSY = c4d.CTrack(self.newContainer,IDPOSY)
        self.newTrackPOSZ = c4d.CTrack(self.newContainer,IDPOSZ)
        self.newContainer.InsertTrackSorted(self.newTrackPOSX)
        self.newContainer.InsertTrackSorted(self.newTrackPOSY)
        self.newContainer.InsertTrackSorted(self.newTrackPOSZ)
        
    def importFileFsb(self,datei):
        f = open(datei, 'rb')
        allstring=f.read()
        f.seek(0)
        bytecounter=0
        while bytecounter<len(allstring):
            bytecounter+=self.readBlock(f)
#print "import binary Success"   
        
    def readBlock(self,f):
        returnLength=0
        blockID= struct.unpack("H", f.read(2))
        #print "readBlock id = "+str(blockID[0])
        blockVersionNr = struct.unpack("H", f.read(2))
        blockSize = struct.unpack("I", f.read(4))
        #print "blockSize id = "+str(blockSize[0])
        returnLength+=8+blockSize[0]
        if blockID[0]==33633:
            self.readBlendShapeNames(f)
            return returnLength
        if blockID[0]==33433:
            self.readTrackingState(f)
            return returnLength
        dunpstring=f.read(blockSize[0])
        return returnLength

    def readTrackingState(self,f):
        blockCount=struct.unpack('H',  f.read(2))
        blockCounter=0
        while blockCounter<blockCount[0]:
            self.readTrackingStateBlock(f)
            blockCounter+=1
        #print blockCount[0]
 

    def readTrackingStateBlock(self,f):
        blockID= struct.unpack("H", f.read(2))
        blockVersionNr = struct.unpack("H", f.read(2))
        blockSize = struct.unpack("I", f.read(4))
        if blockID[0]==101:
            self.readFrameInformationBlock(f)
            return
        if blockID[0]==102:
            self.readHeadPositionBlock(f)
            return
        if blockID[0]==103:
            self.readBlendshapesBlock(f)
            return
        if blockID[0]==104:
            self.readEyesBlock(f)
            return
        if blockID[0]==105:
            self.readMarkersBlock(f)
            return
        dunpstring=f.read(blockSize[0])
        
    def readMarkersBlock(self,f):
        markersCount =  struct.unpack("H", f.read(2))[0]
        markerCounter=0
        while markerCounter<markersCount:
            value1=struct.unpack("f", f.read(4))[0]
            value2=struct.unpack("f", f.read(4))[0]
            value3=struct.unpack("f", f.read(4))[0]
            markerCounter+=1
            
    def readEyesBlock(self,f):
        eyeCount=0
        while eyeCount<4:
            eyeCurve=self.shapeTracks[eyeCount+48].GetCurve()
            keyEye=c4d.CKey()
            keyEye.SetTime(eyeCurve,self.newkeyTime)
            keyEye.SetValue(eyeCurve,float(struct.unpack("f", f.read(4))[0]))
            eyeCurve.InsertKey(keyEye)
            eyeCount+=1
            
    def readBlendshapesBlock(self,f):
        shapesCount =  struct.unpack("I", f.read(4))[0]
        shapesCounter=0
        while shapesCounter<shapesCount:
            shapeCurve=self.shapeTracks[shapesCounter].GetCurve()
            keyShape=c4d.CKey()
            keyShape.SetTime(shapeCurve,self.newkeyTime)
            keyShape.SetValue(shapeCurve,float(struct.unpack("f", f.read(4))[0]))
            shapeCurve.InsertKey(keyShape)
            shapesCounter+=1
            
        
    def readHeadPositionBlock(self,f):
        headMatrix = self.quaternionToMatrix(struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0])
        transX=struct.unpack('f',  f.read(4))[0]
        transY=struct.unpack('f',  f.read(4))[0]
        transZ=struct.unpack('f',  f.read(4))[0]
        doc=c4d.documents.GetActiveDocument()
        curvex=self.newTrackPOSX.GetCurve()
        keyx=c4d.CKey()
        self.newTrackPOSX.FillKey(doc,self.newContainer,keyx)
        keyx.SetTime(curvex,self.newkeyTime)
        keyx.SetValue(curvex,float(transX))
        curvex.InsertKey(keyx)
        
        curvey=self.newTrackPOSY.GetCurve()
        keyy=c4d.CKey()
        self.newTrackPOSY.FillKey(doc,self.newContainer,keyy)
        keyy.SetTime(curvey,self.newkeyTime)
        keyy.SetValue(curvex,float(transY))
        curvey.InsertKey(keyy)
                
        curvez=self.newTrackPOSZ.GetCurve()
        keyz=c4d.CKey()
        self.newTrackPOSZ.FillKey(doc,self.newContainer,keyz)
        keyz.SetTime(curvez,self.newkeyTime)
        keyz.SetValue(curvex,float(transZ*-1))
        curvez.InsertKey(keyz)
        
        self.newContainer.SetRelRot(c4d.utils.MatrixToHPB(headMatrix))
                
        curvex=self.newTrackROTX.GetCurve()
        keyx=c4d.CKey()
        self.newTrackROTX.FillKey(doc,self.newContainer,keyx)
        keyx.SetTime(curvex,self.newkeyTime)
        curvex.InsertKey(keyx)
                
        curvey=self.newTrackROTY.GetCurve()
        keyy=c4d.CKey()
        self.newTrackROTY.FillKey(doc,self.newContainer,keyy)
        keyy.SetTime(curvey,self.newkeyTime)
        curvey.InsertKey(keyy)
                
        curvez=self.newTrackROTZ.GetCurve()
        keyz=c4d.CKey()
        self.newTrackROTZ.FillKey(doc,self.newContainer,keyz)
        keyz.SetTime(curvez,self.newkeyTime)
        curvez.InsertKey(keyz)
        
    def readFrameInformationBlock(self,f):
        newKeyTimeOffset=0
        frameTime=struct.unpack('d',  f.read(8))
        if self.firstFrame==False:
            self.firstFrame=True
            self.newKeyTimeOffset=frameTime[0]
        self.newkeyTime=c4d.BaseTime((float(frameTime[0])-self.newKeyTimeOffset)/1000)
        frameSuccess=struct.unpack('B',  f.read(1))
        

    def readBlendShapeNames(self,f):
        blockCount=struct.unpack('H',  f.read(2))
        blockCnt=0
        while blockCnt<blockCount[0]:
            stringLength=struct.unpack('H',  f.read(2))
            nameCnt=0
            blendShapeName=""
            while nameCnt<stringLength[0]:
                blendShapeName+=str(struct.unpack('c',  f.read(1))[0])
                nameCnt+=1                
            #self.exchangeData.registeredBlendShapeNames[blockCnt]=blendShapeName
            blockCnt+=1
            #print blendShapeName
        
    def importFileTxt(self,datei):      
        #print datei
        f = open(datei, 'rb')
        allString=f.read()
        allFrames=allString.split("FS")
        frameCounter=1
        while frameCounter<len(allFrames):
                
            frame=allFrames[frameCounter].split("C ")
            frameHeader=frame[0].split(" ")
            shapes1=frame[1].split("E ")
            shapes=shapes1[0].split(" ")
            eyes=shapes1[1].split("M ")
            eyesList=eyes[0].split(" ")
            shapeCount=1
            newkeyTime=c4d.BaseTime(float(frameHeader[3])/1000)
            #print "frameTime = "+str(frameHeader)
            curvex=self.newTrackPOSX.GetCurve()
            keyx=c4d.CKey()
            self.newTrackPOSX.FillKey(doc,self.newContainer,keyx)
            keyx.SetTime(curvex,newkeyTime)
            keyx.SetValue(curvex,float(frameHeader[10]))
            curvex.InsertKey(keyx)
                
            curvey=self.newTrackPOSY.GetCurve()
            keyy=c4d.CKey()
            self.newTrackPOSY.FillKey(doc,self.newContainer,keyy)
            keyy.SetTime(curvey,newkeyTime)
            keyy.SetValue(curvex,float(frameHeader[11]))
            curvey.InsertKey(keyy)
                
            curvez=self.newTrackPOSZ.GetCurve()
            keyz=c4d.CKey()
            self.newTrackPOSZ.FillKey(doc,self.newContainer,keyz)
            keyz.SetTime(curvez,newkeyTime)
            keyz.SetValue(curvex,float(frameHeader[12])*-1)
            curvez.InsertKey(keyz)
                
            newMatrix = self.quaternionToMatrix(float(frameHeader[6]),float(frameHeader[7]),float(frameHeader[8]),float(frameHeader[9]))
            self.newContainer.SetRelRot(c4d.utils.MatrixToHPB(newMatrix))
        
            curvex=self.newTrackROTX.GetCurve()
            keyx=c4d.CKey()
            self.newTrackROTX.FillKey(doc,self.newContainer,keyx)
            keyx.SetTime(curvex,newkeyTime)
            curvex.InsertKey(keyx)
                
            curvey=self.newTrackROTY.GetCurve()
            keyy=c4d.CKey()
            self.newTrackROTY.FillKey(doc,self.newContainer,keyy)
            keyy.SetTime(curvey,newkeyTime)
            curvey.InsertKey(keyy)
                
            curvez=self.newTrackROTZ.GetCurve()
            keyz=c4d.CKey()
            self.newTrackROTZ.FillKey(doc,self.newContainer,keyz)
            keyz.SetTime(curvez,newkeyTime)
            curvez.InsertKey(keyz)
                
            #print "shapes[0] "+str(shapes[0])
            #print "kjnfdjkfs "+str(len(shapes))
            shapeCount=1
            shapeCount2=0
            while shapeCount<=int(shapes[0]):
                curvez=self.shapeTracks[shapeCount2].GetCurve()
                keyz=c4d.CKey()
                keyz.SetTime(curvez,newkeyTime)
                keyz.SetValue(curvex,float(shapes[shapeCount]))
                curvez.InsertKey(keyz)
                    
                #print str(shapeCount)+"  /  "+str((shapes[0]))
                #print str(shapeCount)+"  /  "+str((shapes[shapeCount]))
                shapeCount+=1
                shapeCount2+=1
            eyeCount=0
            while eyeCount<4:
                curvez=self.shapeTracks[shapeCount2].GetCurve()
                keyz=c4d.CKey()
                keyz.SetTime(curvez,newkeyTime)
                keyz.SetValue(curvex,float(eyesList[eyeCount]))
                curvez.InsertKey(keyz)
                shapeCount2+=1
                eyeCount+=1
            frameCounter+=1
        
    # This Function converts a FaceShift-Quaternion (= 4 Float-Values) into a C4D-Matrix
    def quaternionToMatrix(self,x,y,z,w):
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
        
def main():

    datei=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open FaceShift", c4d.FILESELECT_LOAD,"set")      
    if datei!=None:  
        fileName, fileExtension = os.path.splitext(datei)
        fileImporter=FileImporter(fileName)
        #print fileExtension
        if fileExtension==".txt":
            fileImporter.importFileTxt(datei)
        if fileExtension==".fsb":
            fileImporter.importFileFsb(datei)
        c4d.EventAdd()
        
   