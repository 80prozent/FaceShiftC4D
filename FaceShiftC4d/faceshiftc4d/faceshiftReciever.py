import c4d
from c4d import documents
from c4d import gui
import struct
import socket
import sys

from faceshiftc4d import ids
from faceshiftc4d import faceShiftData
from faceshiftc4d import faceshiftHelpers

class FaceShiftReciever(object):  
    connected=False 
    exchangeData=0 
    sock=None
    isRecordingInStream=False
    def __init__(self,workerThread,exchangeData):
        global sock
        self.exchangeData=exchangeData
        self.workerThread=workerThread   
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.setblocking(0)
        self.sock.settimeout(1)
        self.connectToFaceShift() 
        self.sock.close() 
        if self.workerThread is not None:
            self.workerThread.End(False)  
  

    def connectToFaceShift(self):
        print 'Try to connect'
        self.exchangeData.connected=0
        try:
            self.sock.connect((str(self.exchangeData.host),int(self.exchangeData.port) ))
 
        except:
            print 'Socket connect failed! Loop up and try socket again'
            return
        print 'Socket connect worked!'
        self.exchangeData.connected=1
        while True:
            if self.workerThread.TestBreak():
                return
            if self.exchangeData.remoteMessage!=0:
                blockIDsend=struct.pack("H", self.exchangeData.remoteMessage) # i = int, I = unsigned int
                blockIDsend+=struct.pack("H", 1) # i = int, I = unsigned int
                blockIDsend+=struct.pack("I", 0) # i = int, I = unsigned int
                #print "new Message send = "+str(self.exchangeData.remoteMessage)
                try:
                    self.sock.send(blockIDsend)
                except:
                    print 'Socket connect failed! Loop up and try socket again'
                    return
                self.exchangeData.remoteMessage=0
            try:
                received = self.sock.recv(64*1024)
                
            except: 
                print "Could not read Block-Header"
                return
                
            if received:
                readBytes=0
                while (len(received)-readBytes)>8: 
                    #print "Read Block-Header "+str(len(received)) 
                    newlyReadBytes=self.readProtokollHeader(received)
                    if newlyReadBytes==0:
                        print "Could not read Block-Header"
                        return
                    if newlyReadBytes>0:
                        readBytes+=newlyReadBytes;     
        return


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
        while (len(received)-8)<blockSize and blockID==33733:
            try:
                receivednew = self.sock.recv(64*1024)                
            except: 
                self.sock.close()
                print "Could not read Block-Header"
                return 0                
            if receivednew:
                received+=receivednew  
                continue
            return 0
        returnReadBytes=self.readProtokoll(received,blockID)
        return blockSize

            
    def readProtokoll(self,received,blockID):  
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
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
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0          
		
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
                newRenderedFrame=faceShiftData.RecordetFrame(self.exchangeData.doneRecTime,tracksuccess)
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
            newMatrix = faceshiftHelpers.quaternionToMatrix(float(quaternion1),float(quaternion2),float(quaternion3*-1),float(quaternion4))
            self.exchangeData.rotationVector=(c4d.utils.MatrixToHPB(newMatrix))
            self.exchangeData.positionVector=(c4d.Vector(transX,transY,transZ*-1))
            if self.isRecordingInStream==True:
                self.exchangeData.recordetFrames[len(self.exchangeData.recordetFrames)-1].headRotation=newMatrix
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
        #print "BlendshapesCount = "+str(blockCount) 
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
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
        reciv=received[8]+received[9]+received[10]+received[11]
        readerCnt=11
        blockCount=struct.unpack('I', reciv)
        quadCnt=0
        quads=[]
        while quadCnt<blockCount[0]:
            quadCnt+=1
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose2=struct.unpack('I', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose3=struct.unpack('I', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose4=struct.unpack('I', reciv)[0]
            quads.append(pose4)
            quads.append(pose3)
            quads.append(pose2)
            quads.append(pose1)
            
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0    
        reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
        readerCnt+=4
        blockCount=struct.unpack('I', reciv)
        quadCnt=0
        tris=[]
        while quadCnt<blockCount[0]:
            quadCnt+=1
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose1=struct.unpack('I', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose2=struct.unpack('I', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pose3=struct.unpack('I', reciv)[0]
            tris.append(pose3)
            tris.append(pose2)
            tris.append(pose1)
               
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0     
        reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
        readerCnt+=4
        blockCount=struct.unpack('I', reciv)
        pointCnt=0
        points=[]
        while pointCnt<blockCount[0]:
            pointCnt+=1
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pointX=struct.unpack('f', reciv)[0]
            #print pointX
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pointY=struct.unpack('f', reciv)[0]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            pointZ=struct.unpack('f', reciv)[0]
            newPoint=c4d.Vector(pointX,pointY,pointZ*-1)
            points.append(newPoint)
           
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0     
        reciv=received[readerCnt+1]+received[readerCnt+2]
        readerCnt+=2
        blockCount=struct.unpack('H', reciv)[0]
        poseCnt=0
        shapes=[]
        while poseCnt<blockCount:
            poseCnt+=1
            poseCnt2=0
            reciv=received[readerCnt+1]+received[readerCnt+2]
            readerCnt+=2
            nameLength=float(struct.unpack('H', reciv)[0])
            nameCnt=0
            name=""
            while nameCnt<nameLength:
                nameCnt+=1
                name+=received[readerCnt+1]
                readerCnt+=1
            #print name
            
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
        reciv=received[readerCnt+1]+received[readerCnt+2]
        readerCnt+=2
        blockCount=struct.unpack('H', reciv)[0]
        #print "POSES = "+str(blockCount)
        poseCnt=0
        while poseCnt<blockCount:
            poseCnt+=1
            poseCnt2=0
            shape=[]
            reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
            readerCnt+=4
            length=float(struct.unpack('I', reciv)[0])
            #print length
            while poseCnt2<(len(points)):
                poseCnt2+=1
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                posepointX=float(struct.unpack('f', reciv)[0])
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                posepointY=float(struct.unpack('f', reciv)[0])
                reciv=received[readerCnt+1]+received[readerCnt+2]+received[readerCnt+3]+received[readerCnt+4]
                readerCnt+=4
                posepointZ=float(struct.unpack('f', reciv)[0])
                shape.append(c4d.Vector(posepointX,posepointY,posepointZ*-1))
            shapes.append(shape)
                        
        #print "quads = "+str(quads) 
        #print "quads = "+str(len(quads))
        #print "tris = "+str(tris) 
        #print "tris = "+str(len(tris))
        #print "points = "+str(points) 
        #print "points = "+str(len(points)) 
        #print "shapes = "+str(shapes) 
        #print "shapes = "+str(len(shapes)) 
        
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
        
        mypoly = c4d.BaseObject(c4d.Opolygon) #Create an empty polygon object
        mypoly.ResizeObject(len(points),len(quads)+len(tris)) #New number of points, New number of polygons
        mypoly.SetAllPoints(points)
        
        quadCnt=0
        quadCnt2=0
        while quadCnt<len(quads):
            mypoly.SetPolygon(quadCnt2, c4d.CPolygon(quads[quadCnt], quads[quadCnt+1],quads[quadCnt+ 2],quads[quadCnt+3]) ) #The Polygon's index, Polygon's points
            quadCnt2+=1
            quadCnt+=4
            
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
        quadCnt=0
        while quadCnt<len(tris):
            mypoly.SetPolygon(quadCnt2, c4d.CPolygon(quads[quadCnt], quads[quadCnt+1],quads[quadCnt+ 2],quads[quadCnt+2]) ) #The Polygon's index, Polygon's points
            quadCnt2+=1
            quadCnt+=3
            
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0
        self.exchangeData.newRiggPoses=[]
        shapeCnt=0
        while shapeCnt<len(shapes):
            newPoly=mypoly.GetClone()
            #print shapes[shapeCnt]
            newPoly.SetAllPoints(shapes[shapeCnt])
            self.exchangeData.newRiggPoses.append(newPoly)
            shapeCnt+=1
           
        if self.workerThread.TestBreak():
            self.sock.close()
            return 0 
        self.exchangeData.newRigg=mypoly    
        c4d.SpecialEventAdd(ids.EVT_NEWRIGG)
                          
      