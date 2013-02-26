import c4d
from c4d import documents
from c4d import gui
import struct
import socket
import sys

from faceshiftc4d import ids
from faceshiftc4d import faceShiftData

class FaceShiftParser(object):  
    connected=False 
    exchangeData=0 
    sock=None
    isRecordingInStream=False
    def __init__(self,workerThread,exchangeData):
        global sock
        self.exchangeData=exchangeData
        self.workerThread=workerThread   
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.setblocking(0)
        #sock.bind( ("localhost", self.port) )
        self.connectToFaceShift() 
        self.sock.close() 
        if self.workerThread is not None:
            self.workerThread.End(False)  
  

    def connectToFaceShift(self):
        print 'Try to connect'
        try:
            self.sock.connect((str(self.exchangeData.host),int(self.exchangeData.port) ))
 
        except socket.error:
            print 'Socket connect failed! Loop up and try socket again'
            return
        print 'Socket connect worked!'
        self.connected=True
        while True:
            
            if self.workerThread.TestBreak():
                self.sock.close()
                return
            if self.exchangeData.remoteMessage!=0:
                blockIDsend=struct.pack("H", self.exchangeData.remoteMessage) # i = int, I = unsigned int
                blockIDsend+=struct.pack("H", 1) # i = int, I = unsigned int
                blockIDsend+=struct.pack("I", 0) # i = int, I = unsigned int
                try:
                    self.sock.send(blockIDsend)
                except socket.error:
                    print 'Socket connect failed! Loop up and try socket again'
                    return
                self.exchangeData.remoteMessage=0
            try:
                received = self.sock.recv(64*1024)
                
            except: 
                self.sock.close()
                print "Could not read Block-Header"
                return
                
            if received:
                readBytes=0
                while (len(received)-readBytes)>8:  
                    #print "Read Block-Header "+str(len(received)) 
                    newlyReadBytes=self.readProtokollHeader(received)
                    if newlyReadBytes==0:
                        #print "Could not read Block-Header"
                        break;
                    if newlyReadBytes>0:
                        readBytes+=newlyReadBytes;       
                #print "exitFrameReader"


    def readProtokollHeader(self,received):
    
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
        returnReadBytes=0
        reciv=received[0]+received[1]
        blockID=struct.unpack('H', reciv)[0]
        reciv=received[2]+received[3]
        versionNr=struct.unpack('H', reciv)[0]
        reciv=received[4]+received[5]+received[6]+received[7]
        blockSize=struct.unpack('I', reciv)[0] 
        #print "read Block-Header = blockID: "+str(blockID)+" / versionNr: "+str(versionNr)+" / blockSize: "+str(blockSize)
        if (len(received)-8)>=blockSize:
            returnReadBytes=self.readProtokoll(received,blockID)
            return blockSize
        return returnReadBytes

            
    def readProtokoll(self,received,blockID):   
        if blockID==33433:   
            self.exchangeData.isNew=True   
            self.isRecordingInStream=False
            if self.exchangeData.isRecording==True:
                self.isRecordingInStream=True
            self.readStandartBlock(received)
        if blockID==33533:   
            pass
        if blockID==33633: 
            self.readBlendShapeNames(received)                 
        if blockID==33733:   
            self.readRig(received) 
       
    def readStandartBlock(self,received):
        reciv=received[8]+received[9]
        blockCount=struct.unpack('H', reciv)
        readerCnt=9
        blockCnt=0
        while blockCnt<blockCount[0]:
            blockCnt+=1
            readerCnt1=self.readBlock(received,readerCnt)    
            readerCnt+=(readerCnt1-readerCnt)
            
                            
    def readBlock(self,received,readerCnt):           
		
        reciv=received[readerCnt+1]+received[readerCnt+2]
        readerCnt+=2
        blockID=struct.unpack('H', reciv)                    
        reciv=received[readerCnt+1]+received[readerCnt+2]
        readerCnt+=2
        versionNr=struct.unpack('H', reciv)        
        reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
        readerCnt+=4
        blockSize=struct.unpack('I', reciv)
        
        if blockID[0]==101:
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]+received[readerCnt+5]+received[readerCnt+6]+received[readerCnt+7]+received[readerCnt+8]
            readerCnt+=8
            frameTime=struct.unpack('d', reciv)[0]
            reciv=received[readerCnt+1]
            readerCnt+=1
            tracksuccess=struct.unpack('B', reciv)[0]
            self.exchangeData.frameSuccess=tracksuccess
            self.exchangeData.frameTime=frameTime
            if self.isRecordingInStream==True:
                if self.exchangeData.startRecTimeFS==-1:
                    self.exchangeData.startRecTimeFS=frameTime
                newFrameTime=frameTime-self.exchangeData.startRecTimeFS
                if newFrameTime>0:
                    self.exchangeData.doneRecTime+=(newFrameTime)
                self.exchangeData.startRecTimeFS=frameTime
                newRenderedFrame=faceShiftData.RecordetFrame(self.exchangeData.doneRecTime)
                if tracksuccess==1:
                    self.exchangeData.recordetFrames.append(newRenderedFrame)
            #print "Frame - frameTime = "+str(frameTime)
            return readerCnt
        
        if blockID[0]==102:
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            quaternion1=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            quaternion2=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            quaternion3=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            quaternion4=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            transX=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            transY=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            transZ=struct.unpack('f', reciv)[0]
            newMatrix = quaternionToMatrix(float(quaternion1),float(quaternion2),float(quaternion3),float(quaternion4))
            self.exchangeData.rotationVector=(c4d.utils.MatrixToHPB(newMatrix))
            self.exchangeData.positionVector=(c4d.Vector(transX,transY,transZ))
            if self.isRecordingInStream==True:
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].headRotation=self.exchangeData.rotationVector
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].headPosition=self.exchangeData.positionVector
            return readerCnt
            
        if blockID[0]==103:#Blendshapes
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            blendShapesCnt=struct.unpack('I', reciv)
            bsCnt=0
            self.exchangeData.blendShapes=[]
            while bsCnt<blendShapesCnt[0]:
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                blendShapesValue=struct.unpack('f', reciv)[0]
                self.exchangeData.blendShapes.append(blendShapesValue)
                if self.isRecordingInStream==True:
                    self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].blendShapeValues.append(blendShapesValue)
                
                bsCnt+=1
                #print "Blendshapes - "+str(bsCnt)+" blendShapesValue = "+str(blendShapesValue)
            return readerCnt
                
        if blockID[0]==104:#Eyes
            self.exchangeData.eyeGazeValues=[]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('f', reciv)[0]
            self.exchangeData.eyeGazeValues.append(pose1)
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose2=struct.unpack('f', reciv)[0]
            self.exchangeData.eyeGazeValues.append(pose2)
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose3=struct.unpack('f', reciv)[0]
            self.exchangeData.eyeGazeValues.append(pose3)
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose4=struct.unpack('f', reciv)[0]
            self.exchangeData.eyeGazeValues.append(pose4)
            if self.isRecordingInStream==True:
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].eyeGazeValues.append(pose1)
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].eyeGazeValues.append(pose2)
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].eyeGazeValues.append(pose3)
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].eyeGazeValues.append(pose4)
            return readerCnt
            
        if blockID[0]==105:#Markers
            reciv=received[readerCnt+1]+received[readerCnt+2]
            readerCnt+=2
            blendShapesCnt=struct.unpack('H', reciv)
            bsCnt=0
            while bsCnt<blendShapesCnt[0]:
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                markerx=struct.unpack('f', reciv)
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                markery=struct.unpack('f', reciv)
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                markerz=struct.unpack('f', reciv)
                newMarker=c4d.Vector(markerx[0],markery[0],markerz[0])
                self.exchangeData.markers.append(newMarker)
                if self.isRecordingInStream==True:
                    self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].markerPositions.append(newMarker)
                bsCnt+=1
            return readerCnt
        return readerCnt
             
     
    def readBlendShapeNames(self,received):
        reciv=received[8]+received[9]
        readerCnt=9
        blockCount=struct.unpack('H', reciv)
        print "BlendshapesCount = "+str(blockCount) 
        blockCnt=0
        while blockCnt<blockCount[0]:
            reciv=received[readerCnt+1]+received[readerCnt+2]
            readerCnt+=2
            stringLength=struct.unpack('H', reciv)
            nameCnt=0
            blendShapeName=""
            while nameCnt<stringLength[0]:
                blendShapeName+=received[readerCnt+1]
                readerCnt+=1
                nameCnt+=1                
            self.exchangeData.registeredBlendShapeNames[blockCnt]=blendShapeName
            blockCnt+=1        
             
             
             
    def readRig(self,received):
        reciv=received[8]+received[9]+received[10]+received[11]
        readerCnt=11
        blockCount=struct.unpack('I', reciv)
        quadCnt=0
        quads=[]
        print "quads = "+str(blockCount) 
        while quadCnt<blockCount[0]:
            quadCnt+=1
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            quads.append(pose1[0])
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            quads.append(pose1[0])
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            quads.append(pose1[0])
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            quads.append(pose1[0])
                
        reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
        readerCnt+=4
        blockCount=struct.unpack('I', reciv)
        quadCnt=0
        tris=[]
        while quadCnt<blockCount[0]:
            quadCnt+=1
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            tris.append(pose1[0])
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            tris.append(pose1[0])
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)
            tris.append(pose1[0])
                    
        reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
        readerCnt+=4
        blockCount=struct.unpack('I', reciv)
        quadCnt=0
        points=[]
        while quadCnt<blockCount[0]:
            quadCnt+=1
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('f', reciv)
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose2=struct.unpack('f', reciv)
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose3=struct.unpack('f', reciv)
            newPoint=c4d.Vector(pose1[0],pose2[0],pose3[0])
            points.append(newPoint)
                
        reciv=received[readerCnt+1]+received[readerCnt+2]
        readerCnt+=2
        blockCount=struct.unpack('H', reciv)
        quadCnt=0
        shapes=[]
        while quadCnt<blockCount[0]:
            quadCnt+=1
            quadCnt2=0
            shape=[]
            while quadCnt2<(len(points)*3):
                quadCnt2+=1
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                pose1=struct.unpack('f', reciv)
                shape.append(pose1[0])
            shapes.append(shape)
                        
        #print "quads = "+str(quads) 
        print "quads = "+str(len(quads))
        #print "tris = "+str(tris) 
        print "tris = "+str(len(tris))
        #print "points = "+str(points) 
        print "points = "+str(len(points)) 
        #print "shapes = "+str(shapes) 
        print "shapes = "+str(len(shapes)) 
        print "shapes = "+str(len(shapes[0])) 
                  
        mypoly = c4d.BaseObject(c4d.Opolygon) #Create an empty polygon object
        mypoly.ResizeObject(len(points),len(quads)+len(tris)) #New number of points, New number of polygons
        mypoly.SetAllPoints(points)
        
        quadCnt=0
        quadCnt2=0
        while quadCnt<len(quads):
            mypoly.SetPolygon(quadCnt2, c4d.CPolygon(quads[quadCnt], quads[quadCnt+1],quads[quadCnt+ 2],quads[quadCnt+3]) ) #The Polygon's index, Polygon's points
            quadCnt2+=1
            quadCnt+=4
        quadCnt=0
        while quadCnt<len(tris):
            mypoly.SetPolygon(quadCnt2, c4d.CPolygon(quads[quadCnt], quads[quadCnt+1],quads[quadCnt+ 2],quads[quadCnt+2]) ) #The Polygon's index, Polygon's points
            quadCnt2+=1
            quadCnt+=3
            
        #doc.InsertObject(mypoly,None,None)
        #mypoly.Message(c4d.MSG_UPDATE)
            
        #c4d.EventAdd()
                          
    
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