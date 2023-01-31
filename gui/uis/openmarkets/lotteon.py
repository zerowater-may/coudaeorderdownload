import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao


##LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 G마켓
class InvoiceCenterLotteon(Kakao):

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '롯데온'
        print(self.info)
        page = 1
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    print('롯데온로그인')
                    self.LotteonLogin(self.info)
                if self.info['loginType'] == '카카오':
                    print('롯데온카카오로그인')
                    self.isCookieLive(self.info)
                continue
            

            # 쿠키를 확인하는 부분
            self.lotteon = requests.Session()
            for cookie in cookies:    
                self.lotteon.cookies.set(cookie['name'], cookie['value'])

            data = {"pageNo":page,"prdStrtDt":"","prdEndDt":"","searchPdNmBrdNmText":"","odInfwRteCd":"LTON"}
            url = 'https://pbf.lotteon.com/order/v1/mylotte/getOrderList'
            # url = 'https://www.lotteon.com/p/order/mylotte/orderDeliveryList'
            headers = {'accept':'application/json, text/plain, */*',
                        'content-type':'application/json;charset=UTF-8'}
            try:
                res = self.lotteon.post(url,data=str(data),headers=headers)
                if (res.text) == '':
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                    return False
                res = res.json()
                if res.pop('returnCode',0) == 422:
                    print('롯데온 429오류')
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
                    continue
                if res.pop('message','') == 'Not Readable Contents':
                    print('롯데온 Not Readable Contents')
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
                    continue

                break
            except Exception:
                print('lotteon 세션 실패 재로그인')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                continue
        
        try:#{'returnCode': '422', 'message': 'Not Readable Contents', 'subMessages': None, 'messageType': None, 'dataCount': 0, 'data': None, 'userMessage': None}
            total = res['totalCount']
        except Exception:
            if res['dataCount'] == 1:
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                return False
        print(res)
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
        return True

    def InvoiceCheck_lotteon(self,info):
        self.info = info
        self.beforeclass = info['self']
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '옥션', 'loginId': 'kys980531', 'loginPass': 'qaz7410@@', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션옥션kys980531.pkl'}
        self.cookiename = self.info['cookiename']
        islogin = self.islogin()
        if islogin == False: return False
        # 여기까지 기본

        page = 1
        result = []
        while True:

            data = {"pageNo":page,"prdStrtDt":"","prdEndDt":"","searchPdNmBrdNmText":"","odInfwRteCd":"LTON"}
            url = 'https://pbf.lotteon.com/order/v1/mylotte/getOrderList'
            # url = 'https://www.lotteon.com/p/order/mylotte/orderDeliveryList'
            headers = {'accept':'application/json, text/plain, */*',
                        'content-type':'application/json;charset=UTF-8'}
            try:
                res = self.lotteon.post(url,data=str(data),headers=headers)
                if (res.text) == '':
                    return False
                res = res.json()  
            except Exception:
                print('롯데온 오류')
                return False


            if len(res['dataList']) == 0:
                break

            if page == 1 : total = res['totalCount']
            print(f'{self.cookiename} 전체주문:',total)
            for i in res['dataList']:
                # input(i)
                res={'invoicenum':'','courier':''}
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                res['wheretobuy'] = self.wheretobuy
                res['price'] = i['fvrPrc']
                res['PayNo'] = str(i['odNo'])
                res['ordNo'] = str(i['odNo'])
                res['prdNm'] = i['spdNm']
                res['Status'] = i['dvBgtCnts']
                res['qty'] = i['odQty']
                res['invoicenum'] = i['invcNo']
                res['detailurl'] = f'https://www.lotteon.com/p/order/claim/orderDetail?odNo={res["ordNo"]}'

                try:
                    res.update(self.InvoiceDetail_lotteon(i['odNo'])) # 디테일
                except Exception:
                    continue

                if i['invcNo'] != None:
                    # print('배송추적됨')
                    # res['Status'] = '배송중'
                    res.update(self.deliveryCheck_lotteon(i['odNo'],i['invcNo'])) # 운송장 조회
                

                if res['Status'] == None: res['Status'] = '-'
                if res['invoicenum'] == None: res['invoicenum'] = ''
                # if res['name'] == '김민혁': 
                    # input(res)
                print(res)
                # print(res['invoicenum'],res['name'])
                print('='*30)
                # res['Status'] = 'fuck'
                result.append(res)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/{total}] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                # break

            page+=1

        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
        return result  

    def InvoiceDetail_lotteon(self,ordNo):
        res = {}
        # while True:
        breakingpoint = True
        for _ in range(2):
            url = 'https://pbf.lotteon.com/order/claim/v1/mylotte/getOrderDetail'
            # print(url)
            headers = {'accept':'application/json, text/plain, */*',
                'content-type':'application/json;charset=UTF-8'}
            data = {"odNo":ordNo}
            response = self.lotteon.post(url,data=str(data),headers=headers).json()
            print(ordNo)
            # input(response)
            try:
                soup = response['data']['orderDeliveryList'][0]
                breakingpoint = False
                break
            except Exception:
                # input(response)
                # input(ordNo)
                # print(ordNo)
                # print('롯데온 오류')
                # time.sleep(3)
                continue
        if breakingpoint: return {}
        # input(soup)
        # d = soup.select('table.order-detail-table')[1].select('tr td')
        res['name'] = soup['dvpCustNm']
        # if res['name'] == '이경숙':
        #     input(ordNo)
        res['addressnum'] = soup['dvpZipNo']
        res['address'] = soup['dvpStnmZipAddr'] +' '+soup['dvpStnmDtlAddr']
        pay = response['data']['pmtList'][0]
        # input(pay)
        res['pay'] =  pay['cccoCdText']
        res['paytime'] = pay['pyCmptDttm']
        res['paydetail'] =pay['crdNo']
        if res['pay'] == None: res['pay'] = ''
        if res['paytime'] == None:  res['paytime'] = ''
        if res['paydetail'] == None:  res['paydetail'] = ''
        return res

    def deliveryCheck_lotteon(self,ordNo,invoicenum):
        url = f'https://www.lotteon.com/p/delivery/deliverysearch/search?odNo={ordNo}&odSeq=1&invcNo={invoicenum}&procSeq=1'
        headers = {'accept':'application/json, text/plain, */*',
        'content-type':'application/json;charset=UTF-8'}
        data = {"odNo":ordNo}
        response = self.lotteon.get(url,headers=headers).text.replace('\\','')
        res={}
        # print(response['dvInfo'])

        try:
            res['courier'] = response.split('dvcNm":"')[1].split('"')[0]
        except Exception:
            pass
            # input(res)
        # res['invoicenum'] = soup.select_one('#contents > div > table > tbody > tr > td.font_tahoma').text.replace('\n','').replace('\t','').replace('\r','')
        # print(res)
        return res
  
    
    def LotteonLogin(self,info):
        '''롯데온 로그인'''
    
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        url = 'https://www.lotteon.com/p/member/login/common?rtnUrl=https://www.lotteon.com/p/mylotte/index/main'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','inId').send_keys(info['loginId'])
        self.driver.find_element('id','Password').send_keys(info['loginPass'])
        
        self.driver.find_element('xpath','/html/body/div[1]/main/div[1]/div/div/div[2]/button').click()
        time.sleep(4)
        self.driver.get('https://www.lotteon.com/')
        time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))

        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()     
#LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 #LOTTEON 롯데온 G마켓 