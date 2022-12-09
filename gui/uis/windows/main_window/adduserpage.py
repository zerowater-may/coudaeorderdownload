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



        # 계정정보 추가하기 버튼
        # PUSH BUTTON 2
        self.addUserPushButton = PyPushButton(
            text = "계정정보 추가",
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
        

        # 계정정보 추가하기 버튼
        # PUSH BUTTON 2
        self.excelDownPushButton = PyPushButton(
            text = "엑셀 다운로드",
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
        
        
        # 동기화 추가하기 버튼
        # PUSH BUTTON 2
        self.syncPushButton = PyPushButton(
            text = "새로고침",
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
        if (self.widget.selectloginTypeList.currentText()) == '카카오':
            self.widget.groupBox_4.show()
        # print('커런트 텍스트')

    def twostepauthpushButton(self):
        print('2차인증 버튼')
        info = {}
        info['emailId'] = self.widget.emailIdLineEdit.text()
        info['emailPass'] = self.widget.emailPassLineEdit_3.text()
        info['loginId'] = self.widget.loginIdLineEdit.text()
        info['loginPass'] = self.widget.loginPassLineEdit.text()

        if info['emailId'] != '' or info['emailPass'] != '':
            if 'naver.com' in info['emailId'] :
                print('이메일 검증하기')

                kakaores = self.kakao.login(info,value=True)
                print(kakaores)
                print('@@@',info['emailId'])
                if kakaores['email'][:2] != info['emailId'][:2]:
                    self.default.showMessageBoxs('2차인증 실패',f'카카오계정의 2차인증 이메일과 입력하신 이메일계정정보가 다릅니다. 카카오계정2차인증설정에서 이메일을 교체 후 시도해주세요..\n현재 카카오 이메일 : {info["emailId"]}')
                    return False

                if self.naver.login(info,twostep=True):
                    self.default.showMessageBoxs('2차인증 성공','정상적으로 로그인 되었습니다.')
                else:
                    self.default.showMessageBoxs('2차인증 실패','아이디나 비밀번호를 확인해주세요. 또는 2차인증 해제 해주세요.')
            else:
                self.default.showMessageBoxs('2차인증 입력오류','현재는 네이버 이메일만 가능합니다. 카카오계정2차인증설정에서 2차인증 이메일을 교체 후 시도해주세요.')

        else:
            self.default.showMessageBoxs('2차인증 입력오류','확인해주세요.')

    def closeBtnClickInAddUserPage(self):
        print('닫기')
        self.Form.close()

    def tryLoginBtnClickInAddUserPage(self,info):
        print('로그인 쓰레드 시작 정보받고')
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
        # info  = {'isAuth': 'True', 'groupId': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '메모장','emailId':'','emailPass':''}
        # info  = {'isAuth': 'True', 'groupId': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '메모장','emailId':'kys053123@naver.com','emailPass':'fkaustkfl123!'}
        if info['mallName'] == '쇼핑몰 선택': self.default.showMessageBoxs('입력 오류',f'쇼핑몰 선택을 해주세요.'); return False
        if info['loginId'] == '': self.default.showMessageBoxs('입력 오류',f'로그인 아이디를 입력해주세요.'); return False
        if info['loginPass'] == '': self.default.showMessageBoxs('입력 오류',f'로그인 비밀번호를 입력해주세요.'); return False
        if info['loginType'] == '카카오' and info['emailId'] == '': self.default.showMessageBoxs('2차인증 정보 입력','카카오에 등록된 네이버이메일 계정을 입력하세요.'); return False

        print('리얼 데이터 :',info)
        print(info)
        info['cookiename']= os.path.join(self.application_path,'COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
        self.info = info
        
        self.login = LoginSessionManageMent(self,info=info,onlycheck=True)
        self.login.start()
        self.login.wait()
        print(self.login.login_res)
        if self.login.login_res == None: 
            self.widget.saveBtn.setEnabled(True)
            self.default.showMessageBoxs('테스트 완료',f'정상적으로 작성하셨다면 저장해주세요.')
            return

        self.default.showMessageBoxs('로그인 테스트 결과',self.login.login_res['msg'])
        self.widget.saveBtn.setEnabled(True)
        if self.login.login_res['result']:
            print('바깥 - 로그인 성공 실제 로그인 실행합니다.')
            self.login = LoginSessionManageMent(self,info=info)
            self.login.start()

    def updateBtnClickInAddUserPage(self):
        print('수정 저장')
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
        
        self.default.showMessageBoxs('수정완료','수정되었습니다.')
        # 데이터 동기화
        self.syncAddUserPageTable()
        self.Form.close()
        
    def saveBtnClickInAddUserPage(self):
        print('저장')
        # res = {
        #     'isAuth':'False',
        #     'groupId':'1번째사업자',
        #     'mallName':'옥션',
        #     'loginType':'카카오',
        #     'loginId':'ybbang0202@naver.com',
        #     'loginPass':'pchw1103',
        #     'emailId':'ybbang0202@naver.com',
        #     'emailPass':'3dlscldtlwja@',
        #     'nickName':'fuck',
        #     'memo':'메모',
        # }
        # 데이터를 저장합니다.
        try:
            SqliteDb().insertSqlData(self.info,'ShoppingMallAccountList')
        except AttributeError as e:
            self.default.showMessageBoxs('저장실패',f'{e}\n로그인 테스트 후 저장해주세요.')
            return False

        self.default.showMessageBoxs('저장완료','저장되었습니다.')

        # 데이터 동기화
        self.syncAddUserPageTable()

        self.Form.close()

    def syncAddUserPageTable(self):
        # 새로운 데이터를 불러옵니다.
        self.newtable = SetupTableWindow(SqliteDb().selectSqlData('ShoppingMallAccountList'),parent=self)
        # 위젯안에 데이터를 삭제함
        for i in reversed(range(self.parent.ui.load_pages.verticalLayout_2.count())): 
            self.parent.ui.load_pages.verticalLayout_2.itemAt(i).widget().setParent(None)
        # 데이터를 다시 넣어줌
        self.parent.ui.load_pages.verticalLayout_2.addWidget(self.newtable.table_widget)
        print('새로고침 완료')
        
    def updateMallNameListCombo(self,index):
        self.widget.selectloginTypeList.clear()
        items = self.widget.selectmallNameList.itemData(index)
        if items:
            self.widget.selectloginTypeList.addItems(items)



    # def deletebtn(self):
    #     print('수정버튼')
    #     self.adduserbutton()
    #     self.Form.setWindowTitle('쇼핑몰 계정 수정')

    #     button = self.parent.ui.sender()
    #     button = self.parent.sender()
    #     # if button:
    #     item = self.table_widget.indexAt(button.pos()).row()
    #     print(item.row())      
    #     # mallproductid = ( self.ranktrackingtableWidget.item( item.row(),12 ).text()  )

    def adduserbutton(self,data=False):
        
        print('계정추가')
        self.fuck = '추가'
        self.r = {
            'mallNameList':[
                ('쇼핑몰 선택','로그인방식 선택'),
                ('네이버쇼핑','네이버'),
                # ('쿠팡','쿠팡'),
                ('지마켓','지마켓,카카오'),
                ('옥션','옥션,카카오'),
                # ('SSG','SSG,카카오'),
                ('11번가','11번가,카카오'),
                ('티몬','티몬'),
                ('위메프','위메프'),
                ('롯데온','롯데온,카카오'),
                
                # ('타오바오','타오바오'),
                
                ],
            # 'loginTypeList':['기본','카카오']
            }

        self.Form = QWidget()
        self.widget = Ui_Form()
        # qtmodern.styles.dark(self.widget)
        self.widget.setupUi(self.Form)
        # self.Form = qtmodern.windows.ModernWindow(self.widget)
        self.Form.show()

        self.Form.setWindowTitle('쇼핑몰 계정 추가')
        
        # 숨카놓기
        self.widget.groupBox_4.hide()
        self.widget.saveBtn.setEnabled(False)
        # 스타일 셋팅
        self.Form.setStyleSheet(Themes().customWidget())

        self.widget.selectmallNameList.currentIndexChanged.connect(self.updateMallNameListCombo)
        self.updateMallNameListCombo(self.widget.selectloginTypeList.currentIndex())
        for mallName in self.r['mallNameList']:
            # print(mallName[0],mallName[1].split(','))
            self.widget.selectmallNameList.addItem(mallName[0],mallName[1].split(','))
        
        self.widget.tryloginBtn.clicked.connect(self.tryLoginBtnClickInAddUserPage)
        if data: # 수정 하는곳
            self.dbdata = data
            self.widget.saveBtn.clicked.connect(self.updateBtnClickInAddUserPage)
        else:    
            self.widget.saveBtn.clicked.connect(self.saveBtnClickInAddUserPage)

        self.widget.closeBtn.clicked.connect(self.closeBtnClickInAddUserPage)
        self.widget.pushButton.clicked.connect(self.twostepauthpushButton) # 2차인증버튼
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
#             place_holder_text = "쇼핑몰 아이디를 입력하세요 :",
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
#             place_holder_text = "쇼핑몰 비밀번호를 입력하세요 :",
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
#             place_holder_text = "쇼핑몰을 구분할 닉네임을 입력하세요 :",
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
#         self.selectloginTypelist.addItem('로그인 방식 선택')
#         self.selectmallNameList.currentIndexChanged.connect(self.updateMallNameListCombo)
#         self.updateMallNameListCombo(self.selectloginTypelist.currentIndex())
#         # for logintype in self.r['loginTypeList']:
#         #     self.selectloginTypelist.addItem(logintype)
#         # 
#         # BTN 1
#         self.saveBtn = PyPushButton(
#             text="저 장",
#             radius=8,
#             color=self.themes["app_color"]["text_foreground"],
#             bg_color=self.themes["app_color"]["dark_one"],
#             bg_color_hover=self.themes["app_color"]["dark_three"],
#             bg_color_pressed=self.themes["app_color"]["dark_four"]
#         )
#         self.saveBtn.setMaximumHeight(40)

#         self.tryloginBtn = PyPushButton(
#             text="로그인 시도",
#             radius=8,
#             color=self.themes["app_color"]["text_foreground"],
#             bg_color=self.themes["app_color"]["dark_one"],
#             bg_color_hover=self.themes["app_color"]["dark_three"],
#             bg_color_pressed=self.themes["app_color"]["dark_four"]
#         )
#         self.tryloginBtn.setMaximumHeight(40)

#         self.closeBtn = PyPushButton(
#             text="닫 기",
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
#         # self.widget.verticalLayout.addRow('쇼핑몰 선택 :',shoppingmallselectbox)
#         # # self.widget.verticalLayout.addStretch(1)
#         # self.widget.verticalLayout.addRow('쇼핑몰 닉네임 :',self.nickNameLineEdit)
#         # self.widget.verticalLayout.addRow('아이디 :',self.loginIdLineEdit)
#         # self.widget.verticalLayout.addRow('비밀번호 :',self.loginPassLineEdit)

#         # pushbuttons=QVBoxLayout()
#         # pushbuttons.addWidget(self.tryloginBtn)
#         # pushbuttons.addWidget(self.saveBtn)
#         # pushbuttons.addWidget(self.closeBtn)
#         # self.widget.verticalLayout.addRow(pushbuttons)
        
#         # self.label =QLabel('계정 추가')
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


        
