import c4d
import os
import struct
from c4d import gui
from faceshiftc4d import ids
from faceshiftc4d import faceShiftData
from faceshiftc4d import faceshiftHelpers

#Welcome to the world of Python
# starts the FileImporter
def main(exchangeData):
    datei=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open FaceShift", c4d.FILESELECT_LOAD,"set")      
    if datei!=None:  
        fileName, fileExtension = os.path.splitext(datei)
        fileImporter=FileImporter(fileName,exchangeData)
        if fileExtension==".txt":
            fileImporter.importFileTxt(datei)
        if fileExtension==".fsb":
            fileImporter.importFileFsb(datei)
        c4d.EventAdd()
        return fileImporter.exchangeData
    return None
    
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
    exchangeData=None
    def __init__(self,fileName,exchangeData):
        self.exchangeData=exchangeData
        self.exchangeData.recordetFrames=[]
                  
      
        
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
        if int(self.newFrame.frameSuccess)==1:
            self.exchangeData.recordetFrames.append(self.newFrame)
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
        self.newFrame.eyeGazeValues=[]
        while eyeCount<4:
            value=float(struct.unpack("f", f.read(4))[0])
            self.newFrame.eyeGazeValues.append(value)
            eyeCount+=1
            
    def readBlendshapesBlock(self,f):
        shapesCount =  struct.unpack("I", f.read(4))[0]
        shapesCounter=0
        self.newFrame.blendShapeValues=[]
        while shapesCounter<shapesCount:
            value=float(struct.unpack("f", f.read(4))[0])
            self.newFrame.blendShapeValues.append(value)
            shapesCounter+=1            
        
    def readHeadPositionBlock(self,f):
        headMatrix = faceshiftHelpers.quaternionToMatrix(struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0],struct.unpack('f',  f.read(4))[0]*-1,struct.unpack('f',  f.read(4))[0])
        transX=struct.unpack('f',  f.read(4))[0]
        transY=struct.unpack('f',  f.read(4))[0]
        transZ=struct.unpack('f',  f.read(4))[0]
        self.newFrame.headRotation=headMatrix
        self.newFrame.headPosition=c4d.Vector(transX,transY,transZ*-1)
                
    def readFrameInformationBlock(self,f):
        newKeyTimeOffset=0
        frameTime=struct.unpack('d',  f.read(8))[0]
        if self.firstFrame==False:
            self.firstFrame=True
            self.newKeyTimeOffset=frameTime
        self.newkeyTime1=(float(frameTime)-self.newKeyTimeOffset)
        frameSuccess=struct.unpack('B',  f.read(1))[0]
        if frameSuccess==1:
            self.newFrame=faceShiftData.RecordetFrame(self.newkeyTime1,frameSuccess)
            self.exchangeData.doneRecTime=self.newkeyTime1
        

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
        firstFrame=True
        firstKeyTime=0
        while frameCounter<len(allFrames):
                
            frame=allFrames[frameCounter].split("C ")
            frameHeader=frame[0].split(" ")
            shapes1=frame[1].split("E ")
            shapes=shapes1[0].split(" ")
            eyes=shapes1[1].split("M ")
            eyesList=eyes[0].split(" ")
            shapeCount=1
            frameSuccess=1
            if int(frameHeader[4])==1:
                if firstFrame==True:
                    firstFrame=False
                    firstKeyTime=float(frameHeader[3])
                newkeyTime=float(frameHeader[3])-firstKeyTime
                self.newFrame=faceShiftData.RecordetFrame(newkeyTime,frameHeader[4])
                self.exchangeData.doneRecTime=newkeyTime
                headMatrix = faceshiftHelpers.quaternionToMatrix(float(frameHeader[6]),float(frameHeader[7]),float(frameHeader[8]),float(frameHeader[9]))
                self.newFrame.headRotation=headMatrix
                self.newFrame.headPosition=c4d.Vector(float(frameHeader[10]),float(frameHeader[11]),float(frameHeader[12])*-1)
                self.newFrame.blendShapeValues=[]
                shapeCount=1
                while shapeCount<=int(shapes[0]):
                    self.newFrame.blendShapeValues.append(float(shapes[shapeCount]))
                    shapeCount+=1
                self.newFrame.eyeGazeValues=[]
                eyeCount=0
                while eyeCount<4:
                    self.newFrame.eyeGazeValues.append(float(eyesList[eyeCount]))
                    eyeCount+=1 
                self.exchangeData.recordetFrames.append(self.newFrame)
            frameCounter+=1
        

        
        
   