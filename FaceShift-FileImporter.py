import c4d
import os
import struct
from c4d import gui
#Welcome to the world of Python


def main():
    datei=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open FaceShift", c4d.FILESELECT_LOAD,"set")  
    
    if datei!=None:  
        fileName, fileExtension = os.path.splitext(datei)
        print fileExtension
        if fileExtension==".txt":
            importFileTxt(datei)
        if fileExtension==".fsb":
            importFileFsb(datei)
        
def importFileFsb(datei):
    f = open(datei, 'rb')
    allstring=f.read()
    f.seek(0)
    bytecounter=0
    while bytecounter<len(allstring):
        bytecounter+=readBlock(f)
    print "import Success"
        
def readBlock(f):
    returnLength=0
    blockID= struct.unpack("H", f.read(2))
    print "readBlock id = "+str(blockID[0])
    blockVersionNr = struct.unpack("H", f.read(2))
    blockSize = struct.unpack("I", f.read(4))
    print "blockSize id = "+str(blockSize[0])
    returnLength+=8+blockSize[0]
    if blockID[0]==33633:
        readBlendShapeNames(f)
        return returnLength
    if blockID[0]==33433:
        readTrackingState(f)
        return returnLength
    dunpstring=f.read(blockSize[0])
    return returnLength

def readTrackingState(f):
    blockCount=struct.unpack('H',  f.read(2))
    blockCounter=0
    while blockCounter<blockCount[0]:
        readTrackingStateBlock(f)
        blockCounter+=1
    print blockCount[0]

def readTrackingStateBlock(f):
    blockID= struct.unpack("H", f.read(2))
    blockVersionNr = struct.unpack("H", f.read(2))
    blockSize = struct.unpack("I", f.read(4))
    if blockID[0]==101:
        readFrameInformationBlock(f)
        return
    if blockID[0]==102:
        readHeadPositionBlock(f)
        return
    if blockID[0]==103:
        readBlendshapesBlock(f)
        return
    if blockID[0]==104:
        readEyesBlock(f)
        return
    if blockID[0]==105:
        readMarkersBlock(f)
        return
    dunpstring=f.read(blockSize[0])
    
def readMarkersBlock(f):
    markersCount =  struct.unpack("H", f.read(2))[0]
    markerCounter=0
    while markerCounter<markersCount:
        value1=struct.unpack("f", f.read(4))[0]
        value2=struct.unpack("f", f.read(4))[0]
        value3=struct.unpack("f", f.read(4))[0]
        markerCounter+=1
        
def readEyesBlock(f):
    shapesCount1=struct.unpack("f", f.read(4))
    shapesCount2=struct.unpack("f", f.read(4))
    shapesCount3=struct.unpack("f", f.read(4))
    shapesCount4=struct.unpack("f", f.read(4))
        
def readBlendshapesBlock(f):
    shapesCount =  struct.unpack("I", f.read(4))[0]
    shapesCounter=0
    while shapesCounter<shapesCount:
        value=struct.unpack("f", f.read(4))[0]
        shapesCounter+=1
        
    
def readHeadPositionBlock(f):
    headMatrix = quaternionToMatrix(struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0])
    headMatrix.off.x=struct.unpack('f',  f.read(4))[0]
    headMatrix.off.y=struct.unpack('f',  f.read(4))[0]
    headMatrix.off.z=struct.unpack('f',  f.read(4))[0]
    
def readFrameInformationBlock(f):
    frameTime=struct.unpack('d',  f.read(8))
    frameSuccess=struct.unpack('B',  f.read(1))
    

def readBlendShapeNames(f):
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
        print blendShapeName
    
def importFileTxt(datei):
    if True:
        blendshapesNames=[]
        blendshapesNames.append("EyeBlink_L") 
        blendshapesNames.append("EyeBlink_R") 
        blendshapesNames.append("EyeSquint_L") 
        blendshapesNames.append("EyeSquint_R") 
        blendshapesNames.append("EyeDown_L") 
        blendshapesNames.append("EyeDown_R") 
        blendshapesNames.append("EyeIn_L") 
        blendshapesNames.append("EyeIn_R") 
        blendshapesNames.append("EyeOpen_L")
        blendshapesNames.append("EyeOpen_R") 
        blendshapesNames.append("EyeOut_L") 
        blendshapesNames.append("EyeOut_R") 
        blendshapesNames.append("EyeUp_L") 
        blendshapesNames.append("EyeUp_R")  
        blendshapesNames.append("BrowsDown_L") 
        blendshapesNames.append("BrowsDown_R") 
        blendshapesNames.append("BrowsUp_C") 
        blendshapesNames.append("BrowsUp_L") 
        blendshapesNames.append("BrowsUp_R") 
        blendshapesNames.append("Jaw_Fwd") 
        blendshapesNames.append("Jaw_L") 
        blendshapesNames.append("Jaw_Open")
        blendshapesNames.append("Jaw_Chew") 
        blendshapesNames.append("Jaw_R")  
        blendshapesNames.append("Mouth_L")  
        blendshapesNames.append("Mouth_R") 
        blendshapesNames.append("MouthFrown_L") 
        blendshapesNames.append("MouthFrown_R") 
        blendshapesNames.append("MouthSmile_L") 
        blendshapesNames.append("MouthSmile_R") 
        blendshapesNames.append("MouthDimple_L") 
        blendshapesNames.append("MouthDimple_R")
        blendshapesNames.append("LipsStretch_L") 
        blendshapesNames.append("LipsStretch_R")
        blendshapesNames.append("LipsUpperClose") 
        blendshapesNames.append("LipsLowerClose")
        blendshapesNames.append("LipsUpperUp") 
        blendshapesNames.append("LipsLowerDown")
        blendshapesNames.append("LipsUpperOpen")
        blendshapesNames.append("LipsLowerOpen")
        blendshapesNames.append("LipsFunnel")
        blendshapesNames.append("LipsPucker")
        blendshapesNames.append("ChinLowerRaise")
        blendshapesNames.append("ChinUpperRaise")
        blendshapesNames.append("Sneer")
        blendshapesNames.append("Puff")
        blendshapesNames.append("CheckSquint_L")
        blendshapesNames.append("CheckSquint_R")
        blendshapesNames.append("Eye_L_Ver")
        blendshapesNames.append("Eye_L_Hor")
        blendshapesNames.append("Eye_R_Ver")
        blendshapesNames.append("Eye_R_Hor")
        
        print str(len(blendshapesNames))
        newContainer = c4d.BaseObject(c4d.Onull) 
        newContainer.SetName("testDatei")  
        doc=c4d.documents.GetActiveDocument()
        doc.InsertObject(newContainer) 
        
        shapeTracks=[]   
        dataCount=0
        while dataCount<len(blendshapesNames):
            if dataCount<48:
                bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
                bc[c4d.DESC_NAME] = blendshapesNames[dataCount]
                bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_PERCENT
                bc[c4d.DESC_MIN] = 0.0
                bc[c4d.DESC_MAX] = 1.0
                bc[c4d.DESC_STEP] = 0.01
                bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER    
            if dataCount>=48:     
                bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL) #create default container
                bc[c4d.DESC_NAME] = blendshapesNames[dataCount]
                bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_REAL
                bc[c4d.DESC_MIN] = -90.0
                bc[c4d.DESC_MAX] = 90.0
                bc[c4d.DESC_STEP] = 0.01
                bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER   
            element = newContainer.AddUserData(bc)     #add userdata container
            newTrackShapeValue = c4d.CTrack(newContainer,element)
            newContainer.InsertTrackSorted(newTrackShapeValue)
            shapeTracks.append(newTrackShapeValue)
            dataCount+=1
            
        IDPOSX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
        IDPOSY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
        IDPOSZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
        IDROTX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
        IDROTY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
        IDROTZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
             
        newTrackROTX = c4d.CTrack(newContainer,IDROTX)
        newTrackROTY = c4d.CTrack(newContainer,IDROTY)
        newTrackROTZ = c4d.CTrack(newContainer,IDROTZ)
        newContainer.InsertTrackSorted(newTrackROTX)
        newContainer.InsertTrackSorted(newTrackROTY)
        newContainer.InsertTrackSorted(newTrackROTZ)
        newTrackPOSX = c4d.CTrack(newContainer,IDPOSX)
        newTrackPOSY = c4d.CTrack(newContainer,IDPOSY)
        newTrackPOSZ = c4d.CTrack(newContainer,IDPOSZ)
        newContainer.InsertTrackSorted(newTrackPOSX)
        newContainer.InsertTrackSorted(newTrackPOSY)
        newContainer.InsertTrackSorted(newTrackPOSZ)
           
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
            curvex=newTrackPOSX.GetCurve()
            keyx=c4d.CKey()
            newTrackPOSX.FillKey(doc,newContainer,keyx)
            keyx.SetTime(curvex,newkeyTime)
            keyx.SetValue(curvex,float(frameHeader[10]))
            curvex.InsertKey(keyx)
            
            curvey=newTrackPOSY.GetCurve()
            keyy=c4d.CKey()
            newTrackPOSY.FillKey(doc,newContainer,keyy)
            keyy.SetTime(curvey,newkeyTime)
            keyy.SetValue(curvex,float(frameHeader[11]))
            curvey.InsertKey(keyy)
            
            curvez=newTrackPOSZ.GetCurve()
            keyz=c4d.CKey()
            newTrackPOSZ.FillKey(doc,newContainer,keyz)
            keyz.SetTime(curvez,newkeyTime)
            keyz.SetValue(curvex,float(frameHeader[12])*-1)
            curvez.InsertKey(keyz)
            
            newMatrix = quaternionToMatrix(float(frameHeader[6]),float(frameHeader[7]),float(frameHeader[8]),float(frameHeader[9]))
            newContainer.SetRelRot(c4d.utils.MatrixToHPB(newMatrix))
            
            curvex=newTrackROTX.GetCurve()
            keyx=c4d.CKey()
            newTrackROTX.FillKey(doc,newContainer,keyx)
            keyx.SetTime(curvex,newkeyTime)
            curvex.InsertKey(keyx)
            
            curvey=newTrackROTY.GetCurve()
            keyy=c4d.CKey()
            newTrackROTY.FillKey(doc,newContainer,keyy)
            keyy.SetTime(curvey,newkeyTime)
            curvey.InsertKey(keyy)
            
            curvez=newTrackROTZ.GetCurve()
            keyz=c4d.CKey()
            newTrackROTZ.FillKey(doc,newContainer,keyz)
            keyz.SetTime(curvez,newkeyTime)
            curvez.InsertKey(keyz)
            
            #print "shapes[0] "+str(shapes[0])
            #print "kjnfdjkfs "+str(len(shapes))
            shapeCount=1
            shapeCount2=0
            while shapeCount<=int(shapes[0]):
                curvez=shapeTracks[shapeCount2].GetCurve()
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
                curvez=shapeTracks[shapeCount2].GetCurve()
                keyz=c4d.CKey()
                keyz.SetTime(curvez,newkeyTime)
                keyz.SetValue(curvex,float(eyesList[eyeCount]))
                curvez.InsertKey(keyz)
                shapeCount2+=1
                eyeCount+=1
            frameCounter+=1
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

if __name__=='__main__':
    main()