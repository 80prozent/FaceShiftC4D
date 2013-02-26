import c4d
import os
from faceshiftc4d import ids
from faceshiftc4d import canvas
from faceshiftc4d import faceshiftparser
from faceshiftc4d import maindialogCreator
from faceshiftc4d import maindialogHelpers
from faceshiftc4d import faceShiftData
from faceshiftc4d import fileloader
from faceshiftc4d import renderthread
from xml.dom import minidom
import xml.dom.minidom as dom

workerThread=None# this will contain the Thread that the TCP/IP-Socket lives in
exchangeData=None# this is a class to hold all date that needs to be accessed from workerThread and MainThread 


class MyThread(c4d.threading.C4DThread):  
    def Main(self):
        global exchangeData     
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
        self.Enable(ids.BTN_ADDREC,False)
            
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
        if exchangeData.isRecording==True:
            self.SetString(ids.TXT_FRAMES2,len(exchangeData.recordetFrames))
            self.SetString(ids.TXT_SEC,str(exchangeData.doneRecTime/1000)+" s")
            if self.playbackC4d==True:
                timea=float(float(exchangeData.startRecTimeC4D)+float(exchangeData.doneRecTime))/1000
                print "hier = "+str(timea)
                c4d.documents.GetActiveDocument().SetTime(c4d.BaseTime(timea))
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
        if self.live==True: 
            if not self.renderer.IsRunning(): 
                shapeCnt=0
                eyeCnt=0
                while shapeCnt<len(self.controllData):
                    if shapeCnt<48:
                        if len(exchangeData.blendShapes)>shapeCnt:
                            self.controll[self.controllData[shapeCnt]] =exchangeData.blendShapes[shapeCnt]
                    shapeCnt+=1
                    #if shapeCnt>=48:
                    #    self.controll[self.controllData[shapeCnt]] =exchangeData.eyeGazeValues[eyeCnt]
                    #    eyeCnt+=1
                self.controll.SetRelRot(exchangeData.rotationVector)
                self.renderer._doc.SetChanged()
                #c4d.EventAdd() 
                self.userarea.draw([self.renderer.bmp,0,0])
                self.renderer.Start() 
        #c4d.bitmaps.ShowBitmap(self.renderer.bmp)
        if workerThread.IsRunning():
            #c4d.bitmaps.ShowBitmap(self.renderer.bmp)
            #print "worker runs = "+str(exchangeData.frameSuccess)+ "   /   "+str(exchangeData.frameTime)
            if self.enabledUserData==True:  
                if exchangeData.isNew==True:
                    exchangeData.isNew=False
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
            self.userarea.draw([])
            #self.SetTimer(0)
 
    def Command(self, id, msg): 
        global exchangeData,workerThread          
        self.updateCanvas()

            
        if id == ids.BTN_CONNECT: 
            newPath = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], "previewHeads", "80prozent.c4d")
            newdoc=c4d.documents.LoadDocument(newPath, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS)
            self.renderer=renderthread.RenderThread(newdoc,c4d.RENDERFLAGS_EXTERNAL|c4d.RENDERFLAGS_PREVIEWRENDER)
            self.renderer.Start()
            #c4d.bitmaps.ShowBitmap(self.renderer.bmp)
            self.controll=newdoc.GetObjects()[0].GetDown()
            self.controllData=[]
            for id, bc in self.controll.GetUserDataContainer():
                self.controllData.append(id)
                #print id, bc
            if exchangeData.connected==False:
                exchangeData.connected=True
                self.Enable(ids.GRP_FACESHIFT,True)
                self.Enable(ids.GRP_RECORDING,True)
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
                if workerThread is not None:
                    workerThread.End(False) 
                self.userarea.draw([])
                self.SetTimer(0)
            
        
        if id == ids.LINK_TARGET:# if a object is dragged into the Link-Field
            if not (type(self.linkBox.GetLink()) is c4d.BaseObject):
                self.linkBox.SetLink(self.targetLink)# if the dragged object is no c4d.BaseObject, reset the Old Link-Target
            elif (type(self.linkBox.GetLink())) is c4d.BaseObject:
                returner=maindialogHelpers.registerNewtarget(self,self.linkBox.GetLink())#if the dragged object is a c4d-BaseObject, it will get updated in "maindialogHelpers.setValues(self)a"
                if returner==False:
                    self.linkBox.SetLink(self.targetLink)
        if id == ids.BTN_CREATE_TARGET:
            if exchangeData is None:
                exchangeData  = faceShiftData.ExchangeData()  
            maindialogHelpers.createNewTarget(self)
            print "Use Target"
        if id == ids.BTN_CREATE_TARGET:
            pass#print "Create Target"
        if id == ids.BTN_STARTREC:
            print "START RECORDING"
            if exchangeData.isRecording==False:
                self.SetString(ids.BTN_STARTREC,"Stop Recording")
                if len(exchangeData.recordetFrames)>0:
                    print "Shit "+str(len(exchangeData.recordetFrames))
                exchangeData.recordetFrames=[]
                self.Enable(ids.BTN_ADDREC,False)
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
                exchangeData.startRecTimeC4D=c4d.documents.GetActiveDocument().GetTime().Get()*1000
                print (exchangeData.startRecTimeC4D)
                exchangeData.startRecTimeFS=-1
                exchangeData.isRecording=True
                exchangeData.doneRecTime=0
            elif exchangeData.isRecording==True:
                self.SetString(ids.BTN_STARTREC,"Start Recording")
                exchangeData.isRecording=False
                self.Enable(ids.BTN_ADDREC,True)
                
                
        if id == ids.BTN_ADDREC:
            print "START RECORDING"
            maindialogHelpers.addRecording(self,exchangeData)
            #exchangeData.recording=False
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
        if id == ids.MENU_FILE_LOADRIG:
            print "GETRIG"
            exchangeData.remoteMessage=44844
        if id == ids.MENU_FILE_LOADREC:
            print "GETRIG"
            fileloader.main()
           
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
         