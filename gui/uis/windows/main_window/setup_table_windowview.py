# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from multiprocessing.sharedctypes import Value
import random
from unittest import result
from gui.db.conndb import SqliteDb
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from . functions_main_window import *
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
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            print(self._data[index.row()][index.column()])
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class SetupTableWindow:
    def __init__(self,result=None):
        super().__init__()
        # result = SqliteDb().selectSqlData('ShoppingMallAccountList')
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        # self.sqldb = SqliteDb()
        # if result:
        self.result = result
        # result = {
        #     'tablename':'ShoppingMallAccountList',
        #     'result':[],
        # }
        if self.result['tablename'] == 'ShoppingMallAccountList':
            self.column_names = ['연결상태','그룹','쇼핑몰','로그인방식','아이디','비밀번호','메모','연결날짜']
        # print('테이블 refresh')
        # print(result)
        # self.result['result'] = [
        #     (1, 'False', '1번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '2번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '3번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '4번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '5번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '6번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '7번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '8번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '9번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
        #     (1, 'False', '0번째사업자', '옥션', '카카오', 'ybbang0202@naver.com', 'pchw1103', '메모', '2022-07-20 18:05:21'),
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


        self.table = QTableView()
        # self.table.setHorizontalHeader(['fuck','fuck1'])
        # data = [
        #     [4, 9, 2],
        #     [1, "hello", 0],
        #     [3, 5, 0],
        #     [3, 3, "what"],
        #     ["this", 8, 9],
        # ]

# qwidgettable로 하면 필터링이안되고 -> db 조회식으로가야됨 -> 동기화식으로가야되고
# qtableview 로하면 버튼이 안달려 custom이 안됨

        self.model = TableModel(self.result['result'])
        
        # self.table.setHorizontalHeaderLabels(self.result['tablename'])
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1) # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)

        self.table.setModel(self.proxy_model)
        # # BTN 2
        # self.deleteUserPushButton = PyPushButton(
        #     text="삭제",
        #     radius=8,
        #     color=self.themes["app_color"]["text_foreground"],
        #     bg_color=self.themes["app_color"]["dark_one"],
        #     bg_color_hover=self.themes["app_color"]["dark_three"],
        #     bg_color_pressed=self.themes["app_color"]["dark_four"]
        # )
        # self.icon = QIcon(Functions.set_svg_icon("icon_delete_user.svg"))
        # self.deleteUserPushButton.setIcon(self.icon)
        # self.deleteUserPushButton.setMaximumHeight(40)

        # HOME TABLE WIDGETS 
        # self.table_widget = PyTableWidget(
        #     radius = 8,
        #     color = self.themes["app_color"]["text_foreground"],
        #     selection_color = self.themes["app_color"]["context_color"],
        #     bg_color = self.themes["app_color"]["bg_two"],
        #     header_horizontal_color = self.themes["app_color"]["dark_two"],
        #     header_vertical_color = self.themes["app_color"]["bg_three"],
        #     bottom_line_color = self.themes["app_color"]["bg_three"],
        #     grid_line_color = self.themes["app_color"]["bg_one"],
        #     scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
        #     scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
        #     context_color = self.themes["app_color"]["context_color"]
        # )


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
        # print('----synctable----',(len(self.column_names)))
        # column = [None] * len(self.column_names)
        # self.table_widget.setColumnCount(len(self.column_names))
        # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # for idx,i in enumerate(self.column_names):
        #     # print(idx,i)
        #     column[idx] =  QTableWidgetItem()
        #     column[idx].setTextAlignment(Qt.AlignCenter)
        #     column[idx].setText(i)
        #     self.table_widget.setHorizontalHeaderItem(idx, column[idx])

        # # self.table_widget.setRowCount(len(result['result']))
        # # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # # print(result)
        # for row_number,row_data in enumerate(self.result['result']):
        #     row_number = self.table_widget.rowCount()
        #     # print(row_number)
        #     # print()
        #     # num = len(result['result']) - row_number
        #     self.table_widget.insertRow(row_number) # Insert row
        #     print(row_data)
        #     for column_number,data in enumerate(row_data):
        #         # print(column_number)
        #         if column_number == 0:

        #             # BTN 2
        #             self.deleteUserPushButton = PyPushButton(
        #                 text="삭제",
        #                 radius=8,
        #                 color=self.themes["app_color"]["text_foreground"],
        #                 bg_color=self.themes["app_color"]["dark_one"],
        #                 bg_color_hover=self.themes["app_color"]["dark_three"],
        #                 bg_color_pressed=self.themes["app_color"]["dark_four"]
        #             )
        #             self.icon = QIcon(Functions.set_svg_icon("icon_delete_user.svg"))
        #             self.deleteUserPushButton.setIcon(self.icon)
        #             self.deleteUserPushButton.setMaximumHeight(40)
                    
        #             self.table_widget.setCellWidget(row_number,0,self.deleteUserPushButton)
        #             self.deleteUserPushButton.clicked.connect(self.deletebtn)
        #         else:
        #             self.table_widget.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        
        # self.proxy_model = QSortFilterProxyModel()
        # self.proxy_model.setFilterKeyColumn(-1) # Search all columns.
        # self.proxy_model.setSourceModel(self.table_widget)
        # self.proxy_model.sort(0, Qt.AscendingOrder)
        # self.table_widget.setModel(self.proxy_model)
        
    def deletebtn(self):
        print('삭제버튼')


    def tableWidgetData(self):
        '''데이터 반환'''
        return result


    

