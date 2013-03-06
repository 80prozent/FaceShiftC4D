import c4d
import os
from faceshiftc4d import ids
from faceshiftc4d import canvas

        
def createLayout(mainDialog):         
    global exportData,workerThread,exchangeData
    mainDialog.SetTitle(c4d.plugins.GeLoadString(ids.STR_TITLE))
        
    mainDialog.MenuFlushAll()
    
    mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_FILE))
    #mainDialog.MenuAddString(ids.MENU_FILE_CLEAR, c4d.plugins.GeLoadString(ids.MENU_FILE_CLEAR))
    #mainDialog.MenuAddString(ids.MENU_FILE_LOAD, c4d.plugins.GeLoadString(ids.MENU_FILE_LOAD))
    #mainDialog.MenuAddString(ids.MENU_FILE_SAVE, c4d.plugins.GeLoadString(ids.MENU_FILE_SAVE))
    #mainDialog.MenuAddSeparator()
    #mainDialog.MenuAddString(ids.MENU_FILE_LOADRIG, c4d.plugins.GeLoadString(ids.MENU_FILE_LOADRIG))
    #mainDialog.MenuAddString(ids.MENU_FILE_SAVERIG, c4d.plugins.GeLoadString(ids.MENU_FILE_SAVERIG))
    #mainDialog.MenuAddSeparator()
    mainDialog.MenuAddString(ids.MENU_FILE_LOADREC, c4d.plugins.GeLoadString(ids.MENU_FILE_LOADREC))
    #mainDialog.MenuAddString(ids.MENU_FILE_SAVEREC, c4d.plugins.GeLoadString(ids.MENU_FILE_SAVEREC))
    #mainDialog.MenuSubEnd()
    #mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_MAPPING))
    #mainDialog.MenuAddString(ids.MENU_MAPPING_TRAIN, c4d.plugins.GeLoadString(ids.MENU_MAPPING_TRAIN))
    #mainDialog.MenuAddString(ids.MENU_MAPPING_CONFLICTS, c4d.plugins.GeLoadString(ids.MENU_MAPPING_CONFLICTS))
    #mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_MAPPING_SHOW))
    #mainDialog.MenuAddString(ids.MENU_MAPPING_SHOW1, c4d.plugins.GeLoadString(ids.MENU_MAPPING_SHOW1))
    #mainDialog.MenuAddString(ids.MENU_MAPPING_SHOW2, c4d.plugins.GeLoadString(ids.MENU_MAPPING_SHOW2))
    #mainDialog.MenuSubEnd()
    #mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_MAPPING_SELECT))
    #mainDialog.MenuAddString(ids.MENU_MAPPING_SELECT1, c4d.plugins.GeLoadString(ids.MENU_MAPPING_SELECT1))
    #mainDialog.MenuAddString(ids.MENU_MAPPING_SELECT2, c4d.plugins.GeLoadString(ids.MENU_MAPPING_SELECT2))
    #mainDialog.MenuSubEnd()
    #mainDialog.MenuSubEnd()
    #mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_HELP))
    #mainDialog.MenuAddString(ids.MENU_HELP_HELP, c4d.plugins.GeLoadString(ids.MENU_HELP_HELP))
    #mainDialog.MenuAddString(ids.MENU_HELP_ABOUT, c4d.plugins.GeLoadString(ids.MENU_HELP_ABOUT))
    #mainDialog.MenuSubEnd()
    mainDialog.MenuFinished()
    #dialogLoadet=mainDialog.LoadDialogResource(ids.MAINDIALOG, None, flags= c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT )  
    #mainDialog.AttachUserArea(mainDialog.userarea,ids.MAINDIALOG_USERAREA, c4d.USERAREA_COREMESSAGE)
    
     
    mainDialog.ScrollGroupBegin(0,c4d.BFV_SCALEFIT|c4d.BFH_SCALEFIT,c4d.SCROLLGROUP_NOBLIT|c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_HORIZ|c4d.SCROLLGROUP_AUTOHORIZ|c4d.SCROLLGROUP_AUTOVERT,700,250)
    #Group Level 1
    mainDialog.TabGroupBegin(ids.TAB_ALL,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.TAB_TABS)
       
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_LIVESTREAM,c4d.BFH_SCALEFIT,1,2,c4d.plugins.GeLoadString(ids.TABGRP_LIVESTREAM))
	
    mainDialog.GroupBorderSpace(5, 5,5, 5)   
    
    #mainDialog.userarea1 = mainDialog.AddUserArea(ids.MAINDIALOG_USERAREA, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=260,inith=200)
    #mainDialog.AttachUserArea(mainDialog.userarea,ids.MAINDIALOG_USERAREA,c4d.USERAREA_COREMESSAGE)   
    
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_CENTER,4,1,"")
    mainDialog.GroupSpace(5,5)   
    #mainDialog.element = mainDialog.AddStaticText(ids.STR_PREVFPS ,flags=c4d.BFH_SCALEFIT|c4d.BFH_LEFT,initw=80, inith=0,name="")      
    #mainDialog.element = mainDialog.AddStaticText(ids.STR_COMBO_PREVDOC,flags=c4d.BFH_SCALE|c4d.BFH_RIGHT,initw=180, inith=0,name=c4d.plugins.GeLoadString(ids.STR_COMBO_PREVDOC)) 
    #mainDialog.element = mainDialog.AddComboBox(ids.COMBO_PREVDOC,flags=c4d.BFH_CENTER,initw=250, inith=0) 
    #mainDialog.element = mainDialog.AddStaticText(ids.STR_PREVFPS ,flags=c4d.BFH_SCALEFIT|c4d.BFH_RIGHT,initw=80, inith=0,name="") 
            #End Level 3
    mainDialog.GroupEnd()
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_CENTER,5,1,"")
    mainDialog.GroupSpace(5,5)   
    mainDialog.createButton = mainDialog.AddButton(ids.TMP_SHAPES, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.TMP_SHAPES))
    mainDialog.createButton = mainDialog.AddButton(ids.TMP_HEAD_TRANS, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.TMP_HEAD_TRANS))
    mainDialog.createButton = mainDialog.AddButton(ids.TMP_HEAD_ROT, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.TMP_HEAD_ROT))
    mainDialog.createButton = mainDialog.AddButton(ids.TMP_EYE_R, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.TMP_EYE_R))
    mainDialog.createButton = mainDialog.AddButton(ids.TMP_EYE_L, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.TMP_EYE_L))
            #End Level 3
    mainDialog.GroupEnd()
            #Group Level 3
    mainDialog.GroupBegin(ids.TABGRP_LIVESTREAM,c4d.BFH_SCALEFIT,2,2,c4d.plugins.GeLoadString(ids.TABGRP_LIVESTREAM),c4d.BFV_GRIDGROUP_EQUALCOLS|c4d.BFV_DIALOG_BAR_VERT)
	
                #Group Level 4
    mainDialog.GroupBegin(ids.GRP_NETWORK,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER,1,1,c4d.plugins.GeLoadString(ids.GRP_NETWORK))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)      
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)   
                    #Group Level 5     
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER,2,1,"")
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=12,name=c4d.plugins.GeLoadString(ids.TXT_HOST))
    mainDialog.element = mainDialog.AddEditText(ids.STRING_HOST, flags=c4d.BFH_SCALEFIT,initw=100,inith=12)
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=12,name=c4d.plugins.GeLoadString(ids.TXT_PORT))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.LONG_PORT, flags=c4d.BFH_SCALEFIT,initw=100,inith=14)
                    #End Level 5     
    mainDialog.GroupEnd()
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CONNECT, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CONNECT))
                #End Level 4     
    mainDialog.GroupEnd()
                #Group Level 4          
    mainDialog.GroupBegin(ids.GRP_FACESHIFTUSERDATA,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.GRP_FACESHIFTUSERDATA))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)        
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=2,name="")
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_ENABLE_TARGET, flags=c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_ENABLE_TARGET))
    mainDialog.linkBox=mainDialog.AddCustomGui(ids.LINK_TARGET, c4d.CUSTOMGUI_LINKBOX, "", c4d.BFH_SCALEFIT, 0, 0)
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=60,inith=3,name="")
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CREATE_TARGET, flags=c4d.BFH_SCALEFIT|c4d.BFV_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CREATE_TARGET))
                #End Level 4 
    mainDialog.GroupEnd()
                #Group Level 4 
    mainDialog.GroupBegin(ids.GRP_FACESHIFT,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.GRP_FACESHIFT)) 
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)        
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_LIVE, flags=c4d.BFH_LEFT, initw=150, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_LIVE))
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CALIBRATE, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CALIBRATE))
                    #Group Level 5 
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.AddStaticText(ids.TXT_HEADPOSE,c4d.BFH_LEFT,100,0,c4d.plugins.GeLoadString(ids.TXT_HEADPOSE),c4d.BORDER_NONE)
    mainDialog.element = mainDialog.AddComboBox(ids.LONG_HEADPOSE,flags=c4d.BFH_SCALEFIT,initw=80, inith=0) 
    mainDialog.AddChild(ids.LONG_HEADPOSE, 0, c4d.plugins.GeLoadString(ids.TXT_HEADPOSE1))
    mainDialog.AddChild(ids.LONG_HEADPOSE, 1, c4d.plugins.GeLoadString(ids.TXT_HEADPOSE2))
                    #End Level 5 
    mainDialog.GroupEnd()
                #End Level 4 
    mainDialog.GroupEnd()
        
                #Group Level 4 
    mainDialog.GroupBegin(ids.GRP_RECORDING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.GRP_RECORDING))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_STARTREC, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_STARTREC))
                    #Group Level 5     
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,3,1,"")
    mainDialog.GroupBorderSpace(0,0, 0,0)
    mainDialog.GroupSpace(0,0)       
    mainDialog.AddStaticText(ids.TXT_FRAMES,c4d.BFH_LEFT|c4d.BFH_SCALEFIT,100,0,c4d.plugins.GeLoadString(ids.TXT_FRAMES),c4d.BORDER_NONE)
    mainDialog.AddStaticText(ids.TXT_FRAMES2,c4d.BFH_LEFT|c4d.BFH_SCALEFIT,40,0,c4d.plugins.GeLoadString(ids.TXT_FRAMES2),c4d.BORDER_NONE)
    mainDialog.AddStaticText(ids.TXT_SEC,c4d.BFH_RIGHT|c4d.BFH_SCALEFIT,40,0,c4d.plugins.GeLoadString(ids.TXT_SEC),c4d.BORDER_NONE)
                    #End Level 5
    mainDialog.GroupEnd()
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_PLAYBACK, flags=c4d.BFH_SCALEFIT, initw=180, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_PLAYBACK))
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_ADDREC, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_ADDREC))
                #End Level 4
    mainDialog.GroupEnd()
            #End Level 3
    mainDialog.GroupEnd()
        #End Level 2
    mainDialog.GroupEnd()
    
    '''
    
    
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_EXPRESSIONMAPPING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,c4d.plugins.GeLoadString(ids.TABGRP_EXPRESSIONMAPPING))
            #Group Level 3
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT|c4d.SCROLLGROUP_NOBLIT,160,100)
    mainDialog.GroupBorderNoTitle(c4d.BORDER_BLACK)
    mainDialog.userarea3 = mainDialog.AddUserArea(ids.POSE_USERAREA_TARGETLIST, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=1000)
    mainDialog.AttachUserArea(mainDialog.userareaPoseList1,ids.POSE_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)  
            #End Level 3
    mainDialog.GroupEnd()
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,2,"")
                #Group Level 4
    mainDialog.TabGroupBegin(ids.TAB_EXPRESSIONMAPPING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT)
                    #Group Level 5
    mainDialog.GroupBegin(ids.TABGRP_MAPPING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,c4d.plugins.GeLoadString(ids.TABGRP_MAPPING))
                        #Group Level 6
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,2,"")
    mainDialog.userarea5 = mainDialog.AddUserArea(ids.POSE1_USERAREA_PREVIEW, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=200)
    mainDialog.AttachUserArea(mainDialog.userareaPosePrev1,ids.POSE1_USERAREA_PREVIEW,c4d.USERAREA_COREMESSAGE)  
                            #Group Level 7
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_CENTER,2,1,"")
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.element = mainDialog.AddStaticText(ids.POSE1_STR_COMBO_PREVDOC,flags=c4d.BFH_SCALE|c4d.BFH_RIGHT,initw=120, inith=0,name=c4d.plugins.GeLoadString(ids.POSE1_STR_COMBO_PREVDOC)) 
    mainDialog.element = mainDialog.AddComboBox(ids.POSE1_COMBO_PREVDOC,flags=c4d.BFH_CENTER,initw=200, inith=0) 
                            #End Level 7
    mainDialog.GroupEnd() 
                            #Group Level 7 
    mainDialog.GroupBegin(ids.POSE1_GRP_POSE,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,3,1,c4d.plugins.GeLoadString(ids.POSE1_GRP_POSE))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(10,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.POSE1_BTN_SAVE, flags=c4d.BFH_SCALEFIT,initw=80, inith=20,name=c4d.plugins.GeLoadString(ids.POSE1_BTN_SAVE))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE1_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=80, inith=20,name=c4d.plugins.GeLoadString(ids.POSE1_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE1_BTN_CLEAR, flags=c4d.BFH_SCALEFIT,initw=80, inith=20,name=c4d.plugins.GeLoadString(ids.POSE1_BTN_CLEAR)) 
                            #End Level 7 
    mainDialog.GroupEnd()
                        #End Level 6 
    mainDialog.GroupEnd()
                    #End Level 5 
    mainDialog.GroupEnd()
                    #Group Level 5
    mainDialog.GroupBegin(ids.TABGRP_POSES ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,c4d.plugins.GeLoadString(ids.TABGRP_POSES ))
                        #Group Level 6
    mainDialog.GroupBegin(ids.POSE2_SCROLLGROUP,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,"")
    mainDialog.scrollGroup=mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT|c4d.SCROLLGROUP_NOBLIT,170,100)
    mainDialog.GroupBorderNoTitle(c4d.BORDER_BLACK)
    mainDialog.userareaas3 = mainDialog.AddUserArea(ids.POSE2_USERAREA_TARGETLIST, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=170,inith=mainDialog.scrollerHeight)
    mainDialog.AttachUserArea(mainDialog.userareaPoseList2,ids.POSE2_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)  
                        #End Level 6 
    mainDialog.GroupEnd()
    mainDialog.GroupEnd()
                        #Group Level 6
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,2,"")
    mainDialog.userareasd5 = mainDialog.AddUserArea(ids.POSE2_USERAREA_PREVIEW, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=40,inith=200)
    mainDialog.AttachUserArea(mainDialog.userareaPosePrev2,ids.POSE2_USERAREA_PREVIEW,c4d.USERAREA_COREMESSAGE)   
                            #Group Level 7
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,2,2,"")
    mainDialog.GroupBorderSpace(3, 5, 3, 5)
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=100,inith=12,name=c4d.plugins.GeLoadString(ids.POSE2_STR_NAME))
    mainDialog.element = mainDialog.AddEditText(ids.POSE2_STRING_NAME, flags=c4d.BFH_SCALEFIT,initw=50,inith=12)
                            #End Level 7 
    mainDialog.GroupEnd()
                            #Group Level 7
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,3,2,"")
    mainDialog.GroupBorderSpace(3, 5, 3, 5)
    mainDialog.GroupSpace(3,3)       
    mainDialog.createButton = mainDialog.AddButton(ids.POSE2_BTN_SAVE, flags=c4d.BFH_SCALEFIT|c4d.BFH_CENTER,initw=80, inith=20,name=c4d.plugins.GeLoadString(ids.POSE2_BTN_SAVE))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE2_BTN_NEW, flags=c4d.BFH_SCALEFIT|c4d.BFH_CENTER,initw=30, inith=20,name=c4d.plugins.GeLoadString(ids.POSE2_BTN_NEW))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE2_BTN_REMOVE, flags=c4d.BFH_SCALEFIT|c4d.BFH_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE2_BTN_REMOVE))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE2_BTN_RESETSLIDERS, flags=c4d.BFH_SCALEFIT|c4d.BFH_CENTER,initw=80, inith=20,name=c4d.plugins.GeLoadString(ids.POSE2_BTN_RESETSLIDERS))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE2_BTN_RESET, flags=c4d.BFH_SCALEFIT|c4d.BFH_CENTER,initw=30, inith=20,name=c4d.plugins.GeLoadString(ids.POSE2_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE2_BTN_RECORD, flags=c4d.BFH_SCALEFIT|c4d.BFH_CENTER,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE2_BTN_RECORD))
                            #End Level 7 
    mainDialog.GroupEnd()
                        #End Level 6 
    mainDialog.GroupEnd()
                    #End Level 5
    mainDialog.GroupEnd()
    
                    #Group Level 5
    mainDialog.GroupBegin(ids.TABGRP_TARGETS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_TARGETS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                        #Group Level 6
    mainDialog.GroupBegin(0 ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,3,1,"")
                            #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_OBJECTS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_OBJECTS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                            #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,60,100)
    mainDialog.userareaas63 = mainDialog.AddUserArea(ids.POSE3_USERAREA_OBJECTS, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=60,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Objects,ids.POSE3_USERAREA_OBJECTS,c4d.USERAREA_COREMESSAGE)  
                                #End Level 8
    mainDialog.GroupEnd()
                            #End Level 7
    mainDialog.GroupEnd()
                            #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_TAGS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_TAGS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                                #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,60,100)
    mainDialog.userareaas73 = mainDialog.AddUserArea(ids.POSE3_USERAREA_TAGS, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=60,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Tags,ids.POSE3_USERAREA_TAGS,c4d.USERAREA_COREMESSAGE)  
                                #End Level 8
    mainDialog.GroupEnd()
                            #End Level 7
    mainDialog.GroupEnd()
                            #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_MATS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_MATS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                                #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,60,100)
    mainDialog.userareaas83 = mainDialog.AddUserArea(ids.POSE3_USERAREA_MATS, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=60,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Mats,ids.POSE3_USERAREA_MATS,c4d.USERAREA_COREMESSAGE) 
                                #End Level 8
    mainDialog.GroupEnd()
                            #End Level 7
    mainDialog.GroupEnd()
                        #End Level 6
    mainDialog.GroupEnd()
                        #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_ATTRIBUTES ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_ATTRIBUTES ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                                #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,180,100)
    mainDialog.userareaas93 = mainDialog.AddUserArea(ids.POSE3_USERAREA_ATTRIBUTES, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=180,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Attributes,ids.POSE3_USERAREA_ATTRIBUTES,c4d.USERAREA_COREMESSAGE)  
                                #End Level 8
    mainDialog.GroupEnd()
                        #End Level 7
    mainDialog.GroupEnd()
                    #End Level 5
    mainDialog.GroupEnd()
    
                #End Level 4
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(ids.POSE_GRP_TARGETS,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,5,1,c4d.plugins.GeLoadString(ids.POSE_GRP_TARGETS))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
    mainDialog.GroupBorderSpace(3, 5, 3, 5)
    mainDialog.GroupSpace(3,3)       
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_ADD, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_ADD))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_REMOVE, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_REMOVE)) 
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_SELECT, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_SELECT)) 
    mainDialog.element = mainDialog.AddCheckbox(ids.POSE_CBOX_RECURSIVE, flags=c4d.BFH_SCALEFIT, initw=120, inith=0, name=c4d.plugins.GeLoadString(ids.POSE_CBOX_RECURSIVE))
                #End Level 4 
    mainDialog.GroupEnd()
            #End Level 3 
    mainDialog.GroupEnd()
        #End Level 2 
    mainDialog.GroupEnd()
  
    
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_EYEMAPPING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_EYEMAPPING))    
            #Group Level 3
    mainDialog.GroupBegin(ids.TABGRP_MAPPING,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,2,c4d.plugins.GeLoadString(ids.TABGRP_MAPPING))
                #Group Level 4
    mainDialog.ScrollGroupBegin(0,c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,160,100)
    mainDialog.GroupBorderNoTitle(c4d.BORDER_BLACK)
    mainDialog.userarea43 = mainDialog.AddUserArea(ids.EYEMAP_USERAREA_TARGETLIST, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=100)
    mainDialog.AttachUserArea(mainDialog.userareaEyeMapList,ids.EYEMAP_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)  
                #End Level 4 
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,"")
    mainDialog.userareas5 = mainDialog.AddUserArea(ids.EYEMAP_USERAREA_PREVIEW, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=100)
    mainDialog.AttachUserArea(mainDialog.userareaEyeMapPrev,ids.EYEMAP_USERAREA_PREVIEW,c4d.USERAREA_COREMESSAGE)   
                #End Level 4 
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_CENTER,1,1,"")
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_SAVE, flags=c4d.BFH_SCALEFIT,initw=120, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_SAVE))
                #End Level 4 
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_CENTER,2,1,"")
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.element = mainDialog.AddStaticText(ids.POSE1_STR_COMBO_PREVDOC,flags=c4d.BFH_SCALE|c4d.BFH_RIGHT,initw=120, inith=0,name=c4d.plugins.GeLoadString(ids.POSE1_STR_COMBO_PREVDOC)) 
    mainDialog.element = mainDialog.AddComboBox(ids.EYEMAP_COMBO_PREVIEW,flags=c4d.BFH_CENTER,initw=200, inith=0) 
                #End Level 4
    mainDialog.GroupEnd() 
    
            #End Level 3 
    mainDialog.GroupEnd()
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,4,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    #mainDialog.createButton = mainDialog.AddButton(ids.BTN_RESET, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_RESET))
    #mainDialog.createButton = mainDialog.AddButton(ids.BTN_ADD, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_ADD))
    #mainDialog.createButton = mainDialog.AddButton(ids.BTN_REMOVE, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_REMOVE)) 
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_RECURSIVE, flags=c4d.BFH_CENTER, initw=120, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_RECURSIVE))
            #End Level 3
    mainDialog.GroupEnd()
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,5,2,"")
    mainDialog.GroupBorderSpace(10, 5, 10, 5)
    mainDialog.GroupSpace(20,5)       
    mainDialog.AddStaticText(0,c4d.BFH_LEFT,100,0,c4d.plugins.GeLoadString(ids.EYEMAP_STR_HORIZONTAL),c4d.BORDER_NONE)
    mainDialog.AddStaticText(ids.EYEMAP_STR_RIGHT_H,c4d.BFH_LEFT,45,0,c4d.plugins.GeLoadString(ids.EYEMAP_STR_RIGHT_H),c4d.BORDER_NONE)
    mainDialog.createButton = mainDialog.AddEditSlider(ids.EYEMAP_SLIDER_LEFT_H, flags=c4d.BFH_SCALEFIT,initw=30, inith=0) 
    mainDialog.AddStaticText(ids.EYEMAP_STR_LEFT_H,c4d.BFH_LEFT,45,0,c4d.plugins.GeLoadString(ids.EYEMAP_STR_LEFT_H),c4d.BORDER_NONE)
    mainDialog.createButton = mainDialog.AddEditSlider(ids.EYEMAP_SLIDER_LEFT_H, flags=c4d.BFH_SCALEFIT,initw=30, inith=0)
    
    mainDialog.AddStaticText(0,c4d.BFH_LEFT,100,0,c4d.plugins.GeLoadString(ids.EYEMAP_STR_VERTICAL),c4d.BORDER_NONE)
    mainDialog.AddStaticText(ids.EYEMAP_STR_RIGHT_V,c4d.BFH_LEFT,45,0,c4d.plugins.GeLoadString(ids.EYEMAP_STR_RIGHT_V),c4d.BORDER_NONE)
    mainDialog.createButton = mainDialog.AddEditSlider(ids.EYEMAP_SLIDER_LEFT_V, flags=c4d.BFH_SCALEFIT,initw=30, inith=0) 
    mainDialog.AddStaticText(ids.EYEMAP_STR_LEFT_V,c4d.BFH_LEFT,45,0,c4d.plugins.GeLoadString(ids.EYEMAP_STR_LEFT_V),c4d.BORDER_NONE) 
    mainDialog.createButton = mainDialog.AddEditSlider(ids.EYEMAP_SLIDER_LEFT_V, flags=c4d.BFH_SCALEFIT,initw=30, inith=0) 
            #End Level 3 
    mainDialog.GroupEnd() 
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,2,1,"")
                #Group Level 4
    mainDialog.GroupBegin(0 ,c4d.BFV_SCALEFIT,1,1,"")
    
                    #Group Level 5
    mainDialog.GroupBegin(ids.TABGRP_TARGETS ,c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_TARGETS ))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)  
                        #Group Level 6
    mainDialog.GroupBegin(0 ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,"")
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER,initw=120,inith=12,name=c4d.plugins.GeLoadString(ids.POSE2_STR_NAME))
    mainDialog.element = mainDialog.AddEditText(ids.POSE2_STRING_NAME, flags=c4d.BFH_SCALEFIT,initw=50,inith=12)
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_SAVE, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_SAVE))
                        #End Level 6
    mainDialog.GroupEnd()
                        #Group Level 6
    mainDialog.GroupBegin(0 ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,"")
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_CLEAR, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_CLEAR)) 
                        #End Level 6
    mainDialog.GroupEnd()
                    #End Level 5
    mainDialog.GroupEnd()
                    #Group Level 5
    mainDialog.GroupBegin(ids.TABGRP_TARGETS ,c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_TARGETS ))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                        #Group Level 6
    mainDialog.GroupBegin(0 ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,"")
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_SAVE, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_SAVE))
                       #End Level 6
    mainDialog.GroupEnd()
                        #Group Level 6
    mainDialog.GroupBegin(0 ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,"")
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.EYEMAP_BTN_CLEAR, flags=c4d.BFH_SCALEFIT,initw=50, inith=20,name=c4d.plugins.GeLoadString(ids.EYEMAP_BTN_CLEAR)) 
                        #End Level 6
    mainDialog.GroupEnd()
                    #End Level 5
    mainDialog.GroupEnd()
                #End Level 4 
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,1,1,"")
                    #Group Level 5
    mainDialog.GroupBegin(ids.TABGRP_TARGETS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_TARGETS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                        #Group Level 6
    mainDialog.GroupBegin(0 ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,3,1,"")
                            #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_OBJECTS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_OBJECTS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                            #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,60,50)
    mainDialog.userareaas63 = mainDialog.AddUserArea(ids.POSE3_USERAREA_OBJECTS, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=60,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Objects,ids.POSE3_USERAREA_OBJECTS,c4d.USERAREA_COREMESSAGE)  
                                #End Level 8
    mainDialog.GroupEnd()
                            #End Level 7
    mainDialog.GroupEnd()
                            #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_TAGS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_TAGS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                                #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,60,50)
    mainDialog.userareaas73 = mainDialog.AddUserArea(ids.POSE3_USERAREA_TAGS, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=60,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Tags,ids.POSE3_USERAREA_TAGS,c4d.USERAREA_COREMESSAGE)  
                                #End Level 8
    mainDialog.GroupEnd()
                            #End Level 7
    mainDialog.GroupEnd()
                            #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_MATS ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_MATS ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                                #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,60,50)
    mainDialog.userareaas83 = mainDialog.AddUserArea(ids.POSE3_USERAREA_MATS, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=60,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Mats,ids.POSE3_USERAREA_MATS,c4d.USERAREA_COREMESSAGE) 
                                #End Level 8
    mainDialog.GroupEnd()
                            #End Level 7
    mainDialog.GroupEnd()
                        #End Level 6
    mainDialog.GroupEnd()
                        #Group Level 7
    mainDialog.GroupBegin(ids.POSE3_GRP_ATTRIBUTES ,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.POSE3_GRP_ATTRIBUTES ))
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
                                #Group Level 8
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,180,50)
    mainDialog.userareaas93 = mainDialog.AddUserArea(ids.POSE3_USERAREA_ATTRIBUTES, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=180,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaPose3Attributes,ids.POSE3_USERAREA_ATTRIBUTES,c4d.USERAREA_COREMESSAGE)  
                                #End Level 8
    mainDialog.GroupEnd()
                        #End Level 7
    mainDialog.GroupEnd()
                    #End Level 5
    mainDialog.GroupEnd()
                    #Group Level 4
    mainDialog.GroupBegin(ids.POSE_GRP_TARGETS,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,5,1,c4d.plugins.GeLoadString(ids.POSE_GRP_TARGETS))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN)
    mainDialog.GroupBorderSpace(3, 3, 3, 3)
    mainDialog.GroupSpace(3,3)       
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_RESET, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_ADD, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_ADD))
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_REMOVE, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_REMOVE)) 
    mainDialog.createButton = mainDialog.AddButton(ids.POSE_BTN_SELECT, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.POSE_BTN_SELECT)) 
    mainDialog.element = mainDialog.AddCheckbox(ids.POSE_CBOX_RECURSIVE, flags=c4d.BFH_SCALEFIT, initw=120, inith=0, name=c4d.plugins.GeLoadString(ids.POSE_CBOX_RECURSIVE))
                    #End Level 5
    mainDialog.GroupEnd()
                #End Level 4 
    mainDialog.GroupEnd()   
            #End Level 3 
    mainDialog.GroupEnd()   
        #End Level 2 
    mainDialog.GroupEnd()
     
     
     
     
     
     
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_EYEGAZE,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_EYEGAZE))
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,"")
    mainDialog.userareaEyeMapPrev2 = mainDialog.AddUserArea(ids.EYEGAZE_USERAREA_PREVIEW, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=100)
    mainDialog.AttachUserArea(mainDialog.userareaEyeGazePrev,ids.EYEGAZE_USERAREA_PREVIEW,c4d.USERAREA_COREMESSAGE)  
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.GroupSpace(5,5)   
    mainDialog.element = mainDialog.AddStaticText(ids.STR_COMBO_PREVDOC,flags=c4d.BFH_SCALE|c4d.BFH_RIGHT,initw=150, inith=0,name=c4d.plugins.GeLoadString(ids.STR_COMBO_PREVDOC)) 
    mainDialog.element = mainDialog.AddComboBox(ids.EYEGAZE_COMBO_PREVIEW,flags=c4d.BFH_CENTER,initw=200, inith=0)      
                #End Level 4
    mainDialog.GroupEnd()    
            #End Level 3  
    mainDialog.GroupEnd() 
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,1,"")
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,4,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.EYEGAZE_BTN_RESET, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.EYEGAZE_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.EYEGAZE_BTN_ADD, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.EYEGAZE_BTN_ADD))
    mainDialog.createButton = mainDialog.AddButton(ids.EYEGAZE_BTN_REMOVE, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.EYEGAZE_BTN_REMOVE)) 
    mainDialog.element = mainDialog.AddCheckbox(ids.EYEGAZE_CBOX_ACTIVATE, flags=c4d.BFH_CENTER, initw=100, inith=0, name=c4d.plugins.GeLoadString(ids.EYEGAZE_CBOX_ACTIVATE))
                #End Level 4 
    mainDialog.GroupEnd()  
            #End Level 3
    mainDialog.GroupEnd()  
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,2,1,"")
                #Group Level 4
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,160,150)
    mainDialog.userareaEyeGazeList2 = mainDialog.AddUserArea(ids.EYEGAZE_USERAREA_TARGETLIST, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaEyeGazeList,ids.EYEGAZE_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)   
                #End Level 4
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,1,3,"")
                   #Group Level 5
    mainDialog.GroupBegin(ids.HEAD_GPR_C4DNODE,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,1,3,c4d.plugins.GeLoadString(ids.HEAD_GPR_C4DNODE))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                        #Group Level 6
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,1,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                            #Group Level 7
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,4,1,"")
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_SCALE , flags=c4d.BFH_CENTER,initw=50,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_SCALE ))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_SCALE, flags=c4d.BFH_SCALEFIT,initw=120,inith=14)
    mainDialog.element = mainDialog.AddStaticText(0 , flags=c4d.BFH_SCALEFIT,initw=0,inith=14,name="")
    mainDialog.element = mainDialog.AddStaticText(0  , flags=c4d.BFH_SCALEFIT,initw=0,inith=14,name="")
                            #End Level 7
    mainDialog.GroupEnd() 
                        #End Level 6
    mainDialog.GroupEnd() 
                        #Group Level 6
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                            #Group Level 7
    mainDialog.GroupBegin(ids.HEAD_GRP_VECTOR,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,2,c4d.plugins.GeLoadString(ids.HEAD_GRP_VECTOR  ))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_UPVECTOR  , flags=c4d.BFH_CENTER,initw=60,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_UPVECTOR  ))
    mainDialog.element = mainDialog.AddComboBox(ids.HEAD_COMBO_UPVECTOR,flags=c4d.BFH_CENTER,initw=60, inith=0) 
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_FRONTVECTOR  , flags=c4d.BFH_CENTER,initw=60,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_FRONTVECTOR  ))
    mainDialog.element = mainDialog.AddComboBox(ids.HEAD_COMBO_FRONTVECTOR,flags=c4d.BFH_CENTER,initw=60, inith=0) 
                            #End Level 7
    mainDialog.GroupEnd() 
                            #Group Level 7
    mainDialog.GroupBegin(ids.HEAD_GRP_USE,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,4,2,c4d.plugins.GeLoadString(ids.HEAD_GRP_USE  ))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_TRANSLATION   , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_TRANSLATION  ))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_TRANSLATIONX, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_TRANSLATIONX))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_TRANSLATIONY, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_TRANSLATIONY))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_TRANSLATIONZ, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_TRANSLATIONZ))
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_ROTATION   , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_ROTATION  ))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ROTATIONX, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ROTATIONX))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ROTATIONY, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ROTATIONY))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ROTATIONZ, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ROTATIONZ))
                            #End Level 7
    mainDialog.GroupEnd() 
                        #End Level 6
    mainDialog.GroupEnd() 
                   #End Level 5
    mainDialog.GroupEnd() 
                   #Group Level 5    
    mainDialog.GroupBegin(ids.HEAD_GPR_PREVIEW,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,4,2,c4d.plugins.GeLoadString(ids.HEAD_GPR_PREVIEW),c4d.BFV_BORDERGROUP_CHECKBOX)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(15, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_PREVIEWTRANS , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_PREVIEWTRANS ))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWX, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWY, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWZ, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_PREVIEWROT , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_PREVIEWROT ))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWH, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWP, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWB, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
                   #End Level 5
    mainDialog.GroupEnd() 
                   #Group Level 5    
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,2,2,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_SELECT, flags=c4d.BFH_SCALEFIT,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_SELECT))
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_RECONNECT, flags=c4d.BFH_SCALEFIT,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_RECONNECT)) 
                   #End Level 5
    mainDialog.GroupEnd() 
                #End Level 4
    mainDialog.GroupEnd() 
            #End Level 3
    mainDialog.GroupEnd()
        #End Level 2  
    mainDialog.GroupEnd()   
    
    
    
    
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_HEADPOSE,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_HEADPOSE))
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,"")
    mainDialog.userareaHeadPrev2 = mainDialog.AddUserArea(ids.HEAD_USERAREA_PREVIEW, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=150)
    mainDialog.AttachUserArea(mainDialog.userareaHeadPrev,ids.HEAD_USERAREA_PREVIEW,c4d.USERAREA_COREMESSAGE)   
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,1,"")
    mainDialog.GroupSpace(5,5)   
    mainDialog.element = mainDialog.AddStaticText(ids.STR_COMBO_PREVDOC,flags=c4d.BFH_SCALE|c4d.BFH_RIGHT,initw=150, inith=0,name=c4d.plugins.GeLoadString(ids.STR_COMBO_PREVDOC)) 
    mainDialog.element = mainDialog.AddComboBox(ids.HEAD_COMBO_PREVIEW,flags=c4d.BFH_CENTER,initw=200, inith=0)      
                #End Level 4
    mainDialog.GroupEnd()   
            #End Level 3  
    mainDialog.GroupEnd() 
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,1,"")
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,4,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_RESET, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_RESET))
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_ADD, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_ADD))
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_REMOVE, flags=c4d.BFH_CENTER,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_REMOVE)) 
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ACTIVATE, flags=c4d.BFH_CENTER, initw=100, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ACTIVATE))
                #End Level 4 
    mainDialog.GroupEnd()  
            #End Level 3
    mainDialog.GroupEnd()  
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,2,1,"")
                #Group Level 4
    mainDialog.ScrollGroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT,160,150)
    mainDialog.userareaHeadList2 = mainDialog.AddUserArea(ids.HEAD_USERAREA_TARGETLIST, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=160,inith=50)
    mainDialog.AttachUserArea(mainDialog.userareaHeadList,ids.HEAD_USERAREA_TARGETLIST,c4d.USERAREA_COREMESSAGE)   
                #End Level 4
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,1,3,"")
                   #Group Level 5
    mainDialog.GroupBegin(ids.HEAD_GPR_C4DNODE,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,1,3,c4d.plugins.GeLoadString(ids.HEAD_GPR_C4DNODE))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                        #Group Level 6
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,1,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                            #Group Level 7
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,4,1,"")
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_SCALE , flags=c4d.BFH_CENTER,initw=50,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_SCALE ))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_SCALE, flags=c4d.BFH_SCALEFIT,initw=120,inith=14)
    mainDialog.element = mainDialog.AddStaticText(0 , flags=c4d.BFH_SCALEFIT,initw=0,inith=14,name="")
    mainDialog.element = mainDialog.AddStaticText(0  , flags=c4d.BFH_SCALEFIT,initw=0,inith=14,name="")
                            #End Level 7
    mainDialog.GroupEnd() 
                        #End Level 6
    mainDialog.GroupEnd() 
                        #Group Level 6
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,1,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
                            #Group Level 7
    mainDialog.GroupBegin(ids.HEAD_GRP_VECTOR,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,2,2,c4d.plugins.GeLoadString(ids.HEAD_GRP_VECTOR  ))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_UPVECTOR  , flags=c4d.BFH_CENTER,initw=60,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_UPVECTOR  ))
    mainDialog.element = mainDialog.AddComboBox(ids.HEAD_COMBO_UPVECTOR,flags=c4d.BFH_CENTER,initw=60, inith=0) 
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_FRONTVECTOR  , flags=c4d.BFH_CENTER,initw=60,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_FRONTVECTOR  ))
    mainDialog.element = mainDialog.AddComboBox(ids.HEAD_COMBO_FRONTVECTOR,flags=c4d.BFH_CENTER,initw=60, inith=0) 
                            #End Level 7
    mainDialog.GroupEnd() 
                            #Group Level 7
    mainDialog.GroupBegin(ids.HEAD_GRP_USE,c4d.BFH_SCALEFIT|c4d.BFH_CENTER,4,2,c4d.plugins.GeLoadString(ids.HEAD_GRP_USE  ))
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_TRANSLATION   , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_TRANSLATION  ))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_TRANSLATIONX, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_TRANSLATIONX))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_TRANSLATIONY, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_TRANSLATIONY))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_TRANSLATIONZ, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_TRANSLATIONZ))
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_ROTATION   , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_ROTATION  ))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ROTATIONX, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ROTATIONX))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ROTATIONY, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ROTATIONY))
    mainDialog.element = mainDialog.AddCheckbox(ids.HEAD_CBOX_ROTATIONZ, flags=c4d.BFH_CENTER, initw=40, inith=0, name=c4d.plugins.GeLoadString(ids.HEAD_CBOX_ROTATIONZ))
                            #End Level 7
    mainDialog.GroupEnd() 
                        #End Level 6
    mainDialog.GroupEnd() 
                   #End Level 5
    mainDialog.GroupEnd() 
                   #Group Level 5    
    mainDialog.GroupBegin(ids.HEAD_GPR_PREVIEW,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,4,2,c4d.plugins.GeLoadString(ids.HEAD_GPR_PREVIEW),c4d.BFV_BORDERGROUP_CHECKBOX)
    mainDialog.GroupBorder(c4d.BORDER_THIN_IN) 
    mainDialog.GroupBorderSpace(15, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_PREVIEWTRANS , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_PREVIEWTRANS ))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWX, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWY, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWZ, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddStaticText(ids.HEAD_STR_PREVIEWROT , flags=c4d.BFH_CENTER,initw=90,inith=14,name=c4d.plugins.GeLoadString(ids.HEAD_STR_PREVIEWROT ))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWH, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWP, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.HEAD_STEPPER_PREVIEWB, flags=c4d.BFH_SCALEFIT,initw=50,inith=14)
                   #End Level 5
    mainDialog.GroupEnd() 
                   #Group Level 5    
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT|c4d.BFH_CENTER|c4d.BFV_SCALEFIT,2,2,"")
    mainDialog.GroupBorderSpace(5, 5, 5, 5)
    mainDialog.GroupSpace(5,5)       
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_SELECT, flags=c4d.BFH_SCALEFIT,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_SELECT))
    mainDialog.createButton = mainDialog.AddButton(ids.HEAD_BTN_RECONNECT, flags=c4d.BFH_SCALEFIT,initw=60, inith=20,name=c4d.plugins.GeLoadString(ids.HEAD_BTN_RECONNECT)) 
                   #End Level 5
    mainDialog.GroupEnd() 
                #End Level 4
    mainDialog.GroupEnd() 
            #End Level 3
    mainDialog.GroupEnd() 
        #End Level 2    
    mainDialog.GroupEnd()
    '''
     
    #End Level 1     
    mainDialog.GroupEnd()
    #End Level 1     
    mainDialog.GroupEnd()
       