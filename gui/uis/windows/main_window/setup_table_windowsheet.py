# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from multiprocessing.sharedctypes import Value
from operator import index
import random
from unittest import result
from gui.db.conndb import SqliteDb
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
from .defpyqt import DefPyQt

class SetupSheetWindow(QMainWindow):
    def __init__(self,result=None,parent=None):
        super().__init__()
        self.parent = parent
        self.default = DefPyQt()
        # result = SqliteDb().selectSqlData('ShoppingMallAccountList')
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        self.sqldb = SqliteDb()
        self.column_names = ['삭제','사용','관리코드','시트명','시트URL','연결날짜']
        print(result)
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # # BTN 2
        self.deleteUserPushButton = PyPushButton(
            text="삭제",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.icon = QIcon(Functions.set_svg_icon("icon_delete_user.svg"))
        self.deleteUserPushButton.setIcon(self.icon)
        self.deleteUserPushButton.setMaximumHeight(40)


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

        column = [None] * len(self.column_names)
        self.table_widget.setColumnCount(len(self.column_names))
        # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection) # 다중 선택 불가능
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectItems) # 셀만 선택가능 개별

        for idx,i in enumerate(self.column_names):
            column[idx] =  QTableWidgetItem()
            column[idx].setTextAlignment(Qt.AlignCenter)
            column[idx].setText(i)
            self.table_widget.setHorizontalHeaderItem(idx, column[idx])

        # self.table_widget.setRowCount(len(result['result']))
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # print(result)
        for row_number,row_data in enumerate(result['result']):
            # input(row_data)
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
            # # BTN 2
            self.readelbutton = PyPushButton(
                text="삭제",
                radius=8,
                color=self.themes["app_color"]["text_foreground"],
                bg_color=self.themes["app_color"]["dark_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            self.icon = QIcon(Functions.set_svg_icon("icon_delete_user.svg"))
            self.readelbutton.setIcon(self.icon)
            self.readelbutton.setMaximumHeight(40)
            # BTN 2
            self.deleteUserPushButton = PyPushButton(
                text="상세정보",
                radius=8,
                color=self.themes["app_color"]["text_foreground"],
                bg_color=self.themes["app_color"]["dark_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            self.icon = QIcon(Functions.set_svg_icon("icon_update.svg"))
            self.deleteUserPushButton.setIcon(self.icon)
            self.deleteUserPushButton.setMaximumHeight(40)
            
            self.deleteUserPushButton.clicked.connect(self.deletebtn)
            self.readelbutton.clicked.connect(self.realdelbtn)
            self.toggle_button.clicked.connect(self.togglebtn)
            # print(self.toggle_button.isChecked(),'체크드 ?')
            if row_data[1] == 'True': self.toggle_button.setChecked(True)
#['상세정보','사용','관리코드','쇼핑몰','로그인방식','아이디','2차인증메일(아이디)','메모','연결날짜']
            self.table_widget.setCellWidget(row_number,0,self.readelbutton) # 수정버튼
            # self.table_widget.setCellWidget(row_number,1,self.deleteUserPushButton) # 수정버튼
            # self.table_widget.setItem(row_number,1,QTableWidgetItem(str(row_data[0]))) # 관리코드

            self.table_widget.setCellWidget(row_number,1,self.toggle_button) # 토글버튼
            self.table_widget.setItem(row_number,2,QTableWidgetItem(str(row_data[0]))) # 관리코드
            self.table_widget.setItem(row_number,3,QTableWidgetItem(str(row_data[2]))) # 닉네임
            self.table_widget.setItem(row_number,4,QTableWidgetItem(str(row_data[3]))) # 쇼핑몰
            self.table_widget.setItem(row_number,5,QTableWidgetItem(str(row_data[-1]))) # 로그인방식

    def deletebtn(self):
        print('수정버튼')
        
        # self.parent.adduserbutton()
        # self.parent.Form.setWindowTitle('쇼핑몰 계정 수정')

        # button = self.sender()
        # # if button:
        # item = self.table_widget.indexAt(button.pos()).row()

        # index = self.table_widget.item( item,3 ).text()
        # result= self.sqldb.selectSqlData('ShoppingMallAccountList',id=index)
        # # print(result)
        # # 숨카놓기
        # self.parent.widget.groupBox.hide()
        #     # 'mallName':self.widget.selectmallNameList.currentText(),
        #     # 'loginType':self.widget.selectloginTypeList.currentText(),

        # self.parent.widget.selectmallNameList.setCurrentText(result[3])
        # self.parent.widget.selectloginTypeList.setCurrentText(result[4])
        # self.parent.widget.loginIdLineEdit.setText(result[5]) # 아이디
        # self.parent.widget.loginPassLineEdit.setText(result[6]) # 비밀번호
        # self.parent.widget.nickNameLineEdit.setText(result[2]) # 닉네임
        
        # if result[4] == '카카오':
        #     self.parent.widget.groupBox_4.show()
        #     self.parent.widget.emailIdLineEdit.setText(result[10]) # 2차 아이디
        #     self.parent.widget.emailPassLineEdit_3.setText(result[11]) # 2차 비밀번호
            
        # self.parent.widget.textEdit.setText(result[7]) # 닉네임

    def realdelbtn(self): # 여기 
        print('삭제버튼')

        if self.default.showMessageBoxsYesNo('삭제요청','정말로 삭제하실껀가요 ?') == False: return 

        button = self.sender()
        # # if button:
        item = self.table_widget.indexAt(button.pos()).row()
        print(item)
        index = self.table_widget.item( item , 2 ).text()
        print(item,index)

        query = f"DELETE FROM googlespreadsheet WHERE id={index};"
        # query = 'DROP TABLE googlespreadsheet;'
        self.sqldb.dbquery(query)
        # print(f'{query} / 삭제되었습니다.')
        self.default.showMessageBoxs('삭제','삭제되었습니다.')
        self.parent.syncAddSheet()

    def togglebtn(self):
        print('토글버튼') # 스프레드 시트 동기화 ###

        button = self.sender()
        changevalue = button.isChecked()
        item = self.table_widget.indexAt(button.pos()).row()
        index = ( self.table_widget.item( item,2 ).text()  )
        # print(index)
        a = self.sqldb.updateSqlData('googlespreadsheet','isuse',changevalue,index)
        if changevalue: self.default.showMessageBoxs('활성화','스프레드시트가 활성화 되었습니다.')
        else: self.default.showMessageBoxs('비활성화','스프레드시트가 비활성화 되었습니다.')

    def tableWidgetData(self):
        '''데이터 반환'''
        return result


    

