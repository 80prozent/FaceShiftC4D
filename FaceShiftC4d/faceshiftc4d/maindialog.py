import c4d
import os
import time
import math
from faceshiftc4d import ids
from faceshiftc4d import canvas
from faceshiftc4d import canvasShapes
from faceshiftc4d import canvasShapes2
from faceshiftc4d import faceshiftReciever
from faceshiftc4d import maindialogCreator
from faceshiftc4d import maindialogHelpers
from faceshiftc4d import faceshiftHelpers
from faceshiftc4d import faceShiftData
from faceshiftc4d import fileloader
from faceshiftc4d import renderthread
from faceshiftc4d import names
from xml.dom import minidom
import xml.dom.minidom as dom

workerThread=None# this will contain the Thread that the TCP/IP-Socket lives in
exchangeData=None# this is a class to hold all date that needs to be accessed from workerThread and MainThread 


class MyThread(c4d.threading.C4DThread):  
    def Main(self):
        global exchangeData     
        faceshiftReciever.FaceShiftReciever(self,exchangeData)    


class MainDialog(c4d.gui.GeDialog):       
    doc = c4d.documents.GetActiveDocument()      
    userarea = None 
    userareaPoseList1 = None 
    userareaPosePrev1 = None
    userareaPoseList2 = None 
    userareaPosePrev2 = None
    scrollGroup = None
    ycounter=0
    
    userareaHeadPrev=None
    userareaHeadList=None
    userareaEyeMapPrev=None
    userareaEyeMapList=None
    userareaEyeGazePrev=None
    userareaEyeGazeList=None
    userareaPose3Objects=None
    userareaPose3Tags=None
    userareaPose3Mats=None
    userareaPose3Attributes=None
    faceShiftData=None 
    host="127.0.0.1"
    port=33433
    live=False
    enabledUserData=False
    targetLink=None
    playbackC4d=False
    headPoseMode=0
    curTabGroup=ids.TABGRP_LIVESTREAM
    curPoseTabGroup=ids.TABGRP_MAPPING
    controllTag=None
    blendShapeTargets=[]
    eyeGazeTargets=[]
    controllData=[]
    prevMainDocsPathes=[]
    prevShapesDocsPathes=[]
    prevEyeDocsPathes=[]
    prevHeadDocsPathes=[]
    prevDocIdx=0
    oldTime=time.clock()
    newTime=0
    renderer=None
    scrollerHeight=0
        
    def __init__(self):  
        self.prevMainDocsPathes=[]
        self.prevShapesDocsPathes=[]
        os.chdir(os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], "previewHeads"))
        for files in os.listdir("."):
            if files.endswith(".c4d"):
                preFixTest=str(files).split("_")
                if preFixTest[0] == "mainView":
                    self.prevMainDocsPathes.append(files)
                if preFixTest[0] == "shapeView":
                    self.prevShapesDocsPathes.append(files)
                if preFixTest[0] == "mainView":#eyeView":
                    self.prevEyeDocsPathes.append(files)
                if preFixTest[0] == "mainView":#"headView":
                    self.prevHeadDocsPathes.append(files)
        #print self.prevMainDocsPathes        
        #print self.prevShapesDocsPathes            
        #newPath1 = self.prevShapesDocsPathes[0]
        #newdoc1=c4d.documents.LoadDocument(newPath1, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS)
        #self.previewRenderer2=renderthread.RenderThread(newdoc1,ids.TABGRP_EXPRESSIONMAPPING,c4d.RENDERFLAGS_EXTERNAL|c4d.RENDERFLAGS_PREVIEWRENDER,False)
        #self.userarea = canvas.Canvas()
        #self.userareaPoseList1 = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaPosePrev1 = canvasShapes2.Canvas()
        #self.userareaPoseList2 = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaPosePrev2 = canvasShapes2.Canvas()
        #self.userareaPose3Objects = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaPose3Tags = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaPose3Mats = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaPose3Attributes = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaHeadList = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaHeadPrev = canvasShapes2.Canvas() 
        #self.userareaEyeMapList = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaEyeMapPrev = canvasShapes2.Canvas() 
        #self.userareaEyeGazeList = canvasShapes.CanvasShapes(self.previewRenderer2)
        #self.userareaEyeGazePrev=canvasShapes2.Canvas() 
        
        self.previewDocs=[]
        
     
        
    def CreateLayout(self):         
        global workerThread,exchangeData
        
        maindialogCreator.createLayout(self)
        self.scrollerHeight=self.scrollerHeight
        fileCnt=0
        while fileCnt<len(self.prevMainDocsPathes):
            preFixTest=str(self.prevMainDocsPathes[fileCnt]).split(".")
            preFixTest2=preFixTest[0].split("_")
            dateiName=""
            dataCnt=1
            while dataCnt<len(preFixTest2):
                dateiName+=str(preFixTest2[dataCnt])
                if dataCnt!=len(preFixTest2)-1:
                    dateiName+="_"
                dataCnt+=1
            self.AddChild(ids.COMBO_PREVDOC, fileCnt, str(dateiName))
            fileCnt+=1
        fileCnt=0
        while fileCnt<len(self.prevShapesDocsPathes):
            preFixTest=str(self.prevShapesDocsPathes[fileCnt]).split(".")
            preFixTest2=preFixTest[0].split("_")
            dateiName=""
            dataCnt=1
            while dataCnt<len(preFixTest2):
                dateiName+=str(preFixTest2[dataCnt])
                if dataCnt!=len(preFixTest2)-1:
                    dateiName+="_"
                dataCnt+=1
            self.AddChild(ids.POSE1_COMBO_PREVDOC, fileCnt, str(dateiName))
            fileCnt+=1
        fileCnt=0
        while fileCnt<len(self.prevEyeDocsPathes):
            preFixTest=str(self.prevEyeDocsPathes[fileCnt]).split(".")
            preFixTest2=preFixTest[0].split("_")
            dateiName=""
            dataCnt=1
            while dataCnt<len(preFixTest2):
                dateiName+=str(preFixTest2[dataCnt])
                if dataCnt!=len(preFixTest2)-1:
                    dateiName+="_"
                dataCnt+=1
            self.AddChild(ids.EYEMAP_COMBO_PREVIEW, fileCnt, str(dateiName))
            self.AddChild(ids.EYEGAZE_COMBO_PREVIEW, fileCnt, str(dateiName))
            fileCnt+=1
        fileCnt=0
        while fileCnt<len(self.prevHeadDocsPathes):
            preFixTest=str(self.prevHeadDocsPathes[fileCnt]).split(".")
            preFixTest2=preFixTest[0].split("_")
            dateiName=""
            dataCnt=1
            while dataCnt<len(preFixTest2):
                dateiName+=str(preFixTest2[dataCnt])
                if dataCnt!=len(preFixTest2)-1:
                    dateiName+="_"
                dataCnt+=1
            self.AddChild(ids.HEAD_COMBO_PREVIEW, fileCnt, str(dateiName))
            fileCnt+=1
        
        maindialogHelpers.InitValues(self)
        exchangeData  = faceShiftData.ExchangeData()  
        self.Enable(ids.GRP_FACESHIFT,False)
        self.Enable(ids.GRP_RECORDING,False)
        self.Enable(ids.BTN_ADDREC,False)
        self.Enable(ids.MENU_FILE_CLEAR,False)
        self.Enable(ids.MENU_FILE_LOAD,False)
        self.Enable(ids.MENU_FILE_SAVE,False)
        self.Enable(ids.MENU_FILE_LOADRIG,False)
        self.Enable(ids.MENU_FILE_SAVERIG,False)
        self.Enable(ids.MENU_FILE_LOADREC,True)
        self.Enable(ids.MENU_FILE_SAVEREC,False)
        self.Enable(ids.CBOX_LIVE,False)
        #shapeNames=[]
        #shapeNames.append("Neutral")
        #for name in names.blendShapeNames:
        #    shapeNames.append(name)
        #self.userareaPoseList1.draw(shapeNames)
        #self.userareaPoseList2.draw(shapeNames)
            
        #self.previewRenderer2.Start()
        return True


    def CoreMessage(self, msg, result):
        global exchangeData
        if msg==ids.EVT_NEWRIGG:
            doc=c4d.documents.GetActiveDocument()
            doc.InsertObject(exchangeData.newRigg,None,None)
            exchangeData.newRigg.Message(c4d.MSG_UPDATE)
            shapeCnt=len(exchangeData.newRiggPoses)-1
            while shapeCnt>=0:
                doc.InsertObject(exchangeData.newRiggPoses[shapeCnt],exchangeData.newRigg,None)
                exchangeData.newRiggPoses[shapeCnt].SetName(names.blendShapeNames[shapeCnt])
                exchangeData.newRiggPoses[shapeCnt].Message(c4d.MSG_UPDATE)
                shapeCnt-=1                
            c4d.EventAdd()
            #exchangeData.newRigg=None
        if msg==ids.EVT_FINISHEDRENDER2:
            #c4d.gui.UpdateMenus()
            self.LayoutChanged(self.scrollGroup)
            if self.curTabGroup==ids.TABGRP_EXPRESSIONMAPPING: 
                self.LayoutFlushGroup(ids.POSE2_SCROLLGROUP)
                #self.scrollerHeight=self.userareaPoseList2.GetHeight()#-180#self.userareaPosePrev2.newHeight
                #print self.scrollerHeight
                #self.scrollGroup=self.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT|c4d.SCROLLGROUP_NOBLIT,170,100)
                #self.GroupBorderNoTitle(c4d.BORDER_BLACK)
                #self.userareaas3 = self.AddUserArea(ids.POSE2_USERAREA_TARGETLIST, flags=c4d.BFV_CENTER|c4d.BFH_CENTER,initw=170,inith=self.scrollerHeight)
                #self.AttachUserArea(self.userareaPoseList2,ids.POSE2_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)  
                        #End Level 6 
                #self.GroupEnd()
    
   #self.userareaas3 = self.AddUserArea(ids.POSE2_USERAREA_TARGETLIST, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=170,inith=self.scrollerHeight)

                #self.LayoutChanged(ids.POSE2_SCROLLGROUP)
                #self.AttachUserArea(self.userareaPoseList2,ids.POSE2_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)  
                #shapeNames=[]
                #shapeNames.append("Neutral")
                #for name in names.blendShapeNames:
                #    shapeNames.append(name)
                #self.userareaPoseList2.draw(shapeNames)
                #if self.curPoseTabGroup==ids.TABGRP_MAPPING: 
                #    self.userareaPosePrev1.draw([self.userareaPoseList1.renderer.bmp,0,0])
                #if self.curPoseTabGroup==ids.TABGRP_POSES: 
                #    self.userareaPosePrev2.draw([self.userareaPoseList1.renderer.bmp,0,0])
                #print "Jeah"
                #self.renderer.Start() 
            if self.curTabGroup!=ids.TABGRP_EXPRESSIONMAPPING: 
                pass#print "Stop PreviewRenderer"
        if msg==ids.EVT_FINISHEDRENDER1:
            if self.curTabGroup==ids.TABGRP_LIVESTREAM: 
                if self.live==True: 
                    shapeCnt=0
                    eyeCnt=0
                    while shapeCnt<len(self.controllData):
                        if shapeCnt<48:
                            if len(exchangeData.blendShapes)>shapeCnt:
                                self.controllTag[self.controllData[shapeCnt]] = exchangeData.blendShapes[shapeCnt]
                        shapeCnt+=1
                    #self.newTime=time.clock()-self.oldTime
                    #newtime2=1000/(self.newTime*1000)
                    #newtime3=int(newtime2*100)
                    #newtime4=float(newtime3/100)
                    #self.SetString(ids.STR_PREVFPS,str(newtime4)+" FPS ")
                    #print "RenderTime = "+str(newtime2)
                    #self.oldTime=time.clock()
                        #if shapeCnt>=48:
                        #    self.controll[self.controllData[shapeCnt]] =exchangeData.eyeGazeValues[eyeCnt]
                        #    eyeCnt+=1
                    #self.controll.SetRelRot(exchangeData.rotationVector)
                    #self.renderer._doc.SetChanged()
                    #c4d.EventAdd() 
                    #self.userarea.draw([self.renderer.bmp,0,0])
                    if workerThread is not None:
                        if not workerThread.IsRunning():
                            self.renderer.End() 
                            self.userarea.draw([])
                            return True
                        return True
                    
                    self.renderer.End() 
                    self.userarea.draw([])
                    #self.renderer.End() 
                    #self.userarea.draw([])
                    return True
            if self.curTabGroup!=ids.TABGRP_LIVESTREAM: 
                pass
                #self.renderer.End() 
                #self.userarea.draw([])
            
                #print "Stop PreviewRenderer"
            #Fired by the main thread...
            #self.dlg.LayoutChanged(GROUP_ID)
            #return True
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
        #        
        #        return
            
   

            
    def Timer(self, msg):   
        #print "Execute Timer"
        global exchangeData,workerThread  
        if self.curTabGroup==ids.TABGRP_LIVESTREAM: 
            if exchangeData.isRecording==True:
                self.SetString(ids.TXT_FRAMES2,len(exchangeData.recordetFrames))
                self.SetString(ids.TXT_SEC,str(exchangeData.doneRecTime/1000)+" s")
                if self.playbackC4d==True:
                    timea=float(float(exchangeData.startRecTimeC4D)+float(exchangeData.doneRecTime))/1000
                    #print "hier = "+str(timea)
                    c4d.documents.GetActiveDocument().SetTime(c4d.BaseTime(timea))
                    c4d.EventAdd(c4d.EVENT_ANIMATE) 
            #c4d.bitmaps.ShowBitmap(self.renderer.bmp)
            if workerThread.IsRunning():
                if exchangeData.connected==1:
                    exchangeData.connected=2
                    self.Enable(ids.GRP_FACESHIFT,True)
                    self.Enable(ids.GRP_RECORDING,True)
                    self.Enable(ids.BTN_STARTREC,True)
                    self.Enable(ids.CBOX_PLAYBACK,True)
                    
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
                        #print self.targetLink.GetFirstTag().GetNodeMaster()
                        #c4d.GeSyncMessage(c4d.EVMSG_ASYNCEDITORMOVE) 
                        #c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED) 
                        #c4d.documents.GetActiveDocument().SetTime(c4d.BaseTime(0))
                        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK)
                        #c4d.EventAdd(c4d.EVENT_FORCEREDRAW) 
            if not workerThread.IsRunning():  
                print "not RUnning"
                exchangeData.connected=False
                self.Enable(ids.GRP_FACESHIFT,False)
                if len(exchangeData.recordetFrames)==0:
                    self.Enable(ids.GRP_RECORDING,False)
                if len(exchangeData.recordetFrames)>0:
                    self.Enable(ids.BTN_STARTREC,False)
                    self.Enable(ids.CBOX_PLAYBACK,False)
                self.SetString(ids.BTN_CONNECT,"Connect")
                #self.userarea.draw([])
                self.SetTimer(0)
                
        if self.curTabGroup==ids.TABGRP_EXPRESSIONMAPPING:
            pass
 
    def Command(self, id, msg): 
        global exchangeData,workerThread          
        self.updateCanvas()
        if id == ids.TAB_ALL:
            self.curTabGroup=self.GetLong(ids.TAB_ALL)
            if exchangeData.connected==2 and self.live==True:
                pass#self.renderer.Start()
        if self.curTabGroup==ids.TABGRP_EXPRESSIONMAPPING:
            if id == ids.TAB_EXPRESSIONMAPPING:
                pass#self.curPoseTabGroup=self.GetLong(ids.TAB_EXPRESSIONMAPPING)
                #self.userareaPosePrev2.draw([self.userareaPoseList1.renderer.bmp,0,0])
            if id == ids.POSE1_BTN_SAVE: 
                pass#self.userareaPoseList1.trainedPoses[self.userareaPoseList1.selected]=1
                #self.userareaPoseList1.Redraw()
        if self.curTabGroup==ids.TABGRP_LIVESTREAM:
            if id == ids.COMBO_PREVDOC: 
                prevdoc=self.GetLong(ids.COMBO_PREVDOC)
                if self.prevDocIdx!=prevdoc:
                    self.prevDocIdx=prevdoc
                    if self.renderer is not None:
                        if self.renderer.IsRunning():
                            self.renderer.End()
                    #newPath = self.prevMainDocsPathes[self.prevDocIdx]
                    #newdoc=c4d.documents.LoadDocument(newPath, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS)#PREVIEWRENDER
                    #self.renderer=renderthread.RenderThread(newdoc,ids.TABGRP_LIVESTREAM,c4d.RENDERFLAGS_EXTERNAL|c4d.RENDERFLAGS_NODOCUMENTCLONE,True)
                    #self.renderer.Start()
                    #c4d.bitmaps.ShowBitmap(self.renderer.bmp)
                    #self.controll=newdoc.GetObjects()[0]
                    #self.controllTag=self.controll.GetTag(1024237)
                    #self.controllData=[]
                    #if self.controllTag:
                    #    allMorphs=self.controllTag.GetMorphCount()
                    #    morphCnt=1
                    #    while morphCnt<allMorphs:
                    #        self.controllData.append(self.controllTag.GetMorphID(morphCnt))
                    #        morphCnt+=1
                     
                    
                
            if id == ids.BTN_CONNECT: 
                #c4d.gui.SelectionListDialog(c4d.documents.GetActiveDocument().GetObjects(), c4d.documents.GetActiveDocument())
                #newPath = self.prevMainDocsPathes[0]
                #newdoc=c4d.documents.LoadDocument(newPath, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS)
                #self.renderer=renderthread.RenderThread(newdoc,ids.TABGRP_LIVESTREAM,c4d.RENDERFLAGS_EXTERNAL|c4d.RENDERFLAGS_PREVIEWRENDER,True)
                #self.renderer.Start()
                #c4d.bitmaps.ShowBitmap(self.renderer.bmp)
                #self.controll=newdoc.GetObjects()[0]
                #self.controllTag=self.controll.GetTag(1024237)
                #self.controllData=[]
                #if self.controllTag:
                #    allMorphs=self.controllTag.GetMorphCount()
                #    morphCnt=1
                #    while morphCnt<allMorphs:
                #        self.controllData.append(self.controllTag.GetMorphID(morphCnt))
                #        morphCnt+=1
                #    print self.controllData
                #for id, bc in self.controll.GetUserDataContainer():
                 #   self.controllData.append(id)
                    #print id, bc
                if exchangeData.connected==False:
                    exchangeData.connected=True
                    self.SetString(ids.BTN_CONNECT,"Disconnect")
                    if workerThread is not None:
                        workerThread.End(False) 
                    exchangeData.host=self.host
                    exchangeData.port=self.port
                    self.setHeadPose()    
                    workerThread  = MyThread()  
                    workerThread.Start() 
                    self.SetTimer(25)
                elif exchangeData.connected==2 and exchangeData.isRecording==False:
                    exchangeData.connected=0
                    self.Enable(ids.GRP_FACESHIFT,False)
                    if len(exchangeData.recordetFrames)==0:
                        self.Enable(ids.GRP_RECORDING,False)
                    if len(exchangeData.recordetFrames)>0:
                        self.Enable(ids.BTN_STARTREC,False)
                        self.Enable(ids.BTN_ADDREC,True)
                        self.Enable(ids.CBOX_PLAYBACK,False)
                    self.SetString(ids.BTN_CONNECT,"Connect")
                    if workerThread is not None:
                        workerThread.End(False) 
                    #self.userarea.draw([])
                    self.SetTimer(0)            
            
            if id == ids.LINK_TARGET:# if a object is dragged into the Link-Field
                if type(self.linkBox.GetLink()) is None:
                    return True
                if not (type(self.linkBox.GetLink()) is c4d.BaseObject):
                    self.linkBox.SetLink(self.targetLink)# if the dragged object is no c4d.BaseObject, reset the Old Link-Target
                elif (type(self.linkBox.GetLink())) is c4d.BaseObject:                    
                    returner=faceshiftHelpers.registerNewtarget(self,self.linkBox.GetLink())#if the dragged object is a c4d-BaseObject, it will get updated in "maindialogHelpers.setValues(self)a"
                    if returner==False:
                        self.linkBox.SetLink(self.targetLink)
                      
            if id == ids.CBOX_LIVE:
                self.live=self.GetBool(ids.CBOX_LIVE)
                if self.live==True:
                    self.renderer.Start()  
                
            if id == ids.BTN_CREATE_TARGET:
                #newMaindialog=MainDialog()
                if exchangeData is None:
                    exchangeData  = faceShiftData.ExchangeData()  
                faceshiftHelpers.createNewTarget(self)
                
            if id == ids.BTN_STARTREC:
                print "START RECORDING"
                if exchangeData.isRecording==False:
                    if len(exchangeData.recordetFrames)>0:
                        answer=c4d.gui.QuestionDialog("Override exisiting Data?")
                        if answer==False:
                            return False
                    self.SetString(ids.BTN_STARTREC,"Stop Recording")
                        #c4d.gui.MessageDialog("Could not use the Object as target, because UserData-DataTyps does not match")
                    exchangeData.recordetFrames=[]
                    self.Enable(ids.BTN_ADDREC,False)
                    c4d.EventAdd(c4d.EVENT_ANIMATE) 
                    exchangeData.startRecTimeC4D=c4d.documents.GetActiveDocument().GetTime().Get()*1000
                    c4d.documents.RunAnimation(c4d.documents.GetActiveDocument(),False)
                    exchangeData.startRecTimeFS=-1
                    exchangeData.isRecording=True
                    exchangeData.doneRecTime=0                
                elif exchangeData.isRecording==True:
                    self.SetString(ids.BTN_STARTREC,"Start Recording")
                    c4d.documents.RunAnimation(c4d.documents.GetActiveDocument(),True)
                    exchangeData.isRecording=False
                    self.Enable(ids.BTN_ADDREC,True)
                    
            if id == ids.BTN_ADDREC:
                print "ADD RECORDING TO TIMELINE"
                faceshiftHelpers.addRecording(self,exchangeData)
                c4d.EventAdd()
                
            if id == ids.TMP_SHAPES:
                tester=self.checkForTarget()
                if tester==True:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                        poseTags=doc.GetActiveTags()
                        tagsdone=0
                        xpressoTag=self.targetLink.GetFirstTag()
                        nodemaster = xpressoTag.GetNodeMaster() #Generates xpresso nodes
                        #node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_CONDITION, insert=None, x=300, y=200) #create condition node and place in X,Y coord

                        mainNode=nodemaster.GetRoot().GetChildren()[1]
                        allOutports=mainNode.GetOutPorts()
                        for tag in poseTags:
                            if tag.GetType()==1024237:
                                newNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=500, y=self.ycounter) #create Object node and place in X,Y coord
                                self.ycounter+=100
                                newNode[c4d.GV_OBJECT_OBJECT_ID] = tag
                                morphConnector=[]
                                morphCount=1
                                maxMorph=tag.GetMorphCount()
                                while morphCount<maxMorph:
                                    shapeCnt=0
                                    newPose=newNode.AddPort(c4d.GV_PORT_INPUT, tag.GetMorphID(morphCount)) #add a position input port to the object node
                                    self.ycounter+=20
                                    while shapeCnt < len(allOutports):
                                        if allOutports[shapeCnt].GetName(mainNode)==str(tag.GetMorph(morphCount).GetName()):
                                            allOutports[shapeCnt].Connect(newPose)
                                            shapeCnt=len(allOutports)
                                        shapeCnt+=1
                                    morphCount+=1
                                tagsdone+=1
                        c4d.modules.graphview.RedrawMaster(nodemaster)
                        c4d.EventAdd() 
                        if tagsdone==0:
                            c4d.gui.MessageDialog("No Pose-Tag connected")
                        
                    print "Connect Shapes"
                if tester==False:
                    c4d.gui.MessageDialog("No UserData-Object connected")
            if id == ids.TMP_HEAD_TRANS:
                tester=self.checkForTarget()
                if tester==True:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                        headObj=doc.GetActiveObject()
                        if headObj is not None:
                            print "Connect Head Position"
                            xpressoTag=self.targetLink.GetFirstTag()
                            nodemaster = xpressoTag.GetNodeMaster() #Generates xpresso nodes
                            #node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_CONDITION, insert=None, x=300, y=200) #create condition node and place in X,Y coord
                            mainNode=nodemaster.GetRoot().GetChildren()[1]
                            rotationNode=mainNode.GetPort(c4d.ID_BASEOBJECT_REL_POSITION)
                            if rotationNode is None:
                                rotationNode = mainNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_POSITION) #add a position input port to the object node
                            newNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=500, y=self.ycounter) #create Object node and place in X,Y coord
                            self.ycounter+=100
                            newNode[c4d.GV_OBJECT_OBJECT_ID] = headObj
                            newPose=newNode.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_REL_POSITION) #add a position input port to the object node
                            rotationNode.Connect(newPose)                    
                            c4d.modules.graphview.RedrawMaster(nodemaster)
                            c4d.EventAdd() 
                if tester==False:
                    c4d.gui.MessageDialog("No UserData-Object connected")
            if id == ids.TMP_HEAD_ROT:
                tester=self.checkForTarget()
                if tester==True:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                        headObj=doc.GetActiveObject()
                        if headObj is not None:
                            print "Connect Head Rotation"
                            xpressoTag=self.targetLink.GetFirstTag()
                            nodemaster = xpressoTag.GetNodeMaster() #Generates xpresso nodes
                            #node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_CONDITION, insert=None, x=300, y=200) #create condition node and place in X,Y coord
                            mainNode=nodemaster.GetRoot().GetChildren()[1]
                            rotationNode=mainNode.GetPort(c4d.ID_BASEOBJECT_REL_ROTATION)
                            if rotationNode is None:
                                rotationNode = mainNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_ROTATION) #add a position input port to the object node
                            newNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=500, y=self.ycounter) #create Object node and place in X,Y coord
                            self.ycounter+=100
                            newNode[c4d.GV_OBJECT_OBJECT_ID] = headObj
                            newPose=newNode.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_REL_ROTATION) #add a position input port to the object node
                            rotationNode.Connect(newPose)                    
                            c4d.modules.graphview.RedrawMaster(nodemaster)
                            c4d.EventAdd() 
                if tester==False:
                    c4d.gui.MessageDialog("No UserData-Object connected")
            if id == ids.TMP_EYE_R:
                tester=self.checkForTarget()
                if tester==True:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                        headObj=doc.GetActiveObject()
                        if headObj is not None:
                            print "Connect Eye Right"
                            xpressoTag=self.targetLink.GetFirstTag()
                            nodemaster = xpressoTag.GetNodeMaster() #Generates xpresso nodes
                            #node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_CONDITION, insert=None, x=300, y=200) #create condition node and place in X,Y coord
                            mainNode=nodemaster.GetRoot().GetChildren()[1]
                            allOutports=mainNode.GetOutPorts()
                            node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_RANGEMAPPER, insert=None, x=450, y=self.ycounter) #create condition node and place in X,Y coord
                            node1[c4d.GV_RANGEMAPPER_OUTPUT_DEFS]=1
                            node1[c4d.GV_RANGEMAPPER_RANGE11]=-90
                            node1[c4d.GV_RANGEMAPPER_RANGE12]=90
                            node1[c4d.GV_RANGEMAPPER_RANGE21]=-90*(math.pi/180)
                            node1[c4d.GV_RANGEMAPPER_RANGE22]=90*(math.pi/180)
                            newNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=550, y=self.ycounter) 
                            self.ycounter+=200 
                            node2 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_RANGEMAPPER, insert=None, x=450, y=self.ycounter) #create condition node and place in X,Y coord
                            node2[c4d.GV_RANGEMAPPER_OUTPUT_DEFS]=1
                            node2[c4d.GV_RANGEMAPPER_RANGE11]=-90
                            node2[c4d.GV_RANGEMAPPER_RANGE12]=90
                            node2[c4d.GV_RANGEMAPPER_RANGE21]=-90*(math.pi/180)
                            node2[c4d.GV_RANGEMAPPER_RANGE22]=90*(math.pi/180)
                            self.ycounter+=200
                            newNode[c4d.GV_OBJECT_OBJECT_ID] = headObj
                            shapeCnt=0
                            while shapeCnt < len(allOutports):
                                if str(allOutports[shapeCnt].GetName(mainNode))=="Eye_R_Ver":
                                    print "Jes"
                                    newPose=newNode.AddPort(c4d.GV_PORT_INPUT, (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X)) #add a position input port to the object node
                                    allOutports[shapeCnt].Connect(node1.GetInPorts()[0])
                                    node1.GetOutPorts()[0].Connect(newPose)
                                if allOutports[shapeCnt].GetName(mainNode)=="Eye_R_Hor":
                                    newPose=newNode.AddPort(c4d.GV_PORT_INPUT, (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Y)) #add a position input port to the object node
                                    allOutports[shapeCnt].Connect(node2.GetInPorts()[0])
                                    node2.GetOutPorts()[0].Connect(newPose)
                                shapeCnt+=1
                            c4d.modules.graphview.RedrawMaster(nodemaster)
                            c4d.EventAdd() 
                if tester==False:
                    c4d.gui.MessageDialog("No UserData-Object connected")
            if id == ids.TMP_EYE_L:
                tester=self.checkForTarget()
                if tester==True:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                        headObj=doc.GetActiveObject()
                        if headObj is not None:
                            print "Connect Eye Left"
                            xpressoTag=self.targetLink.GetFirstTag()
                            nodemaster = xpressoTag.GetNodeMaster() #Generates xpresso nodes
                            #node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_CONDITION, insert=None, x=300, y=200) #create condition node and place in X,Y coord
                            mainNode=nodemaster.GetRoot().GetChildren()[1]
                            allOutports=mainNode.GetOutPorts()
                            node1 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_RANGEMAPPER, insert=None, x=450, y=self.ycounter) #create condition node and place in X,Y coord
                            node1[c4d.GV_RANGEMAPPER_OUTPUT_DEFS]=1
                            node1[c4d.GV_RANGEMAPPER_RANGE11]=-90
                            node1[c4d.GV_RANGEMAPPER_RANGE12]=90
                            node1[c4d.GV_RANGEMAPPER_RANGE21]=-90*(math.pi/180)
                            node1[c4d.GV_RANGEMAPPER_RANGE22]=90*(math.pi/180)
                            newNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, insert=None, x=550, y=self.ycounter) 
                            self.ycounter+=200 
                            node2 = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_RANGEMAPPER, insert=None, x=450, y=self.ycounter) #create condition node and place in X,Y coord
                            node2[c4d.GV_RANGEMAPPER_OUTPUT_DEFS]=1
                            node2[c4d.GV_RANGEMAPPER_RANGE11]=-90
                            node2[c4d.GV_RANGEMAPPER_RANGE12]=90
                            node2[c4d.GV_RANGEMAPPER_RANGE21]=-90*(math.pi/180)
                            node2[c4d.GV_RANGEMAPPER_RANGE22]=90*(math.pi/180)
                            self.ycounter+=200
                            newNode[c4d.GV_OBJECT_OBJECT_ID] = headObj
                            shapeCnt=0
                            while shapeCnt < len(allOutports):
                                if str(allOutports[shapeCnt].GetName(mainNode))=="Eye_L_Ver":
                                    newPose=newNode.AddPort(c4d.GV_PORT_INPUT, (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X)) #add a position input port to the object node
                                    allOutports[shapeCnt].Connect(node1.GetInPorts()[0])
                                    node1.GetOutPorts()[0].Connect(newPose)
                                if allOutports[shapeCnt].GetName(mainNode)=="Eye_L_Hor":
                                    newPose=newNode.AddPort(c4d.GV_PORT_INPUT, (c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Y)) #add a position input port to the object node
                                    allOutports[shapeCnt].Connect(node2.GetInPorts()[0])
                                    node2.GetOutPorts()[0].Connect(newPose)
                                shapeCnt+=1
                            c4d.modules.graphview.RedrawMaster(nodemaster)
                            c4d.EventAdd() 
                if tester==False:
                    c4d.gui.MessageDialog("No UserData-Object connected")
            if id == ids.BTN_CALIBRATE:
                print "CALIBRATE"
                exchangeData.remoteMessage=44544
                
            if id == ids.LONG_HEADPOSE:
                maindialogHelpers.setValues(self)     
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
            print "LOAD RECORDING FILE"
            exchangeData2=fileloader.main(exchangeData)
            if exchangeData2 is None:
                print "LOAD RECORDING FILE - NOT SUCCESSFULL ERROR"                
            if exchangeData2 is not None:
                exchangeData=exchangeData2
                self.SetString(ids.TXT_FRAMES2,len(exchangeData.recordetFrames))
                self.SetString(ids.TXT_SEC,str(exchangeData.doneRecTime/1000)+" s")
            if exchangeData.connected==2:
                self.Enable(ids.BTN_ADDREC,True)
            if exchangeData.connected<2:
                self.Enable(ids.BTN_ADDREC,True)
                self.Enable(ids.GRP_RECORDING,True)
                self.Enable(ids.BTN_STARTREC,False)
                self.Enable(ids.CBOX_PLAYBACK,False)
                
            print len(exchangeData.recordetFrames)
              
        maindialogHelpers.setValues(self)     
        maindialogHelpers.setUI(self)     
        return True  
    
    def checkForTarget(self):
        if self.targetLink is not None:
            xpressoTag=self.targetLink.GetFirstTag()
            if xpressoTag is not None:                
                if xpressoTag.GetType()==1001149:
                    return True
        return False
    
    def setHeadPose(self):
        if self.headPoseMode==0:
            exchangeData.remoteMessage=44944
        if self.headPoseMode==1:
            exchangeData.remoteMessage=44945
    # called on 'Close()'
    def AskClose(self):
        global exchangeData,workerThread  
        #self.renderer.End() 
        c4d.StopAllThreads()   
            
        
        return False#not c4d.gui.QuestionDialog(c4d.plugins.GeLoadString(ids.STR_TITLE))
         