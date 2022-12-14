# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from config import ConfigFile
from gui.uis.openmarkets.kakaologin import Kakao
from gui.uis.openmarkets.naverlogin import Naver
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget

from .functions_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *
from ....db.conndb import SqliteDb
from gui.uis.pages.ui_main_pages import Ui_MainPages
# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *
from .setup_table_window import *
from .defpyqt import DefPyQt

import datetime
# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .adduserwidget import Ui_Form
from loginsession.logincheck import LoginSessionManageMent

class AddUserPage:
    def __init__(self,parent=None):
        super().__init__()
        self.uip = Ui_MainPages()
        self.parent = parent
        self.config = ConfigFile()
        self.application_path = self.config.read()['system']['dir']
        self.naver =  Naver()
        self.kakao =  Kakao()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        # self.uid.setup_ui(self)
        settings = Settings()
        self.settings = settings.items
        self.default = DefPyQt()
        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items
     

        result = SqliteDb().selectSqlData('ShoppingMallAccountList')
        self.myTableWidget = SetupTableWindow(result,parent=self)

        self.fuck = 'fuck'



        # ???????????? ???????????? ??????
        # PUSH BUTTON 2
        self.addUserPushButton = PyPushButton(
            text = "???????????? ??????",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_add_user.svg"))
        self.addUserPushButton.setMinimumHeight(40)
        self.addUserPushButton.setIcon(self.icon_2)

        self.addUserPushButton.clicked.connect(self.adduserbutton)
        

        # ???????????? ???????????? ??????
        # PUSH BUTTON 2
        self.excelDownPushButton = PyPushButton(
            text = "?????? ????????????",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_add_user.svg"))
        self.excelDownPushButton.setMinimumHeight(40)
        self.excelDownPushButton.setIcon(self.icon_2)

        # self.excelDownPushButton.clicked.connect(self.exceldownloadbutton)
        
        
        # ????????? ???????????? ??????
        # PUSH BUTTON 2
        self.syncPushButton = PyPushButton(
            text = "????????????",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_refresh.svg"))
        self.syncPushButton.setMinimumHeight(40)
        self.syncPushButton.setIcon(self.icon_2)

        self.syncPushButton.clicked.connect(self.syncAddUserPageTable)
        
        #### TABLE SETTING ####
    
        # companies = ('Apple', 'Facebook', 'Google', 'Amazon', 'Walmart', 'Dropbox', 'Starbucks', 'eBay', 'Canon')
        # model = QStandardItemModel(len(companies), 1)
        # model.setHorizontalHeaderLabels(['Company'])

        # for row, company in enumerate(companies):
        #     item = QStandardItem(company)
        #     model.setItem(row, 0, item)

        # filter_proxy_model = QSortFilterProxyModel()
        # filter_proxy_model.setSourceModel(model)
        # filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # filter_proxy_model.setFilterKeyColumn(0)
    def ComboValue(self):
        if (self.widget.selectloginTypeList.currentText()) == '?????????':
            self.widget.groupBox_4.show()
        # print('????????? ?????????')

    def twostepauthpushButton(self):
        print('2????????? ??????')
        info = {}
        info['emailId'] = self.widget.emailIdLineEdit.text()
        info['emailPass'] = self.widget.emailPassLineEdit_3.text()
        info['loginId'] = self.widget.loginIdLineEdit.text()
        info['loginPass'] = self.widget.loginPassLineEdit.text()

        if info['emailId'] != '' or info['emailPass'] != '':
            if 'naver.com' in info['emailId'] :
                print('????????? ????????????')

                kakaores = self.kakao.login(info,value=True)
                print(kakaores)
                print('@@@',info['emailId'])
                if kakaores['email'][:2] != info['emailId'][:2]:
                    self.default.showMessageBoxs('2????????? ??????',f'?????????????????? 2????????? ???????????? ???????????? ???????????????????????? ????????????. ???????????????2????????????????????? ???????????? ?????? ??? ??????????????????..\n?????? ????????? ????????? : {info["emailId"]}')
                    return False

                if self.naver.login(info,twostep=True):
                    self.default.showMessageBoxs('2????????? ??????','??????????????? ????????? ???????????????.')
                else:
                    self.default.showMessageBoxs('2????????? ??????','???????????? ??????????????? ??????????????????. ?????? 2????????? ?????? ????????????.')
            else:
                self.default.showMessageBoxs('2????????? ????????????','????????? ????????? ???????????? ???????????????. ???????????????2????????????????????? 2????????? ???????????? ?????? ??? ??????????????????.')

        else:
            self.default.showMessageBoxs('2????????? ????????????','??????????????????.')

    def closeBtnClickInAddUserPage(self):
        print('??????')
        self.Form.close()

    def tryLoginBtnClickInAddUserPage(self,info):
        print('????????? ????????? ?????? ????????????')
        info = {
            'isAuth':'True',
            'groupId':'',
            'mallName':self.widget.selectmallNameList.currentText().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'loginType':self.widget.selectloginTypeList.currentText().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'loginId':self.widget.loginIdLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'loginPass':self.widget.loginPassLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'nickName':self.widget.nickNameLineEdit.text(),
            'emailId':self.widget.emailIdLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'emailPass':self.widget.emailPassLineEdit_3.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            # 'updateDate': datetime.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'memo':self.widget.textEdit.toPlainText(),
        }
        # info  = {'isAuth': 'True', 'groupId': '', 'mallName': '??????', 'loginType': '?????????', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '?????????','emailId':'','emailPass':''}
        # info  = {'isAuth': 'True', 'groupId': '', 'mallName': '??????', 'loginType': '?????????', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '?????????','emailId':'kys053123@naver.com','emailPass':'fkaustkfl123!'}
        if info['mallName'] == '????????? ??????': self.default.showMessageBoxs('?????? ??????',f'????????? ????????? ????????????.'); return False
        if info['loginId'] == '': self.default.showMessageBoxs('?????? ??????',f'????????? ???????????? ??????????????????.'); return False
        if info['loginPass'] == '': self.default.showMessageBoxs('?????? ??????',f'????????? ??????????????? ??????????????????.'); return False
        if info['loginType'] == '?????????' and info['emailId'] == '': self.default.showMessageBoxs('2????????? ?????? ??????','???????????? ????????? ?????????????????? ????????? ???????????????.'); return False

        print('?????? ????????? :',info)
        print(info)
        info['cookiename']= os.path.join(self.application_path,'COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
        self.info = info
        
        self.login = LoginSessionManageMent(self,info=info,onlycheck=True)
        self.login.start()
        self.login.wait()
        print(self.login.login_res)
        if self.login.login_res == None: 
            self.widget.saveBtn.setEnabled(True)
            self.default.showMessageBoxs('????????? ??????',f'??????????????? ?????????????????? ??????????????????.')
            return

        self.default.showMessageBoxs('????????? ????????? ??????',self.login.login_res['msg'])
        self.widget.saveBtn.setEnabled(True)
        if self.login.login_res['result']:
            print('?????? - ????????? ?????? ?????? ????????? ???????????????.')
            self.login = LoginSessionManageMent(self,info=info)
            self.login.start()

    def updateBtnClickInAddUserPage(self):
        print('?????? ??????')
        info = {
            'isAuth':'True',
            'groupId':'',
            'mallName':self.widget.selectmallNameList.currentText().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'loginType':self.widget.selectloginTypeList.currentText().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'loginId':self.widget.loginIdLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'loginPass':self.widget.loginPassLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'nickName':self.widget.nickNameLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'emailId':self.widget.emailIdLineEdit.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            'emailPass':self.widget.emailPassLineEdit_3.text().rstrip().lstrip().replace('\t','').replace('\n','').replace('\r',''),
            # 'updateDate': datetime.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'memo':self.widget.textEdit.toPlainText(),
        }
        print(info)
        index = self.dbdata[0]

        print(self.dbdata)
        self.sql = SqliteDb()

        query = f'''UPDATE ShoppingMallAccountList
        SET 'mallName' = '{self.widget.selectmallNameList.currentText()}',
        'loginType' = '{self.widget.selectloginTypeList.currentText()}', 
        'loginId' = '{self.widget.loginIdLineEdit.text()}', 
        'loginPass' = '{self.widget.loginPassLineEdit.text()}', 
        'nickName' = '{self.widget.nickNameLineEdit.text()}', 
        'emailId' = '{self.widget.emailIdLineEdit.text()}', 
        'emailPass' = '{self.widget.emailPassLineEdit_3.text()}', 
        'memo' = '{self.widget.textEdit.toPlainText()}' WHERE id={index}
        '''
        self.sql.dbquery(query)
        
        self.default.showMessageBoxs('????????????','?????????????????????.')
        # ????????? ?????????
        self.syncAddUserPageTable()
        self.Form.close()
        
    def saveBtnClickInAddUserPage(self):
        print('??????')
        # res = {
        #     'isAuth':'False',
        #     'groupId':'1???????????????',
        #     'mallName':'??????',
        #     'loginType':'?????????',
        #     'loginId':'ybbang0202@naver.com',
        #     'loginPass':'pchw1103',
        #     'emailId':'ybbang0202@naver.com',
        #     'emailPass':'3dlscldtlwja@',
        #     'nickName':'fuck',
        #     'memo':'??????',
        # }
        # ???????????? ???????????????.
        try:
            SqliteDb().insertSqlData(self.info,'ShoppingMallAccountList')
        except AttributeError as e:
            self.default.showMessageBoxs('????????????',f'{e}\n????????? ????????? ??? ??????????????????.')
            return False

        self.default.showMessageBoxs('????????????','?????????????????????.')

        # ????????? ?????????
        self.syncAddUserPageTable()

        self.Form.close()

    def syncAddUserPageTable(self):
        # ????????? ???????????? ???????????????.
        self.newtable = SetupTableWindow(SqliteDb().selectSqlData('ShoppingMallAccountList'),parent=self)
        # ???????????? ???????????? ?????????
        for i in reversed(range(self.parent.ui.load_pages.verticalLayout_2.count())): 
            self.parent.ui.load_pages.verticalLayout_2.itemAt(i).widget().setParent(None)
        # ???????????? ?????? ?????????
        self.parent.ui.load_pages.verticalLayout_2.addWidget(self.newtable.table_widget)
        print('???????????? ??????')
        
    def updateMallNameListCombo(self,index):
        self.widget.selectloginTypeList.clear()
        items = self.widget.selectmallNameList.itemData(index)
        if items:
            self.widget.selectloginTypeList.addItems(items)



    # def deletebtn(self):
    #     print('????????????')
    #     self.adduserbutton()
    #     self.Form.setWindowTitle('????????? ?????? ??????')

    #     button = self.parent.ui.sender()
    #     button = self.parent.sender()
    #     # if button:
    #     item = self.table_widget.indexAt(button.pos()).row()
    #     print(item.row())      
    #     # mallproductid = ( self.ranktrackingtableWidget.item( item.row(),12 ).text()  )

    def adduserbutton(self,data=False):
        
        print('????????????')
        self.fuck = '??????'
        self.r = {
            'mallNameList':[
                ('????????? ??????','??????????????? ??????'),
                ('???????????????','?????????'),
                # ('??????','??????'),
                ('?????????','?????????,?????????'),
                ('??????','??????,?????????'),
                # ('SSG','SSG,?????????'),
                ('11??????','11??????,?????????'),
                ('??????','??????'),
                ('?????????','?????????'),
                ('?????????','?????????,?????????'),
                
                # ('????????????','????????????'),
                
                ],
            # 'loginTypeList':['??????','?????????']
            }

        self.Form = QWidget()
        self.widget = Ui_Form()
        # qtmodern.styles.dark(self.widget)
        self.widget.setupUi(self.Form)
        # self.Form = qtmodern.windows.ModernWindow(self.widget)
        self.Form.show()

        self.Form.setWindowTitle('????????? ?????? ??????')
        
        # ????????????
        self.widget.groupBox_4.hide()
        self.widget.saveBtn.setEnabled(False)
        # ????????? ??????
        self.Form.setStyleSheet(Themes().customWidget())

        self.widget.selectmallNameList.currentIndexChanged.connect(self.updateMallNameListCombo)
        self.updateMallNameListCombo(self.widget.selectloginTypeList.currentIndex())
        for mallName in self.r['mallNameList']:
            # print(mallName[0],mallName[1].split(','))
            self.widget.selectmallNameList.addItem(mallName[0],mallName[1].split(','))
        
        self.widget.tryloginBtn.clicked.connect(self.tryLoginBtnClickInAddUserPage)
        if data: # ?????? ?????????
            self.dbdata = data
            self.widget.saveBtn.clicked.connect(self.updateBtnClickInAddUserPage)
        else:    
            self.widget.saveBtn.clicked.connect(self.saveBtnClickInAddUserPage)

        self.widget.closeBtn.clicked.connect(self.closeBtnClickInAddUserPage)
        self.widget.pushButton.clicked.connect(self.twostepauthpushButton) # 2???????????????
        self.widget.selectloginTypeList.activated.connect(self.ComboValue)
        # print(self.widget.saveBtn.text())
#         # self.Form.setStyleSheet(stylesheet)
#         # self.Form.setStyleSheet(f"""
#         # background: "{self.themes['app_color']['bg_two']}";
#         # font: {self.settings["font"]["text_size"]}pt "{self.settings["font"]["family"]}";
#         # """)

#         # self.


#         # PY LINE EDIT
#         self.loginIdLineEdit = PyLineEdit(
#             text = "",
#             place_holder_text = "????????? ???????????? ??????????????? :",
#             radius = 8,
#             border_size = 2,
#             color = self.themes["app_color"]["text_foreground"],
#             selection_color = self.themes["app_color"]["white"],
#             bg_color = self.themes["app_color"]["dark_one"],
#             bg_color_active = self.themes["app_color"]["dark_three"],
#             context_color = self.themes["app_color"]["context_color"],
#             bold='bold'
#         )

#         self.loginIdLineEdit.setMinimumHeight(30)
#         # PY LINE EDIT
#         self.loginPassLineEdit = PyLineEdit(
#             text = "",
#             place_holder_text = "????????? ??????????????? ??????????????? :",
#             radius = 8,
#             border_size = 2,
#             color = self.themes["app_color"]["text_foreground"],
#             selection_color = self.themes["app_color"]["white"],
#             bg_color = self.themes["app_color"]["dark_one"],
#             bg_color_active = self.themes["app_color"]["dark_three"],
#             context_color = self.themes["app_color"]["context_color"],
#             bold='bold'
#         )

#         self.loginPassLineEdit.setMinimumHeight(30)
#         self.nickNameLineEdit = PyLineEdit(
#             text = "",
#             place_holder_text = "???????????? ????????? ???????????? ??????????????? :",
#             radius = 8,
#             border_size = 2,
#             color = self.themes["app_color"]["text_foreground"],
#             selection_color = self.themes["app_color"]["white"],
#             bg_color = self.themes["app_color"]["dark_one"],
#             bg_color_active = self.themes["app_color"]["dark_three"],
#             context_color = self.themes["app_color"]["context_color"],
#             bold='bold'
#         )

#         self.nickNameLineEdit.setMinimumHeight(30)
        
#         self.selectmallNameList = QComboBox()
#         self.selectmallNameList.setStyleSheet(f"""
#             color:{self.themes["app_color"]["text_foreground"]};
#             background-color: {self.themes["app_color"]["dark_one"]}; 
#             border-radius: 8px;
#             padding: 8px;
#             font-weight: bold;
#         """)
        
#         for mallName in self.r['mallNameList']:
#             # print(mallName[0],mallName[1].split(','))
#             self.selectmallNameList.addItem(mallName[0],mallName[1].split(','))
        
#         self.selectloginTypelist = QComboBox()
#         self.selectloginTypelist.setStyleSheet(f"""
#             color:{self.themes["app_color"]["text_foreground"]};
#             background-color: {self.themes["app_color"]["dark_one"]}; 
#             border-radius: 8px;
#             padding: 8px;
#             font-weight: bold;
#         """)
#         self.selectloginTypelist.addItem('????????? ?????? ??????')
#         self.selectmallNameList.currentIndexChanged.connect(self.updateMallNameListCombo)
#         self.updateMallNameListCombo(self.selectloginTypelist.currentIndex())
#         # for logintype in self.r['loginTypeList']:
#         #     self.selectloginTypelist.addItem(logintype)
#         # 
#         # BTN 1
#         self.saveBtn = PyPushButton(
#             text="??? ???",
#             radius=8,
#             color=self.themes["app_color"]["text_foreground"],
#             bg_color=self.themes["app_color"]["dark_one"],
#             bg_color_hover=self.themes["app_color"]["dark_three"],
#             bg_color_pressed=self.themes["app_color"]["dark_four"]
#         )
#         self.saveBtn.setMaximumHeight(40)

#         self.tryloginBtn = PyPushButton(
#             text="????????? ??????",
#             radius=8,
#             color=self.themes["app_color"]["text_foreground"],
#             bg_color=self.themes["app_color"]["dark_one"],
#             bg_color_hover=self.themes["app_color"]["dark_three"],
#             bg_color_pressed=self.themes["app_color"]["dark_four"]
#         )
#         self.tryloginBtn.setMaximumHeight(40)

#         self.closeBtn = PyPushButton(
#             text="??? ???",
#             radius=8,
#             color=self.themes["app_color"]["text_foreground"],
#             bg_color=self.themes["app_color"]["dark_one"],
#             bg_color_hover=self.themes["app_color"]["dark_three"],
#             bg_color_pressed=self.themes["app_color"]["dark_four"]
#         )
#         # self.closeBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.closeBtn.setMaximumHeight(40)
#         self.closeBtn.setMaximumWidth(100)

#         # self.widget.verticalLayout.setContentsMargins(3,3,3,3)
#         # self.widget.verticalLayout.setSpacing(6)
        
#         # main_layout = QFormLayout()

#         # shoppingmallselectbox = QHBoxLayout()
#         # shoppingmallselectbox.addWidget(self.selectmallNameList)
#         # shoppingmallselectbox.addWidget(self.selectloginTypelist)
#         # self.widget.verticalLayout.addRow('????????? ?????? :',shoppingmallselectbox)
#         # # self.widget.verticalLayout.addStretch(1)
#         # self.widget.verticalLayout.addRow('????????? ????????? :',self.nickNameLineEdit)
#         # self.widget.verticalLayout.addRow('????????? :',self.loginIdLineEdit)
#         # self.widget.verticalLayout.addRow('???????????? :',self.loginPassLineEdit)

#         # pushbuttons=QVBoxLayout()
#         # pushbuttons.addWidget(self.tryloginBtn)
#         # pushbuttons.addWidget(self.saveBtn)
#         # pushbuttons.addWidget(self.closeBtn)
#         # self.widget.verticalLayout.addRow(pushbuttons)
        
#         # self.label =QLabel('?????? ??????')
# #         self.widget.verticalLayout.addWidget(self.label)
# # # 
# #         self.widget.verticalLayout.addWidget(self.selectmallNameList)
#         # self.widget.verticalLayout.addWidget(self.selectloginTypelist)
#         # self.widget.verticalLayout.addStretch(1)
#         # self.widget.verticalLayout.addWidget(self.loginIdLineEdit)
#         # self.widget.verticalLayout.addWidget(self.loginPassLineEdit)
#         # self.widget.verticalLayout.addWidget(self.nickNameLineEdit)
#         # self.widget.verticalLayout.addStretch(1)
#         # self.memo = QTextEdit()
#         # self.widget.verticalLayout.addWidget(self.memo)
#         # self.widget.verticalLayout.addStretch(1)
#         # self.widget.verticalLayout.addWidget(self.tryloginBtn)
#         # self.widget.verticalLayout.addWidget(self.saveBtn)
#         # self.widget.verticalLayout.addWidget(self.closeBtn)

#         # self.tryloginBtn.clicked.connect(self.tryLoginBtnClickInAddUserPage)
#         # self.saveBtn.clicked.connect(self.saveBtnClickInAddUserPage)
#         # self.closeBtn.clicked.connect(self.closeBtnClickInAddUserPage)

#         # self.FormsetStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
#         # self.widget.verticalLayoutWidget = QVBoxLayout(self.widget.verticalLayoutWidget)
#         # if self.settings["custom_title_bar"]:
#         #     self.widget.verticalLayoutWidget.setContentsMargins(10,10,10,10)
#         # else:
#         #     self.widget.verticalLayoutWidget.setContentsMargins(0,0,0,0)


        
