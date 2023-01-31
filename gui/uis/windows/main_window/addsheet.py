# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import webbrowser
from config import ConfigFile
from gui.uis.openmarkets.kakaologin import Kakao
from gui.uis.openmarkets.naverlogin import Naver
from gui.uis.windows.main_window.setup_table_windowsheet import SetupSheetWindow
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget

from .functions_main_window import *
import sys
import os , string

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
from ....db.googlespread import GoogleSpreadSheet
from gui.uis.pages.ui_main_pages import Ui_MainPages
# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *
from .setup_table_window import *
from .defpyqt import DefPyQt

import datetime
# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .addspreadsheet import Ui_Form
from loginsession.logincheck import LoginSessionManageMent

class AddSheet:
    def __init__(self,parent=None):
        super().__init__()
        self.uip = Ui_MainPages()
        self.parent = parent
        self.config = ConfigFile()
        self.application_path = self.config.read()['system']['dir']
        self.naver =  Naver()
        self.kakao =  Kakao()
        self.sheet =  GoogleSpreadSheet()
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
     

        result = SqliteDb().selectSqlData('googlespreadsheet')
        self.myTableWidget = SetupSheetWindow(result,parent=self)

        self.fuck = 'fuck'



        # 계정정보 추가하기 버튼
        # PUSH BUTTON 2
        self.addUserPushButton = PyPushButton(
            text = "시트정보 추가",
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

        self.syncPushButton.clicked.connect(self.syncAddSheet)
        
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

                if kakaores['email'][:2] != info['emailId'][:2]:
                    self.default.showMessageBoxs('2차인증 실패','카카오계정의 2차인증 이메일과 입력하신 이메일계정정보가 다릅니다. 카카오계정2차인증설정에서 이메일을 교체 후 시도해주세요..')
                    return False

                if self.naver.login(info,twostep=True):
                    self.default.showMessageBoxs('2차인증 성공','정상적으로 로그인 되었습니다.')
                else:
                    self.default.showMessageBoxs('2차인증 실패','아이디나 비밀번호를 확인해주세요.')
            else:
                self.default.showMessageBoxs('2차인증 입력오류','현재는 네이버 이메일만 가능합니다. 카카오계정2차인증설정에서 2차인증 이메일을 교체 후 시도해주세요.')

        else:
            self.default.showMessageBoxs('2차인증 입력오류','확인해주세요.')

    def closeBtnClickInAddSheet(self):
        print('닫기')
        self.Form.close()

    def trySheetConnectTestAddSheet(self):
        print('시트 연동 테스트')
        SPREADSHEET_ALPHABET = {
        'A': '1', 'B': '2','C': '3','D': '4','E': '5','F': '6','G': '7','H': '8','I': '9','J': '10','K': '11','L': '12','M': '13','N': '14','O': '15','P': '16','Q': '17','R': '18','S': '19','T': '20','U': '21','V': '22','W': '23','X': '24','Y': '25','Z': '26',
        'AA': '27', 'AB': '28','AC': '29','AD': '30','AE': '31','AF': '32','AG': '33','AH': '34','AI': '35','AJ': '36','AK': '37','AL': '38','AM': '39','AN': '40','AO': '41','AP': '42','AQ': '43','AR': '44','AS': '45','AT': '46','AU': '47','AV': '48','AW': '49','AX': '50','AY': '51','AZ': '52',}
        if self.widget.input_sheetname.text() == '': return self.default.showMessageBoxs('미입력 오류','시트명을 입력하세요.')
        if 'https://' not in self.widget.input_sheeturl.text(): return self.default.showMessageBoxs('잘못된 입력','시트URL을 재입력하세요.')
        if self.widget.input_sheeturl.text() == '': return self.default.showMessageBoxs('미입력 오류','시트URL을 입력하세요.')
        
        r = [   
            self.widget.comboBox.currentText(),
            self.widget.comboBox_2.currentText(),
            self.widget.comboBox_3.currentText(),
            self.widget.comboBox_4.currentText(),
            self.widget.comboBox_5.currentText(),
            self.widget.comboBox_7.currentText(),
            self.widget.comboBox_8.currentText(),
            self.widget.comboBox_9.currentText(),
            self.widget.comboBox_10.currentText(),
            self.widget.comboBox_11.currentText(),
        ]
        for i in range(1,8):
            try:
                if r[i] == r[i-1]:
                    return self.default.showMessageBoxs('오류','동일 알파벳이 있습니다. 수정해주세요.')
            except IndexError:
                pass
        # testlist = list('' for i in range(0,60))
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox.currentText()])] = 'No'
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox_2.currentText()])] = '수취인명'
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox_3.currentText()])] = '구매처'
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox_4.currentText()])] = '구매가격'
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox_5.currentText()])] = '택배사'
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox_7.currentText()])] = '운송장번호'
        # testlist[int(SPREADSHEET_ALPHABET[self.widget.comboBox_8.currentText()])] = '주문번호'
        # testlist.pop(0)
        self.worksheet,istest = self.sheet.getWorksheet(self.widget.input_sheeturl.text(),self.widget.input_sheetname.text())
        # self.worksheet,istest = self.sheet.getWorksheet('https://docs.google.com/spreadsheets/d/1PfD8X3ZTASV22QXnkSIUlau7tYK1dq5nVNZOJMWKbAg/edit#gid=1537881676','TITANS STORE')
        if istest:
            # print(testlist)
            # input(int(SPREADSHEET_ALPHABET[self.widget.comboBox_2.currentText()]))
            webbrowser.open(self.widget.input_sheeturl.text())
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox.currentText()]) , value='No')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_2.currentText()]) , value='수취인명')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_3.currentText()]) , value='구매처')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_4.currentText()]) , value='구매가격')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_5.currentText()]) , value='택배사')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_7.currentText()]) , value='운송장번호')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_8.currentText()]) , value='주문번호')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_9.currentText()]) , value='우편번호')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_10.currentText()]) , value='구매시간')
            self.sheet.updateCell(row = 1 , col = int(SPREADSHEET_ALPHABET[self.widget.comboBox_11.currentText()]) , value='주문고유번호')
            self.default.showMessageBoxs('시트 연동 성공',f'시트 연동에 성공했습니다.\n{self.worksheet}')
            self.widget.saveBtn.setEnabled(True)
        else:
            self.default.showMessageBoxs('시트 연동 실패',f'시트 연동에 실패했습니다.\n1.경로 상 setting.json 파일이 있는 지 확인해주세요\n2.시트 권한을 공유했는지 확인해주세요\n{self.worksheet}')



    def saveBtnClickInAddSheet(self):
        print('저장')
        res = {
            'sheetname':self.widget.input_sheetname.text(),
            'sheeturl':self.widget.input_sheeturl.text(),

            'isuse':'True',
            'No':self.widget.comboBox.currentText(),
            'name':self.widget.comboBox_2.currentText(),
            'wheretobuy':self.widget.comboBox_3.currentText(),
            'price':self.widget.comboBox_4.currentText(),
            'courier':self.widget.comboBox_5.currentText(),
            'invoicenum':self.widget.comboBox_7.currentText(),
            'ordNo':self.widget.comboBox_8.currentText(),
            'adressnum':self.widget.comboBox_9.currentText(),
            'buytime':self.widget.comboBox_10.currentText(),
            'idnum':self.widget.comboBox_11.currentText(),
        }
        # res = {'sheetname': 'TITANS STORE', 'sheeturl': 'https://docs.google.com/spreadsheets/d/1PfD8X3ZTASV22QXnkSIUlau7tYK1dq5nVNZOJMWKbAg/edit#gid=1537881676', 'No': 'A', 'name': 'B', 'wheretobuy': 'C', 'price': 'D', 'courier': 'E', 'invoicenum': 'F', 'ordNo': 'G'}
        print(res)
        
        # # 데이터를 저장합니다.
        try:
            SqliteDb().insertSqlData(res,'googlespreadsheet')
        except AttributeError as e:
            self.default.showMessageBoxs('저장실패',f'{e}\n스프레드시트 실패')
            return False

        self.default.showMessageBoxs('저장완료','저장되었습니다.')

        # # 데이터 동기화
        self.syncAddSheet()

        self.Form.close()

    def syncAddSheet(self):
        # 새로운 데이터를 불러옵니다.
        self.newtable = SetupSheetWindow(SqliteDb().selectSqlData('googlespreadsheet'),parent=self)
        # 위젯안에 데이터를 삭제함
        for i in reversed(range(self.parent.ui.load_pages.verticalLayout_3.count())): 
            self.parent.ui.load_pages.verticalLayout_3.itemAt(i).widget().setParent(None)
        # 데이터를 다시 넣어줌
        self.parent.ui.load_pages.verticalLayout_3.addWidget(self.newtable.table_widget)
        print('새로고침 완료')
        # 우편번호가 없네 

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

    def adduserbutton(self):
        print('시트정보 추가')
        # self.r = {
        #     'mallNameList':[
        #         ('쇼핑몰 선택','로그인방식 선택'),
        #         ('네이버쇼핑','네이버'),
        #         ('쿠팡','쿠팡'),
        #         ('지마켓','지마켓,카카오'),
        #         ('옥션','옥션,카카오'),
        #         ('SSG','SSG,카카오'),
        #         ('11번가','11번가,카카오'),
        #         ('티몬','티몬'),
        #         ('위메프','위메프'),
        #         ('롯데온','롯데온,카카오'),
        #         # ('타오바오','타오바오'),
        #         ],
        #     # 'loginTypeList':['기본','카카오']
        #     }

        self.Form = QWidget()
        self.widget = Ui_Form()
        # # qtmodern.styles.dark(self.widget)
        self.widget.setupUi(self.Form)
        # self.Form = qtmodern.windows.ModernWindow(self.widget)
        self.Form.show()
        self.widget.saveBtn.setDisabled(True)

        self.Form.setWindowTitle('스프레드시트 추가')
        spreadsheet_alphabet = list(string.ascii_uppercase) + ['A'+i for i in list(string.ascii_uppercase)]
        # # 숨카놓기
        # self.widget.groupBox_4.hide()

        # # 스타일 셋팅
        # self.Form.setStyleSheet(Themes().customWidget())
        self.widget.comboBox.addItems(spreadsheet_alphabet)
        self.widget.comboBox_2.addItems(spreadsheet_alphabet)
        self.widget.comboBox_3.addItems(spreadsheet_alphabet)
        self.widget.comboBox_4.addItems(spreadsheet_alphabet)
        self.widget.comboBox_5.addItems(spreadsheet_alphabet)
        self.widget.comboBox_7.addItems(spreadsheet_alphabet)
        self.widget.comboBox_8.addItems(spreadsheet_alphabet)
        self.widget.comboBox_9.addItems(spreadsheet_alphabet)
        self.widget.comboBox_10.addItems(spreadsheet_alphabet)
        self.widget.comboBox_11.addItems(spreadsheet_alphabet)
        # self.widget.selectmallNameList.currentIndexChanged.connect(self.updateMallNameListCombo)
        # self.updateMallNameListCombo(self.widget.selectloginTypeList.currentIndex())
        # for mallName in self.r['mallNameList']:
        #     # print(mallName[0],mallName[1].split(','))
        #     self.widget.selectmallNameList.addItem(mallName[0],mallName[1].split(','))
        
        # self.widget.tryloginBtn.clicked.connect(self.tryLoginBtnClickInAddUserPage)
        self.widget.testBtn.clicked.connect(self.trySheetConnectTestAddSheet)
        self.widget.saveBtn.clicked.connect(self.saveBtnClickInAddSheet)
        self.widget.closeBtn.clicked.connect(self.closeBtnClickInAddSheet)
        # self.widget.pushButton.clicked.connect(self.twostepauthpushButton) # 2차인증버튼
        # self.widget.selectloginTypeList.activated.connect(self.ComboValue)

