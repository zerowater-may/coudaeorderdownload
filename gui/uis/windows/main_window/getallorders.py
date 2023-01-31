# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from distutils.log import info
import re
from threading import Thread
import time

import requests
from config import ConfigFile
from gui.uis.openmarkets.aliexpress import InvoiceCenterAliexpress
from gui.uis.openmarkets.auction import InvoiceCenterAuction
from gui.uis.openmarkets.gmarket import InvoiceCenterGmarket
from gui.uis.openmarkets.eleven11st import InvoiceCenter11st
from gui.uis.openmarkets.interpark import InvoiceCenterInterPark
from gui.uis.openmarkets.lotteon import InvoiceCenterLotteon
from gui.uis.openmarkets.tmon import InvoiceCenterTmon
from gui.uis.openmarkets.wemarket import InvoiceCenterWemarket
from gui.uis.openmarkets.navershopping import InvoiceCenterNaverShopping
from gui.uis.openmarkets.center import InvoiceCenter

from gui.uis.openmarkets.kakaologin import Kakao
from gui.uis.openmarkets.naverlogin import Naver
# from gui.uis.windows.main_window.ordermanagementpage import OrderManagement
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
# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *
from .setup_table_window import *
from .defpyqt import DefPyQt

import datetime
# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .adduserwidget import Ui_Form
# from loginsession.logincheck import LoginSessionManageMent
import threading

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

class GetAllOrders(QThread):

    update_msg = Signal(str)
    returnValue = Signal(dict)

    def __init__(self,res,parent=None,onlylogin=False):
        super().__init__()

        self.parent = parent
        self.res = res
        self.config = ConfigFile()
        self.application_path = self.config.read()['system']['dir']
        self.naver =  Naver()
        self.kakao =  Kakao()
        self.onlylogin = onlylogin

        # SETUP OPENMARKET
        # self._auction = InvoiceCenterAuction()
        # self._gmarket = InvoiceCenterGmarket()
        # self._eleven11st = InvoiceCenter11st()
        # self.ordertable = OrderManagement()
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

    def work(self,id, start, end):
        result = []
        for i in range(start, end):
            t = random.randint(1,5)
            time.sleep(t)
            print(id,t,'초휴식')
            result.append(t)
        return result
    def slack_alram(self,text):
        '''포로야 안녕 '''
        try:
            token = "xoxb-3654661590581-3657847749234-OOY0CB8Rmo0wviNnYXCmKqr0"
            channel = "coudaesellerhelperdata"
            channel = "쿠대주문관리"
            # text = "TESTESTESTESTESTSETESTSET MESSAGE"
            f=requests.post("https://slack.com/api/chat.postMessage",
                headers={"Authorization": "Bearer "+token},
                data={"channel": channel,"text": text})
        # print(f.text)
        except Exception:
            pass
    def run(self):
        self.headless = True 
        self.update_msg.emit(f'{len(self.res)}개 구매처의 주문수집을 시작합니다.')
        # self.res = [
        #     # {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오kys980531navercom.pkl'}
        #     # {'groupId': '', 'id': 118, 'isAuth': 'True', 'nickName': '1번째사업자', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'ybbang0202@naver.com', 'loginPass': 'pchw1103', 'memo': '메모', 'emailId': 'ybbang0202@naver.com', 'emailPass': '3dlscldtlwja@', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오ybbang0202navercom.pkl'}
        #     {'groupId': '', 'id': 118, 'isAuth': 'True', 'nickName': '1번째사업자', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'ybbang0202@naver.com', 'loginPass': 'pchw1103', 'memo': '메모', 'emailId': 'ybbang0202@naver.com', 'emailPass': '3dlscldtlwja@', 'cookiename': 'C:\\Users\\user\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오ybbang0202navercom.pkl'}
        #     ]
        kakaos = []
        for i,info in enumerate(self.res):
            info['headless'] = self.headless
            # 카카오 세션이 있는지 확인
            # {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오kys980531navercom.pkl'}
            
            cookiekakao = info['loginType']+info['loginId']
            if info['loginType'] == '카카오' and cookiekakao not in kakaos:
                self.update_msg.emit(f'''[{info['loginType']}/{info['loginId']}] 로그인 세션 확인중''')
                self.kakao.kakaologinmaster(info) # 카카오 로그인 , 세션 
                # input('세션확인')
                self.kakao.close()
                self.update_msg.emit(f'''[{info['loginType']}/{info['loginId']}] 로그인 세션 확인완료''')

                # input('pass')
                kakaos.append(cookiekakao)

            # 각 마켓별로 긁어오기
        # 0313306971
        x = [None] * len(self.res)
        for i,info in enumerate(self.res):
            print(info)
            # 클래스 전달
            info['self'] = self
            info['page'] = 1
            info['headless'] = self.headless
            self.update_msg.emit(f"""[{info['mallName']}/{info['loginType']}/{info['loginId']}] 주문수집 시작""")
            
            if info['mallName'] == '옥션':    
                info['headless'] = False
                x[i] = ThreadWithResult(target=InvoiceCenterAuction().InvoiceCheck_auction, args=(info,))
                x[i].start()

            if info['mallName'] == '지마켓':     
                info['headless'] = False
                x[i] = ThreadWithResult(target=InvoiceCenterGmarket().InvoiceCheck_gmarket, args=(info,))
                x[i].start()
                
            if info['mallName'] == '11번가':     
                print('infoinfo',info)
                x[i] = ThreadWithResult(target=InvoiceCenter11st().InvoiceCheck_11st, args=(info,))
                x[i].start()
                
            if info['mallName'] == '위메프':     
                print('infoinfo',info)
                info['headless'] = False
                x[i] = ThreadWithResult(target=InvoiceCenterWemarket().InvoiceCheck_wemarket, args=(info,))
                x[i].start()

            if info['mallName'] == '롯데온':     
                print('infoinfo',info)
                x[i] = ThreadWithResult(target=InvoiceCenterLotteon().InvoiceCheck_lotteon, args=(info,))
                x[i].start()

            if info['mallName'] == '네이버쇼핑':     
                print('infoinfo',info)
                x[i] = ThreadWithResult(target=InvoiceCenterNaverShopping().InvoiceCheck_navershopping_apiv2, args=(info,))
                x[i].start()

            if info['mallName'] == '티몬':     
                print('infoinfo',info)
                x[i] = ThreadWithResult(target=InvoiceCenterTmon().InvoiceCheck_tmon, args=(info,))
                x[i].start()
            if info['mallName'] == '인터파크':     
                print('infoinfo',info)
                x[i] = ThreadWithResult(target=InvoiceCenterInterPark().InvoiceCheck_interpark, args=(info,))
                x[i].start()

            if info['mallName'] == '알리익스프레스':     
                print('infoinfo',info)
                info['headless'] = False
                x[i] = ThreadWithResult(target=InvoiceCenterAliexpress().InvoiceCheck_aliexpress, args=(info,))
                x[i].start()
        
        insertcount = 0
        updatecount = 0
        allcount = 0
        prices = 0
        prdNm = ''
        totalcount =0
        for i,info in enumerate(self.res):
            print(i,'조인')
            x[i].join()
            try:
                x[i].result
            except AttributeError:
                print('결과값이 없습니다 다음 이동~')
                continue

            print(x[i].result,'결과값') # 결과값
            # 데이터 6번째에 주문번호 있음
            self.db = SqliteDb()
            beforedb = self.db.selectSqlData('ShoppingMallOrderList')['result']
            beforeorderdb = [l[6] for l in beforedb]
            # input(beforedb)
            
            if x[i].result:
                
                for l in x[i].result:
                    allcount +=1
                    if l['ordNo'].rstrip().lstrip() not in beforeorderdb:# 만약 주문 번호가 없으면 바로 넣기 :
                        l['billiid'] = self.config.read()['loginform']['id']
                        l['price'] = re.sub(r'[^0-9]', '', str(l['price']))
                        # try:
                        # except Exception:
                        #     input(l['price'])
                        if l['paytime'] != '': 
                            a = re.sub(r'[^0-9]', '', l['paytime'])[:8]
                            try:
                                l['paytime'] = datetime.datetime(year=int(a[0:4]), month=int(a[4:6]), day=int(a[6:8])).strftime("%Y-%m-%d")
                            except Exception:
                                l['paytime'] = '' 

                        for _ in range(2):
                            try:
                                self.db.insertSqlData(l,'ShoppingMallOrderList')
                                break
                            except Exception:
                                l['address'] = ''
                                continue

                        insertcount +=1
                    else:
                        for b in beforedb:
                            if str(l['ordNo']).rstrip().lstrip() == str(b[6]).rstrip().lstrip(): # 주문번호가 같은경우
                                # print(b)
                                # l['Status'] = 'fuck'
                                # input(b)
                                if l['Status'] != b[7] or str(b[5]).rstrip().lstrip() != str(b[6]).rstrip().lstrip(): # 현재 상태와 이전 상태가 다른경우
                                    if l['paytime'] != '': 
                                        try:
                                            a =re.sub(r'[^0-9]', '', l['paytime'])[:8]
                                            l['paytime'] = datetime.datetime(year=int(a[0:4]), month=int(a[4:6]), day=int(a[6:8])).strftime("%Y-%m-%d")
                                        except Exception:
                                            l['paytime'] = ''
                                    print(f'{b[7]} -> {l["Status"]}')
                                    query = f'''UPDATE ShoppingMallOrderList
                                    SET 'Status' = '{l["Status"]}',
                                    'name' = '{l["name"]}', 
                                    'PayNo' = '{l["PayNo"]}', 
                                    'ordNo' = '{l["ordNo"]}', 
                                    'addressnum' = '{l["addressnum"]}', 
                                    'paytime' = '{l["paytime"]}', 
                                    'courier' = '{l["courier"]}', 
                                    'invoicenum' = '{l["invoicenum"]}', 
                                    'cookiepath' = '{l["cookiepath"]}', 
                                    'price' = '{l["price"]}' WHERE id={b[0]}
                                    '''
                                    print(query)
                                    self.db.dbquery(query)
                                    # self.db.updateSqlData('ShoppingMallOrderList','Status',l["Status"],b[0])
                                    updatecount +=1


                print('완료되었습니다.')
                datares = x[i].result
                for p in datares:
                    try:
                        prices+= int(p['price'])
                    except Exception:
                        pass
                    prdNm += '\n'+p['prdNm']
                    totalcount +=1

        if totalcount != 0:
            self.slack_alram(f'''{prdNm}\n
업체코드 : {self.config.read()['loginform']['id']}\n
주문건수 : {totalcount}건\n
매출 : {prices}원''')
        
        self.update_msg.emit(f'{len(self.res)}개 구매처의 주문수집을 완료했습니다. [전체주문 : {allcount}건 | 신규주문 : {insertcount}건 | 주문동기화 : {updatecount}건]')
        # 디비에 넣어주기
        # 테이블 동기화
        self.parent.push_button_1.setEnabled(True) # 다시 버튼 하기
        # self.parent.default.showMessageBoxs('주문건 수집완료',f'{len(self.res)}개 구매처의 주문수집을 완료했습니다.\n[전체주문 : {allcount}건 | 신규주문 : {insertcount}건 | 주문동기화 : {updatecount}건]\n오른쪽 위 새로고침 눌러주세요.')
    
    def test(self):
        print('완료~@!!~!!')

