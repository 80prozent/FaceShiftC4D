import c4d
import os
from faceshiftc4d import ids
from faceshiftc4d import canvas
from faceshiftc4d import faceshiftparser
from faceshiftc4d import faceShiftData

        
def createLayout(mainDialog):         
    global exportData,workerThread,exchangeData
    mainDialog.SetTitle(c4d.plugins.GeLoadString(ids.STR_TITLE))
        
    mainDialog.MenuFlushAll()
    mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_FILE))
    mainDialog.MenuAddString(ids.MENU_FILE_CLEAR, c4d.plugins.GeLoadString(ids.MENU_FILE_CLEAR))
    mainDialog.MenuAddString(ids.MENU_FILE_LOAD, c4d.plugins.GeLoadString(ids.MENU_FILE_LOAD))
    mainDialog.MenuAddString(ids.MENU_FILE_SAVE, c4d.plugins.GeLoadString(ids.MENU_FILE_SAVE))
    mainDialog.MenuAddSeparator()
    mainDialog.MenuAddString(ids.MENU_FILE_LOADRIG, c4d.plugins.GeLoadString(ids.MENU_FILE_LOADRIG))
    mainDialog.MenuAddString(ids.MENU_FILE_SAVERIG, c4d.plugins.GeLoadString(ids.MENU_FILE_SAVERIG))
    mainDialog.MenuAddSeparator()
    mainDialog.MenuAddString(ids.MENU_FILE_LOADREC, c4d.plugins.GeLoadString(ids.MENU_FILE_LOADREC))
    mainDialog.MenuAddString(ids.MENU_FILE_SAVEREC, c4d.plugins.GeLoadString(ids.MENU_FILE_SAVEREC))
    mainDialog.MenuSubEnd()
    mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_HELP))
    mainDialog.MenuAddString(ids.MENU_HELP_HELP, c4d.plugins.GeLoadString(ids.MENU_HELP_HELP))
    mainDialog.MenuAddString(ids.MENU_HELP_ABOUT, c4d.plugins.GeLoadString(ids.MENU_HELP_ABOUT))
    mainDialog.MenuSubEnd()
    mainDialog.MenuFinished()
    mainDialog.Enable(ids.MENU_FILE_CLEAR,False)
    mainDialog.Enable(ids.MENU_FILE_LOAD,False)
    mainDialog.Enable(ids.MENU_FILE_SAVE,False)
    mainDialog.Enable(ids.MENU_FILE_LOADRIG,False)
    mainDialog.Enable(ids.MENU_FILE_SAVERIG,False)
    mainDialog.Enable(ids.MENU_FILE_LOADREC,True)
    mainDialog.Enable(ids.MENU_FILE_SAVEREC,False)
    #dialogLoadet=mainDialog.LoadDialogResource(ids.MAINDIALOG, None, flags= c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT )  
    #mainDialog.AttachUserArea(mainDialog.userarea,ids.MAINDIALOG_USERAREA, c4d.USERAREA_COREMESSAGE)
          
    
    mainDialog.TabGroupBegin(ids.TAB_ALL,c4d.TAB_TABS)
       
    mainDialog.GroupBegin(ids.TABGRP_LIVESTREAM,c4d.BFH_SCALEFIT,1,2,c4d.plugins.GeLoadString(ids.TABGRP_LIVESTREAM))
	
    mainDialog.GroupBorderSpace(5, 5,5, 5)
    
    
    mainDialog.userarea1 = mainDialog.AddUserArea(ids.MAINDIALOG_USERAREA, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=260,inith=200)
    mainDialog.AttachUserArea(mainDialog.userarea,ids.MAINDIALOG_USERAREA,c4d.USERAREA_COREMESSAGE)   
    
    mainDialog.GroupBegin(ids.TABGRP_LIVESTREAM,c4d.BFH_SCALEFIT,2,2,c4d.plugins.GeLoadString(ids.TABGRP_LIVESTREAM),c4d.BFV_GRIDGROUP_EQUALCOLS|c4d.BFV_DIALOG_BAR_VERT)
	
    mainDialog.GroupBegin(ids.GRP_NETWORK,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER,1,1,c4d.plugins.GeLoadString(ids.GRP_NETWORK))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)      
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)        
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER,2,1,"")
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=12,name=c4d.plugins.GeLoadString(ids.TXT_HOST))
    mainDialog.element = mainDialog.AddEditText(ids.STRING_HOST, flags=c4d.BFH_SCALEFIT,initw=100,inith=12)
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=12,name=c4d.plugins.GeLoadString(ids.TXT_PORT))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.LONG_PORT, flags=c4d.BFH_SCALEFIT,initw=100,inith=14)
    mainDialog.GroupEnd()
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CONNECT, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CONNECT))
    mainDialog.GroupEnd()
        
    mainDialog.GroupBegin(ids.GRP_FACESHIFTUSERDATA,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.GRP_FACESHIFTUSERDATA))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)        
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=2,name="")
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_ENABLE_TARGET, flags=c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_ENABLE_TARGET))
    mainDialog.linkBox=mainDialog.AddCustomGui(ids.LINK_TARGET, c4d.CUSTOMGUI_LINKBOX, "", c4d.BFH_SCALEFIT, 0, 0)
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=3,name="")
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CREATE_TARGET, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CREATE_TARGET))
    mainDialog.GroupEnd()
       
    mainDialog.GroupBegin(ids.GRP_FACESHIFT,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.GRP_FACESHIFT)) 
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)        
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_LIVE, flags=c4d.BFH_LEFT, initw=150, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_LIVE))
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CALIBRATE, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CALIBRATE))
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.AddStaticText(ids.TXT_HEADPOSE,c4d.BFH_LEFT,100,0,c4d.plugins.GeLoadString(ids.TXT_HEADPOSE),c4d.BORDER_NONE)
    mainDialog.element = mainDialog.AddComboBox(ids.LONG_HEADPOSE,flags=c4d.BFH_SCALEFIT,initw=80, inith=0) 
    mainDialog.AddChild(ids.LONG_HEADPOSE, 0, c4d.plugins.GeLoadString(ids.TXT_HEADPOSE1))
    mainDialog.AddChild(ids.LONG_HEADPOSE, 1, c4d.plugins.GeLoadString(ids.TXT_HEADPOSE2))
    mainDialog.GroupEnd()
    mainDialog.GroupEnd()
        
    mainDialog.GroupBegin(ids.GRP_RECORDING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.GRP_RECORDING))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_STARTREC, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_STARTREC))
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,3,1,"")
    mainDialog.GroupBorderSpace(0,0, 0,0)
    mainDialog.GroupSpace(0,0)       
    mainDialog.AddStaticText(ids.TXT_FRAMES,c4d.BFH_LEFT|c4d.BFH_SCALEFIT,100,0,c4d.plugins.GeLoadString(ids.TXT_FRAMES),c4d.BORDER_NONE)
    mainDialog.AddStaticText(ids.TXT_FRAMES2,c4d.BFH_LEFT|c4d.BFH_SCALEFIT,40,0,c4d.plugins.GeLoadString(ids.TXT_FRAMES2),c4d.BORDER_NONE)
    mainDialog.AddStaticText(ids.TXT_SEC,c4d.BFH_RIGHT|c4d.BFH_SCALEFIT,40,0,c4d.plugins.GeLoadString(ids.TXT_SEC),c4d.BORDER_NONE)
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_PLAYBACK, flags=c4d.BFH_SCALEFIT, initw=180, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_PLAYBACK))
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_ADDREC, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_ADDREC))
    mainDialog.GroupEnd()
    mainDialog.GroupEnd()
    mainDialog.GroupEnd()
        
    #mainDialog.GroupBegin(ids.GRP_FILTER,c4d.BFH_SCALE,2,2,"Mapping",c4d.BFV_GRIDGROUP_EQUALCOLS)
    #mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
    #mainDialog.GroupEnd()
    mainDialog.GroupEnd()
             
        