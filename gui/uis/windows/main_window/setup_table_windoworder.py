# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from audioop import reverse
from multiprocessing.sharedctypes import Value
from operator import index
import random
from unittest import result
from gui.db.conndb import SqliteDb
from gui.uis.windows.main_window.defpyqt import DefPyQt
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

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *
# from PySide6.QtWidgets import QMainWindow
from config import ConfigFile

class SetupOrderTableWindow(QMainWindow):
    def __init__(self,result=None,parent=None):
        super().__init__()
        self.parent = parent
        self.config = ConfigFile()
        self.default = DefPyQt()
        self.application_path = self.config.read()['system']['dir']
        # self.myTableWidget = SetupTableWindow(result,parent=self)
        # result = SqliteDb().selectSqlData('ShoppingMallAccountList')
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        self.sqldb = SqliteDb()
        # if result:
        result = result
        # print(result)
        # result = {
        #     'tablename':'ShoppingMallAccountList',
        #     'result':[],
        # }

        # print('테이블 refresh')
        # print(result)
        # result['result'] = [
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        # ]
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # # BTN 2
        # self.detailbutton = PyPushButton(
        #     text="삭제",
        #     radius=8,
        #     color=self.themes["app_color"]["text_foreground"],
        #     bg_color=self.themes["app_color"]["dark_one"],
        #     bg_color_hover=self.themes["app_color"]["dark_three"],
        #     bg_color_pressed=self.themes["app_color"]["dark_four"]
        # )
        # self.icon = QIcon(Functions.set_svg_icon("icon_delete_user.svg"))
        # self.detailbutton.setIcon(self.icon)
        # self.detailbutton.setMaximumHeight(40)

        # HOME TABLE WIDGETS 
        self.table_widget = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )


        # self.table_widget = QTableWidget()

        # # Columns / Header
        # self.column_1 = QTableWidgetItem()
        # self.column_1.setTextAlignment(Qt.AlignCenter)
        # self.column_1.setText("NAME")

        # self.column_2 = QTableWidgetItem()
        # self.column_2.setTextAlignment(Qt.AlignCenter)
        # self.column_2.setText("NICK")

        # self.column_3 = QTableWidgetItem()
        # self.column_3.setTextAlignment(Qt.AlignCenter)
        # self.column_3.setText("PASS")

        # # Set column
        # self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        # self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        # self.table_widget.setHorizontalHeaderItem(2, self.column_3)
    

    # def synctablee(self,result=False):
        # if result: result = result
        # from ....db.conndb import SqliteDb
        # result = SqliteDb().selectSqlData('ShoppingMallAccountList')
        # print(result)
        # if result['tablename'] == 'ShoppingMallAccountList':
        #     self.column_names = ['연결상태','그룹','쇼핑몰','로그인방식','아이디','비밀번호','메모','연결날짜']
        if result['tablename'] == 'ShoppingMallOrderList':
            self.column_names = ['상세정보','주문수집일','주문상태','구매처(계정)','결제번호','결제일','상품명','수취인명','우편번호','받는주소','구매가격','택배사','운송장번호','상품 URL','관리코드']
        print('----synctable----',(len(self.column_names)))
        column = [None] * len(self.column_names)
        self.table_widget.setColumnCount(len(self.column_names))
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection) # 다중 선택 불가능
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectItems) # 셀만 선택가능 개별
        
        for idx,i in enumerate(self.column_names):
            # print(idx,i)
            column[idx] =  QTableWidgetItem()
            column[idx].setTextAlignment(Qt.AlignCenter)
            column[idx].setText(i)
            self.table_widget.setHorizontalHeaderItem(idx, column[idx])

        # self.table_widget.setRowCount(len(result['result']))
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # print(result)
        # newlist = sorted(result['result'], key=lambda d: d['name']) 
        # result['result'] = result['result'].sort()
        result['result'].sort(key=lambda a:a[-1] , reverse = True)
        for row_number,row_data in enumerate(result['result']):
            row_number = self.table_widget.rowCount()
            
            # print(row_number)
            # print()
            # num = len(result['result']) - row_number
            self.table_widget.insertRow(row_number) # Insert row

            # row_data = list(row_data)
            # row_data.insert(0,'')
            # row_data.insert(0,'')
            self.toggle_button = PyToggle(
                width = 50,
                bg_color = self.themes["app_color"]["dark_two"],
                circle_color = self.themes["app_color"]["icon_color"],
                active_color = self.themes["app_color"]["context_color"]
            )
            # BTN 2
            self.detailbutton = PyPushButton(
                text="상세",
                radius=8,
                color=self.themes["app_color"]["text_foreground"],
                bg_color=self.themes["app_color"]["dark_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            self.icon = QIcon(Functions.set_svg_icon("icon_update.svg"))
            self.detailbutton.setIcon(self.icon)
            self.detailbutton.setMaximumHeight(40)
            
            self.detailbutton.clicked.connect(self.productdetailbtn)
            self.toggle_button.clicked.connect(self.togglebtn)
            # print(self.toggle_button.isChecked(),'체크드 ?')
            if row_data[1] == 'True': self.toggle_button.setChecked(True)
#['상세정보','사용','관리코드','쇼핑몰','로그인방식','아이디','2차인증메일(아이디)','메모','연결날짜']
# (30, 'test', '옥션', '화장실용 비데물티슈 80매 10입', 19800, '1519320097', '2309671464', '배송중', '이다혜', '28392', '충청북도 청주시 흥덕구 풍산로89번길 31 (세원2차아파트) (101~104동) 104동206호', 'https://ssl.auction.co.kr/Close/BuyAwardInfolayer.aspx?order_no=2309671464', '롯데택배', '311017462932', '2022년 09월 05일', '스마일 카드', '', 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오ybbang0202navercom.pkl', '2022-09-07 15:38:56')
            self.table_widget.setCellWidget(row_number,0,self.detailbutton) # 상세정보
            # self.table_widget.setCellWidget(row_number,1,self.toggle_button) # 토글버튼
            t={
                '관리코드': str(row_data[0]),
                '주문상태': str(row_data[7]),
                '구매처(계정)': str(row_data[17].split('\\')[-1].replace('.pkl','')),
                '결제번호': str(row_data[6]),
                '결제일': str(row_data[14]),
                '주문수집일': str(row_data[-1]),
                '상품명': str(row_data[3]),
                '수취인명': str(row_data[8]),
                '우편번호': str(row_data[9]),
                '받는주소': str(row_data[10]),
                '구매가격': str(row_data[4]),
                '택배사': str(row_data[12]),
                '운송장번호': str(row_data[13]),
                '상품URL': str(row_data[11]),
                '경로': str(row_data[17]),
            }
            
            self.table_widget.setItem(row_number,1,QTableWidgetItem(t['주문수집일'])) # 관리코드
            self.table_widget.setItem(row_number,2,QTableWidgetItem(t['주문상태'])) # 구매처
            self.table_widget.setItem(row_number,3,QTableWidgetItem(t['구매처(계정)'])) # 결제일
            self.table_widget.setItem(row_number,4,QTableWidgetItem(t['결제번호'])) # 로그인방식
            self.table_widget.setItem(row_number,5,QTableWidgetItem(t['결제일'])) # 아이디
            self.table_widget.setItem(row_number,6,QTableWidgetItem(t['상품명'])) # 2차인증메일*(아이디)
            self.table_widget.setItem(row_number,7,QTableWidgetItem(t['수취인명'])) # 메모
            self.table_widget.setItem(row_number,8,QTableWidgetItem(t['우편번호'])) # 등록일
            self.table_widget.setItem(row_number,9,QTableWidgetItem(t['받는주소'])) # 등록일
            self.table_widget.setItem(row_number,10,QTableWidgetItem(t['구매가격'])) # 등록일
            self.table_widget.setItem(row_number,11,QTableWidgetItem(t['택배사']) ) # 등록일
            self.table_widget.setItem(row_number,12,QTableWidgetItem(t['운송장번호'])) # 등록일
            self.table_widget.setItem(row_number,13,QTableWidgetItem(t['상품URL'])) # 등록일
            self.table_widget.setItem(row_number,14,QTableWidgetItem(t['관리코드'])) # 등록일

            # self.table_widget.setItem(row_number,14,QTableWidgetItem(t['경로'])) # 등록일
            # self.table_widget.setItem(row_number,15,QTable                                                                                                                                                                                                       WidgetItem(t['경로']))
            # self.table_widget.setItem(row_number,16,QTableWidgetItem(t['경로']))
            # self.table_widget.setItem(row_number,17,QTableWidgetItem(t['경로']))
            # self.table_widget.setItem(row_number,18,QTableWidgetItem(t['경로']))

            # for column_number,data in enumerate(row_data):
            #     # print(column_number)
            #     if column_number == 0:
            #         self.toggle_button = PyToggle(
            #             width = 50,
            #             bg_color = self.themes["app_color"]["dark_two"],
            #             circle_color = self.themes["app_color"]["icon_color"],
            #             active_color = self.themes["app_color"]["context_color"]
            #         )
            #         # BTN 2
            #         self.
            # 
            # 
            #  = PyPushButton(
            #             text="수정",
            #             radius=8,
            #             color=self.themes["app_color"]["text_foreground"],
            #             bg_color=self.themes["app_color"]["dark_one"],
            #             bg_color_hover=self.themes["app_color"]["dark_three"],
            #             bg_color_pressed=self.themes["app_color"]["dark_four"]
            #         )
            #         self.icon = QIcon(Functions.set_svg_icon("icon_update.svg"))
            #         self.detailbutton.setIcon(self.icon)
            #         self.detailbutton.setMaximumHeight(40)
                    
            #         self.detailbutton.clicked.connect(self.deletebtn)
            #         # print(self.toggle_button.isChecked(),'체크드 ?')
            #         if row_data[3] == 'True': self.toggle_button.setChecked(True)
            #         self.table_widget.setCellWidget(row_number,0,self.detailbutton)
            #         self.table_widget.setCellWidget(row_number,1,self.toggle_button)
            #     else:
            #         self.table_widget.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                

    def productdetailbtn(self):
        print('상세 버튼을 눌렀습니다.')
        
        # from gui.uis.windows.main_window.getallorders import GetAllOrders
        # from gui.uis.openmarkets.kakaologin import Kakao
        # self.parent.adduserbutton()
        # self.parent.Form.setWindowTitle('쇼핑몰 계정 수정')

        button = self.sender()
        # # if button:
        item = self.table_widget.indexAt(button.pos()).row()
        index = ( self.table_widget.item( item,14 ).text()  )
        result= self.sqldb.selectSqlData('ShoppingMallOrderList',id=index)
        self.default.showMessageBoxs('준비중',f'{result[-2]}\n준비중인 기능입니다.')
        # # {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오kys980531navercom.pkl'}
        # i = result
        # info  = {
        #     'groupId': '', 
        #     'id': i[0],
        #     'isAuth': i[1],
        #     'nickName': i[2], 
        #     'mallName': i[2], 
        #     'loginType': i[4], 
        #     'loginId': i[5],
        #     'loginPass': i[6], 
        #     'memo': i[7],
        #     'emailId': i[10],
        #     'emailPass': i[11],
        #     'cookiename':i[-2]
        #     }

        # if '카카오' in info['cookiename']: info['loginType'] = '카카오'
        # else: info['loginType'] = info['mallName'] 
        # print(info)
        # Kakao().kakaologinmaster(info,onlylogin=True)
        # # info['cookiename']= os.path.join(self.application_path,'COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
        # # self.orders = GetAllOrders([info],parent=self,onlylogin=True)
        # # self.orders.start()
        # # # # 숨카놓기
        # # # self.parent.widget.groupBox.hide()

        # # # self.parent.widget.loginIdLineEdit.setText(result[5]) # 아이디
        # # # self.parent.widget.loginPassLineEdit.setText(result[6]) # 비밀번호
        # # # self.parent.widget.nickNameLineEdit.setText(result[2]) # 닉네임
        
        # # # if result[4] == '카카오':
        # # #     self.parent.widget.groupBox_4.show()
        # # #     self.parent.widget.emailIdLineEdit.setText(result[10]) # 2차 아이디
        # # #     self.parent.widget.emailPassLineEdit_3.setText(result[11]) # 2차 비밀번호
            
        # # # self.parent.widget.textEdit.setText(result[7]) # 닉네임




    def togglebtn(self):

        print('토글버튼')

        button = self.sender()
        changevalue = str(button.isChecked())
        item = self.table_widget.indexAt(button.pos()).row()
        index = ( self.table_widget.item( item,2 ).text()  )
        # print(index)
        self.sqldb.updateSqlData('ShoppingMallAccountList',index,'isAuth',changevalue)


    def tableWidgetData(self):
        '''데이터 반환'''
        return result


    

