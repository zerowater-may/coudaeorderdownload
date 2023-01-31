# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import re

import openpyxl
from config import ConfigFile
from gui.db.googlespread import GoogleSpreadSheet
from gui.db.spreadthread import SyncSpreadSheetData
from gui.uis.windows.main_window.getallorders import GetAllOrders
from gui.uis.windows.main_window.setup_table_windoworder import SetupOrderTableWindow
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget

from .functions_main_window import *
import sys
import os
import webbrowser
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

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *
from .setup_table_window import *
from .defpyqt import DefPyQt
from datetime import datetime
# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *
from .adduserwidget import Ui_Form
from loginsession.logincheck import LoginSessionManageMent
from ...libs.customlibrary import Custom_Library
from gui.db.conndb import SqliteDb
# import pandas as pd

# #쓰레드 선언
# class SyncThread(Threading):
#     #parent = MainWidget을 상속 받음.
#     def __init__(self, parent=None):
#         super().__init__(parent=None)
#         self.parent = parent
#         print(self.parent)

#     def run(self):
#         self.parent.realsyncordertable()

class OrderManagement:
    def __init__(self,parent=None):
        super().__init__()
        self.config = ConfigFile()
        self.custom = Custom_Library()
        self.parent = parent
        self.application_path = self.config.read()['system']['dir']
        self.sheet =  GoogleSpreadSheet()
        # self.parent.isapi
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        # self.uid = UI_MainWindow()
        # self.uid.setup_ui(self)
        settings = Settings()
        self.settings = settings.items
        self.default = DefPyQt()
        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        result = SqliteDb().selectSqlData('ShoppingMallOrderList')
        self.orderTableWidget = SetupOrderTableWindow(result,parent=self)

        self.textbrowser = QTextBrowser()
        self.statusbar = QLabel()
        self.statusbar.setText('대기중 . . .')
        
        # 계정정보 추가하기 버튼
        # PUSH BUTTON 2
        self.push_button_1 = PyPushButton(
            text = "주문내역 가져오기",
            radius  =8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )

        self.push_button_1.setMinimumHeight(40)
        self.push_button_1.clicked.connect(self.getOrders)
        
        # PUSH BUTTON 2
        self.spreadsheetupload_button = PyPushButton(
            text = "스프레드시트 업로드",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.spreadsheetupload_button.setMinimumHeight(40)
        self.spreadsheetupload_button.setIcon(self.icon_2)

        # 업로드 버튼
        self.spreadsheetupload_button.clicked.connect(self.uploadspreadsheet)

        # PUSH BUTTON 2
        self.deleteorderdata = PyPushButton(
            text = "주문내역 삭제",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.deleteorderdata.setMinimumHeight(40)
        self.deleteorderdata.setIcon(self.icon_2)

        # 업로드 버튼
        self.deleteorderdata.clicked.connect(self.orderdatadelete)

        # PUSH BUTTON 2
        self.ordertable_sync_button = PyPushButton(
            text = "새로고침",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.ordertable_sync_button.setMinimumHeight(40)
        self.ordertable_sync_button.setIcon(self.icon_2)

        # 업로드 버튼
        self.ordertable_sync_button.clicked.connect(self.table_sync_button)
        # PUSH BUTTON 2
        self.to_excel_uploadform_button = PyPushButton(
            text = "운송장 업로드 폼 변환하기",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.to_excel_uploadform_button.setMinimumHeight(40)
        self.to_excel_uploadform_button.setIcon(self.icon_2)

        # 업로드 버튼
        self.to_excel_uploadform_button.clicked.connect(self.to_excel_form_button)

        # PUSH BUTTON 2
        self.exceldownload_button = PyPushButton(
            text = "엑셀 다운로드",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.exceldownload_button.setMinimumHeight(40)
        self.exceldownload_button.setIcon(self.icon_2)

        # 업로드 버튼
        self.exceldownload_button.clicked.connect(self.exceldownloadbutton)

        # 업로드 계정추가 버튼
        # self.parent.clicked.connect(self.updatespreadsheet)

    
    def exceldownloadbutton(self):
        print('엑셀로 다운로드합니다.')

        excelform = 'shopmine'

        # 엑셀 폴더 경로
        excelpath = os.path.join(self.application_path,'EXCELDOWNLOAD')

        # 일단 필터링 없이 엑셀로 다 다운로드
        result = SqliteDb().selectSqlData('ShoppingMallOrderList')['result']
        # result.insert(0, ('test','test1','test2'))
        # print(result)
        # df = pd.DataFrame(result)
        # df.columns = ['상세정보','주문수집일','주문상태','구매처(계정)','결제번호','결제일','상품명','수취인명','우편번호','받는주소','구매가격','택배사','운송장번호','상품 URL','','','','','관리코드']
        formattedDate = str(self.custom.now().strftime("%Y%m%d_%H%M%S"))

        wb = openpyxl.Workbook()
        # wb.create_sheet("TEST")
        sheet = wb['Sheet'] # 시트 선택
        for db in result:
            # input(db)
            sheet.append(db)

        wb.save(os.path.join(excelpath,f'{excelform}_{formattedDate}_{len(result)}건')+'.xlsx')
            
        # df.to_excel(
        #     os.path.join(excelpath,
        #     f'{excelform}_{formattedDate}_{len(result)}건')+'.xlsx',index=False)
            
        # self.default.showMessageBoxs('다운로드 성공',f'{}건의 상품 정보를 엑셀로 다운로드 완료했습니다.')

        # 다운로드가 완료되면 폴더열기
        try: 
            self.custom.createFolder(excelpath)
            webbrowser.open(excelpath)
        except Exception:
            self.default.showMessageBoxs('관리자 권한 오류','관리자 권한이 없는 폴더입니다.\n프로그램 폴더위치를 바탕화면으로 옮겨주세요.')




    def uploadspreadsheet(self):
        print('스프레드 시트를 업로드합니다.')

        # 전체 주문조회

        # 활성화 된 스프레드시트만 가져오기
        sheetinfo = [i for i in SqliteDb().selectSqlData('googlespreadsheet')['result'] if i[1] == 'True']
        sheetinfoname = "\n".join([i[2] for i in sheetinfo])
        if len(sheetinfo) == 0: self.default.showMessageBoxs('오류',f'스프레드시트 등록된 정보가 없습니다.'); return
        select = self.default.showMessageBoxsYesNo('선택',f'총 {len(sheetinfo)}개의 스프레드시트에 동기화 하시겠습니까 ?\n\n{sheetinfoname}')
        if select == False: return
        print(select)
        # print(orderdata)
        # 주문데이터랑 시트정보 넣기
        self.t = SyncSpreadSheetData(sheetinfo,parent=self)
        self.t.start()
        self.t.update_msg.connect(self.msg_update)

    def orderdatadelete(self):
        print('주문내역 삭제하기')
        a = self.default.showMessageBoxsYesNo('삭제요청','정말로 삭제하실껀가요 ?')
        if a:
            SqliteDb().delete_table('ShoppingMallOrderList')
            self.syncOrderTable()
    def table_sync_button(self):
        print('테이블 동기화 합니다.')
        self.syncOrderTable()

    def to_excel_form_button(self):
        print('엑셀 폼으로 만들기')
        # 활성화 된 스프레드시트만 가져오기
        sheetinfo = [i for i in SqliteDb().selectSqlData('googlespreadsheet')['result'] if i[1] == 'True']
        sheetinfoname = "\n".join([i[2] for i in sheetinfo])
        select = self.default.showMessageBoxsYesNo('선택',f'총 {len(sheetinfo)}개의 시트에서 운송장을 엑셀폼으로 생성하시겠습니까 ?\n\n{sheetinfoname}')
        if select == False: return
        print(select)
        # print(orderdata)

        # 주문데이터랑 시트정보 넣기
        self.s = SyncSpreadSheetData(sheetinfo,onlyinvoice=True,parent=self)
        self.s.start()
        self.s.update_msg.connect(self.msg_update)

    def updatespreadsheet(self):
        print('스프레드 시트 계정 추가/수정')

    def closeBtnClickInAddUserPage(self):
        print('닫기')
        self.Form.close()

    def tryLoginBtnClickInAddUserPage(self,info):
        print('로그인 쓰레드 시작 정보받고')
        # info = {
        #     'isAuth':'True',
        #     'groupId':'',
        #     'mallName':self.widget.selectmallNameList.currentText(),
        #     'loginType':self.widget.selectloginTypeList.currentText(),
        #     'loginId':self.widget.loginIdLineEdit.text(),
        #     'loginPass':self.widget.loginPassLineEdit.text(),
        #     'nickName':self.widget.nickNameLineEdit.text(),
        #     # 'updateDate': datetime.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        #     'memo':self.widget.textEdit.toPlainText(),
        # }
        # info  = {'isAuth': 'True', 'groupId': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '메모장','naverId':'kys053123@naver.com','naverPass':'fkaustkfl12!'}
        # print(info)
        info['cookiename']= os.path.join(self.application_path,'COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
        
        self.login = LoginSessionManageMent(self,info=info)
        self.login.start()
        print('여기로 통하나 ?')
        # res = {
        #     'isAuth':'False',
        #     'groupId':'1번째사업자',
        #     'mallName':'옥션',
        #     'loginType':'카카오',
        #     'loginId':'ybbang0202@naver.com',
        #     'loginPass':'pchw1103',
        #     'memo':'메모',
        # }
        # SqliteDb().insertSqlData(res,'ShoppingMallAccountList')

    def msg_update(self, msg):
        '''상태메세지 업데이트'''
        msg = datetime.now().strftime("[%H:%M:%S]")+' '+msg
        # try:
        # except Exception:
            # pass
        self.textbrowser.append(msg)
        self.statusbar.setText(msg)
        print(msg) # 나중에 로그로 바꾸기
        if '주문수집을 완료했습니다' in msg: # 쓰레드가 끝났으면 동기화 시켜주기
            print('동기화')
            self.syncOrderTable()
            msg = msg.replace("했습니다.","했습니다.\n")
            self.default.showMessageBoxs('주문건 수집완료',f'{msg}')
            
    def productdetailbtntest(self):
        print('부모 디테일 클릭함')

    def syncOrderTable(self):
    #     x = SyncThread(self)
    #     x.start()

    # def realsyncordertable(self):
        # 새로운 데이터를 불러옵니다.
        resultdata = SqliteDb().selectSqlData('ShoppingMallOrderList')
        # print(resultdata)
        self.newordertable = SetupOrderTableWindow(resultdata,parent=self)
        # 위젯안에 데이터를 삭제함
        # print(self.newordertable)
        for i in reversed(range(self.parent.ui.load_pages.row_4_layout.count())): 
            self.parent.ui.load_pages.row_4_layout.itemAt(i).widget().setParent(None)
        # # 데이터를 다시 넣어줌
        self.parent.ui.load_pages.row_4_layout.addWidget(self.newordertable.table_widget)
        # print('새로고침 완료')
        print('동기화 완료')
    
    def getOrders(self):
        print('주문내역을 가져옵니다.')
        result = SqliteDb().selectSqlData('ShoppingMallAccountList')
        # 토글 활성화인것만 추리기
        # res = [i for i in result['result'] if i[1] == 'True']
        # print(res)

        res = []
        accountinfos = ''
        for i in result['result']:
            if i[1] != 'True': continue
            info  = {
                'groupId': '', 
                'id': i[0],
                'isAuth': i[1],
                'nickName': i[2], 
                'mallName': i[3], 
                'loginType': i[4], 
                'loginId': i[5],
                'loginPass': i[6], 
                'memo': i[7],
                'emailId': i[10],
                'emailPass': i[11],
                }
            accountinfos+=(info['mallName']+'/'+info['loginType']+'/'+info['loginId']+'\n')
            info['cookiename']= os.path.join(self.application_path,'COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
            
            res.append(info)
        
        if len(res) == 0: self.default.showMessageBoxs('오류',f'등록된 계정정보가 없습니다.'); return
        select = self.default.showMessageBoxsYesNo('선택',f'총 {len(res)}개의 구매처에서 데이터를 수집하시겠습니까 ?\n\n{accountinfos}')
        if select == False: return
        print(select)
        # input(res)
        self.orders = GetAllOrders(res,parent=self)
        self.orders.start()
        self.push_button_1.setEnabled(False)
        self.orders.returnValue.connect(self.onCheckThreadFinished)
        self.orders.update_msg.connect(self.msg_update)
        # self.msg_update('',result=True)
        # 주문내역 수집하기 버튼 비활성화하기 

    def onCheckThreadFinished(self,result):
        print(result)
        print('리저르')

    def saveBtnClickInAddUserPage(self):
        print('저장')
        self.default.showMessageBoxs('저장완료','저장되었습니다.')

    def updateMallNameListCombo(self,index):
        self.widget.selectloginTypeList.clear()
        items = self.widget.selectmallNameList.itemData(index)
        if items:
            self.widget.selectloginTypeList.addItems(items)
 
    def adduserbutton(self):
        print('계정추가')
        
        # import qtmodern.styles
        # import qtmodern.windows

        self.r = {
            'mallNameList':[
                ('쇼핑몰 선택','로그인방식 선택'),
                ('네이버쇼핑','네이버'),
                ('쿠팡','쿠팡'),
                ('지마켓','카카오,지마켓'),
                ('옥션','카카오,옥션'),
                ('SSG','카카오,SSG'),
                ('11번가','카카오,11번가'),
                ('티몬','티몬'),
                ('위메프','카카오,위메프'),
                ('롯데온','카카오,롯데온')
               
                ],
            # 'loginTypeList':['기본','카카오']
            }

        self.Form = QWidget()
        self.widget = Ui_Form()
        self.Form.setWindowTitle('쇼핑몰 계정 추가')
        # qtmodern.styles.dark(self.widget)
        self.widget.setupUi(self.Form)
        # self.Form = qtmodern.windows.ModernWindow(self.widget)
        self.Form.show()


        # 스타일 셋팅
        self.Form.setStyleSheet(Themes().customWidget())

        self.widget.selectmallNameList.currentIndexChanged.connect(self.updateMallNameListCombo)
        self.updateMallNameListCombo(self.widget.selectloginTypeList.currentIndex())
        for mallName in self.r['mallNameList']:
            # print(mallName[0],mallName[1].split(','))
            self.widget.selectmallNameList.addItem(mallName[0],mallName[1].split(','))
        
        self.widget.tryloginBtn.clicked.connect(self.tryLoginBtnClickInAddUserPage)
        self.widget.saveBtn.clicked.connect(self.saveBtnClickInAddUserPage)
        self.widget.closeBtn.clicked.connect(self.closeBtnClickInAddUserPage)

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


        
