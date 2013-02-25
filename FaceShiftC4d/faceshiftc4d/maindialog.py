import c4d
import os
from faceshiftc4d import ids
from faceshiftc4d import canvas
from faceshiftc4d import faceshiftparser
from faceshiftc4d import maindialogCreator
from faceshiftc4d import maindialogHelpers
from faceshiftc4d import faceShiftData

from xml.dom import minidom
import xml.dom.minidom as dom

workerThread=None
exchangeData=None
enableObjects=[]
enableStates=[] 

class MyThread(c4d.threading.C4DThread):   
    global exchangeData   
    def Main(self):
        global exchangeData    
        print "THREAD CREATES MAINDATA"   
        faceshiftparser.FaceShiftParser(self,exchangeData)    


class MainDialog(c4d.gui.GeDialog):       
    doc = c4d.documents.GetActiveDocument()      
    userarea = None
    faceShiftData=None 
    
    host="127.0.0.1"
    port=33433
    live=False
    enabledUserData=False
    targetLink=None
    playbackC4d=False
    headPoseMode=0
    
    blendShapeTargets=[]
    eyeGazeTargets=[]
    
        
    def __init__(self):   
        self.userarea = canvas.Canvas()
     
        
    def CreateLayout(self):         
        global workerThread,exchangeData
        
        maindialogCreator.createLayout(self)
        
        maindialogHelpers.InitValues(self)
        exchangeData  = faceShiftData.ExchangeData()  
        self.Enable(ids.GRP_FACESHIFT,False)
        self.Enable(ids.GRP_RECORDING,False)
            
        return True


    def CoreMessage(self, msg, result):
        pass#self.updateCanvas()
        return True


    def updateCanvas(self):
        pass
        #doc=c4d.documents.GetActiveDocument()
        #if doc==None:
        #    statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
        #    self.userarea.draw([statusStr,0,0])
        #    return
        #if doc!=None:
        #    if doc.GetDocumentPath()==None or doc.GetDocumentPath()=="":
        #        statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
        #        self.userarea.draw([statusStr,0,0])
        #        return
            
   

            
    def Timer(self, msg):   
        global exchangeData,workerThread    
        if workerThread.IsRunning():
            pass#print "worker runs = "+str(exchangeData.frameSuccess)+ "   /   "+str(exchangeData.frameTime)
            if self.live==True:    
                if exchangeData.frameSuccess==1:
                    if self.targetLink is not None:
                        self.targetLink.SetRelRot(exchangeData.rotationVector)
                        self.targetLink.SetRelPos(exchangeData.positionVector)
                        shapeCnt=0
                        while shapeCnt<len(self.blendShapeTargets):
                            if len(exchangeData.blendShapes)>shapeCnt:
                                self.targetLink[self.blendShapeTargets[shapeCnt]] = exchangeData.blendShapes[shapeCnt]
                            shapeCnt+=1
                        eyeCnt=0
                        while eyeCnt<len(self.eyeGazeTargets):
                            if len(exchangeData.eyeGazeValues)>eyeCnt:
                                self.targetLink[self.eyeGazeTargets[eyeCnt]] = exchangeData.eyeGazeValues[eyeCnt]
                            eyeCnt+=1
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
        if not workerThread.IsRunning():  
            exchangeData.connected=False
            self.Enable(ids.GRP_FACESHIFT,False)
            self.Enable(ids.GRP_RECORDING,False)
            self.SetString(ids.BTN_CONNECT,"Connect")
            if faceshiftparser.sock is not None:
                faceshiftparser.sock.close()
            self.SetTimer(0)
 
    def Command(self, id, msg): 
        global exchangeData,workerThread          
        self.updateCanvas()

            
        if id == ids.BTN_CONNECT: 
            if exchangeData.connected==False:
                exchangeData.connected=True
                self.Enable(ids.GRP_FACESHIFT,True)
                #self.Enable(ids.GRP_RECORDING,True)
                self.SetString(ids.BTN_CONNECT,"Disconnect")
                if workerThread is not None:
                    workerThread.End(False) 
                exchangeData.host=self.host
                exchangeData.port=self.port
                self.setHeadPose()    
                workerThread  = MyThread()  
                workerThread.Start() 
                self.SetTimer(5)
            elif exchangeData.connected==True:
                exchangeData.connected=False
                self.Enable(ids.GRP_FACESHIFT,False)
                self.Enable(ids.GRP_RECORDING,False)
                self.SetString(ids.BTN_CONNECT,"Connect")
                if faceshiftparser.sock is not None:
                    faceshiftparser.sock.close()
                if workerThread is not None:
                    workerThread.End(False) 
                self.SetTimer(0)
            
        
        if id == ids.LINK_TARGET:# if a object is dragged into the Link-Field
            if not (type(self.linkBox.GetLink()) is c4d.BaseObject):
                self.linkBox.SetLink(self.targetLink)# if the dragged object is no c4d.BaseObject, reset the Old Link-Target
            elif (type(self.linkBox.GetLink())) is c4d.BaseObject:
                pass#if the dragged object is a c4d-BaseObject, it will get updated in "maindialogHelpers.setValues(self)a"
        
        if id == ids.BTN_CREATE_TARGET:
            if exchangeData is None:
                exchangeData  = faceShiftData.ExchangeData()  
            maindialogHelpers.createNewTarget(self)
            print "Use Target"
        if id == ids.BTN_CREATE_TARGET:
            print "Create Target"
        if id == ids.BTN_STARTREC:
            print "START RECORDING"
            exchangeData.recording=True
        if id == ids.BTN_STOPREC:
            print "START RECORDING"
            exchangeData.recording=False
        if id == ids.BTN_CALIBRATE:
            print "CALIBRATE"
            exchangeData.remoteMessage=44544
        if id == ids.LONG_HEADPOSE:
            print "CHANGE HEADPOSE-MODUS"
            self.setHeadPose()    
        if id == ids.CBOX_LIVE :
            print "CHANGE LIVE-MODUS"
            #exchangeData.remoteMessage=44444
        #if id == ids.BTN_GETMARKERNAMES:
        #    print "GETMARKERNAMES"
        #    exchangeData.remoteMessage=44644
        #if id == ids.BTN_GETBLENDSHAPENAMES:
        #    print "GETBLENDSHAPENAMES"
        #    exchangeData.remoteMessage=44744
        #if id == ids.BTN_GETRIG:
        #    print "GETRIG"
        #    exchangeData.remoteMessage=44844
           
        #if id == ids.MENU_PRESET_LOAD:   
        #    exportResult=self.loadPreset()  
        #if id == ids.MENU_PRESET_SAVE:   
         #   exportResult=self.savePreset() 
              
        maindialogHelpers.setValues(self)     
        maindialogHelpers.setUI(self)     
        return True  
    
    
    def setHeadPose(self):
        if self.headPoseMode==0:
            exchangeData.remoteMessage=44944
        if self.headPoseMode==1:
            exchangeData.remoteMessage=44945
    # called on 'Close()'
    def AskClose(self):
        global exchangeData,workerThread  
        workerThread.End(False)    
            
        
        return False#not c4d.gui.QuestionDialog(c4d.plugins.GeLoadString(ids.STR_TITLE))
         