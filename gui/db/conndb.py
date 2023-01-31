from email.mime import application
import sqlite3 , os , math ,sys
# from PyQt5.QtWidgets import *
from PySide6.QtWidgets import *

from config import ConfigFile
# from PyQt5.QtWidgets import *
# if getattr(sys, 'frozen', False):
#     application_path = os.path.dirname(sys.executable)
# elif __file__:
#     application_path = os.path.dirname(__file__)

class SqliteDb:

    def __init__(self):
        configfile = ConfigFile()
        self.application_path = configfile.read()['system']['dir']
        # with sqlite3.connect('./data.db',isolation_level=None) as self.connection:
        try:
            # print(os.path.join(self.application_path,'data.db'))
            self.connection = sqlite3.connect(os.path.join(self.application_path,'data.db'),isolation_level=None)
            self.cur = self.connection.cursor()
            query = """ CREATE TABLE IF NOT EXISTS "ShoppingMallAccountList" (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'isAuth' TEXT,
                'groupId' TEXT,
                'mallName' TEXT,
                'loginType' TEXT,
                'loginId' TEXT,
                'loginPass' TEXT,
                'memo' TEXT,
                'updateDate' TEXT,
                'nickName' TEXT,
                'emailId' TEXT,
                'emailPass' TEXT,
                "timestamp" TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))
            );"""
                # 'date' TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            self.connection.execute(query)
            self.connection.commit()
            # 주문 테이블 
            query = """ CREATE TABLE IF NOT EXISTS "ShoppingMallOrderList" (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'billiid' TEXT,
                'wheretobuy' TEXT,
                'prdNm' TEXT,
                'price' INT,
                'PayNo' TEXT,
                'ordNo' TEXT,
                'Status' TEXT,
                'name' TEXT,
                'addressnum' TEXT,
                'address' TEXT,
                'detailurl' TEXT,
                'courier' TEXT,
                'invoicenum' TEXT,
                'paytime' TEXT,
                'pay' TEXT,
                'paydetail' TEXT,
                'cookiepath' TEXT,
                "timestamp" TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))
            );"""
                # 'date' TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            self.connection.execute(query)
            self.connection.commit()
            # 주문 테이블 
            query = """ CREATE TABLE IF NOT EXISTS "googlespreadsheet" (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'isuse' TEXT,
                'sheetname' TEXT,
                'sheeturl' TEXT,
                'No' INT,
                'name' TEXT,
                'wheretobuy' TEXT,
                'price' TEXT,
                'courier' TEXT,
                'invoicenum' TEXT,
                'ordNo' TEXT,
                'adressnum' TEXT,
                'buytime' TEXT,
                'idnum' TEXT,
                "timestamp" TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))
            );"""
            self.connection.execute(query)
            self.connection.commit()
            
        except Exception as e:
            print(e,'디비생성 실패')
            pass

        
        print('디비연결')

    def dbquery(self,query):
        # print(query)
        try:
            with sqlite3.connect(os.path.join(self.application_path,'data.db'),isolation_level=None) as self.connection:
                r = self.connection.execute(query)
                self.connection.commit()
                print(query,'완료')
        except sqlite3.OperationalError as e:
            print(e)
            return False

        return r
    

    def isduplicated(self,res):
        query =  f"SELECT * FROM NaverFindMyProduct WHERE mallProductId={res['mallProductId']} AND keyword='{res['keyword']}';"
        print(query)
        data = self.dbquery(query) # 상품코드가 같은  데이터
        if data == False: return True
        if data: 
            listdata = data.fetchall()
            if len(listdata) > 0 : return True # 이미 값이 있으면 패스
        
        return False

    def insertSqlData(self,res,tablename):
        '''계정정보 데이터 넣기'''
        print(res)
        if tablename == 'ShoppingMallAccountList':
            query = f"""INSERT INTO {tablename} (
                isAuth,
                groupId,
                mallName,
                loginType,
                loginId,
                loginPass,
                nickName,
                emailId,
                emailPass,
                memo) VALUES (
                    '{res["isAuth"]}',
                    '{res["groupId"]}',
                    '{res["mallName"]}',
                    '{res["loginType"]}',
                    '{res["loginId"]}',
                    '{res["loginPass"]}',
                    '{res["nickName"]}',
                    '{res["emailId"]}',
                    '{res["emailPass"]}',
                    '{res["memo"]}');"""
        if tablename == 'ShoppingMallOrderList':
            query = f"""INSERT INTO {tablename} (
                billiid,
                wheretobuy,
                prdNm,
                price,
                PayNo,
                ordNo,
                Status,
                name,
                addressnum,
                address,
                detailurl,
                courier,
                invoicenum,
                paytime,
                pay,
                paydetail,
                cookiepath) VALUES (
                    '{res["billiid"]}',
                    '{res["wheretobuy"]}',
                    '{res["prdNm"]}',
                    '{res["price"]}',
                    '{res["PayNo"]}',
                    '{res["ordNo"]}',
                    '{res["Status"]}',
                    '{res["name"]}',
                    '{res["addressnum"]}',
                    '{res["address"]}',
                    '{res["detailurl"]}',
                    '{res["courier"]}',
                    '{res["invoicenum"]}',
                    '{res["paytime"]}',
                    '{res["pay"]}',
                    '{res["paydetail"]}',
                    '{res["cookiepath"]}');"""
        if tablename == 'googlespreadsheet':
            query = f"""INSERT INTO {tablename} (
                'isuse',
                'sheetname',
                'sheeturl',
                'No',
                'name',
                'wheretobuy',
                'price',
                'courier',
                'invoicenum',
                'ordNo',
                'adressnum',
                'buytime',
                'idnum') VALUES (
                    '{res["isuse"]}',
                    '{res["sheetname"]}',
                    '{res["sheeturl"]}',
                    '{res["No"]}',
                    '{res["name"]}',
                    '{res["wheretobuy"]}',
                    '{res["price"]}',
                    '{res["courier"]}',
                    '{res["invoicenum"]}',
                    '{res["ordNo"]}',
                    '{res["adressnum"]}',
                    '{res["buytime"]}',
                    '{res["idnum"]}');"""

        
        print(query)
        self.cur.execute(query)

        print('데이터넣기완료')

    def delete_row(self,mallproductid,keyword):
        '''id 받고 삭제'''
        # query = f"DELETE FROM NaverFindMyProduct WHERE id={mallproductid};"
        query = f"DELETE FROM NaverFindMyProduct WHERE mallProductId={mallproductid} AND keyword='{keyword}';"
        print(query)
        self.dbquery(query)
        # self.loaddata_ranktracking()
        self.syncRankTracking()

    def delete_table(self,tablename):
        query = f"DELETE FROM {tablename};"
        print(query)
        self.dbquery(query)
        # self.loaddata_ranktracking()
        # self.syncRankTracking()

    def updateSqlData(self,tablename,key,changevalue,index,):
        '''디비 업데이트'''
        query = f"UPDATE {tablename} SET {key} = '{changevalue}' WHERE id={index}"
        print(query)
        self.dbquery(query)


    def selectSqlData(self,tablename,id=False):
        '''디비를 불러옵니다.
        ShoppingMallAccountList # 계정정보'''
        res = {}

        query = f"SELECT * FROM {tablename}"
        if id:
            query += f' WHERE id={id}'

        print('query',query)
        res['tablename'] = tablename
        for _ in range(2):
            try:
                self.connection = sqlite3.connect(os.path.join(self.application_path,'data.db'),isolation_level=None)
                self.cur = self.connection.cursor()
                res['result'] = list(self.cur.execute(query))
                break
            except Exception:
                # print(os.path.join(self.application_path,'data.db'))
                self.connection = sqlite3.connect(os.path.join(self.application_path,'data.db'),isolation_level=None)
                self.cur = self.connection.cursor()
                continue
        # print(res)
        if id: return list(res['result'][0])
        # print('리스트:',list(self.cur.execute(query)))
        
        return res
        # for i in list(listup):
        #     if i[1]+i[2] not in result :
        #         # result.index(i[1])
        #         # if i[2] != result
        #         result.append(i[1]+i[2])
        #         res.append(i)
        #         print(result)
 
    # def syncRankTracking(self):
    #     # DB 테이블 초기설정
    #     # pass
    #     # result = self.loaddata_ranktracking()
    #     result = SqliteDb().loaddata_ranktracking()
    #     result = [(18, '6393356208', '물티슈', '노메이커 물티슈 캡형, 100매, 20팩', 52, '-', 16609, '쿠팡', '쿠팡', '', '-', 0, '쿠팡', 'https://www.coupang.com/vp/products/6393356208?itemId=13639224644&vendorItemId=4519545975', '2022-06-29 12:22:40')]
    #     self.ranktrackingtableWidget.setRowCount(len(result))
    #     self.ranktrackingtableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    #     for row,i in enumerate(result):
    #         print(i)
    #         openmarket = i[12]
    #         if openmarket == '네이버쇼핑': 
    #             openmarket = '스마트스토어'
    #             rank = f'{math.ceil(i[4]/40)}페이지 {i[4]%40}위'
    #         elif openmarket == '쿠팡':
    #             rank = f'{math.ceil(i[4]/36)}페이지 {i[4]%36}위'
    #         self.ranktrackingtableWidget.setItem(row,2,QTableWidgetItem(openmarket))#쇼핑몰
    #         self.ranktrackingtableWidget.setItem(row,3,QTableWidgetItem(rank))#순위
    #         self.ranktrackingtableWidget.setItem(row,4,QTableWidgetItem(str(i[5])))#판매량
    #         self.ranktrackingtableWidget.setItem(row,5,QTableWidgetItem(str(i[6])))#리뷰수
    #         self.ranktrackingtableWidget.setItem(row,6,QTableWidgetItem(str(i[-1])))#추적시간
    #         self.ranktrackingtableWidget.setItem(row,7,QTableWidgetItem(str(i[2])))#키워드
    #         self.ranktrackingtableWidget.setItem(row,8,QTableWidgetItem(str(i[3])))#상품명
    #         self.ranktrackingtableWidget.setItem(row,9,QTableWidgetItem(str(i[10])))#상품등록일
    #         isoversea = '-'
    #         if str(i[9]) == '1': isoversea = '해외'
    #         elif str(i[9]) == '0': isoversea = '국내'
    #         self.ranktrackingtableWidget.setItem(row,10,QTableWidgetItem(isoversea))#상품타입
    #         self.ranktrackingtableWidget.setItem(row,11,QTableWidgetItem(str(i[-2])))#상품링크
    #         self.ranktrackingtableWidget.setItem(row,12,QTableWidgetItem(str(i[1])))#상품코드
    #         self.ranktrackingtableWidget.setItem(row,13,QTableWidgetItem(str(i[0])))#ID

    #         self.stat_btn = QPushButton('자세히')
    #         self.ranktrackingtableWidget.setCellWidget(row,0,self.stat_btn)
    #         self.del_btn = QPushButton('삭제')
    #         self.ranktrackingtableWidget.setCellWidget(row,1,self.del_btn)
            

    #         self.stat_btn.clicked.connect(self.btn_fun)
    #         self.del_btn.clicked.connect(self.delete_btn)

    # def btn_fun(self):
    #     button = self.sender()

    #     item = self.ranktrackingtableWidget.indexAt(button.pos())  
    #     # print(item.row())      
    #     print( self.ranktrackingtableWidget.item( item.row(),1 ).text()  )
        
    #     self.Form = QtWidgets.QWidget()
    #     self.ui = Ui_Form()
    #     self.ui.setupUi(Form)
    #     self.Form.show()
        



if __name__ == '__main__':
    # SqliteDb().loaddata_ranktracking()
    res = {'mallProductId': '6579718682', 'total': 324, 'rank': 27, 'purchaseCnt': 0, 'reviewCountSum': 0, 'manuTag': '가챠,만화피규어', 'productTitle': 'PLEX 크레용신짱 카자마 토오루 철수 사쿠다라 네네 유리 보오 맹구 소프비 피규어', 'mallName': '네임', 'mallprodCnt': '1992', 'openDate': '20220422', 'storename': 'nameme', 'mallProductUrl': 'https://smartstore.naver.com/main/products/6579718682', 'overseaTp': '1', 'keyword': '맹구피규어', 'producturl': '6579718682', 'openmarket': '네이버쇼핑'}
    # res = list(res.values())
    SqliteDb().insert_ranktracking(res)