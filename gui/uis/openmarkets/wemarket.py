import json
import os
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao


#위메프
class InvoiceCenterWemarket(Kakao):

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '위메프'
        count = 1 
        total = None
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    self.WeLogin(self.info)
                    continue
            
            # 쿠키를 확인하는 부분
            self.we = requests.Session()
            for cookie in cookies:    
                self.we.cookies.set(cookie['name'], cookie['value'])

            # 로그인 확인 유무
            url = 'https://front.wemakeprice.com/mypage/orders?page=1'
            # print(url)
            res = self.we.get(url)#,data=str(data),headers=headers)
            if (res.text) == '':
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                return False
            try:
                soup = BeautifulSoup(res.text,'html.parser')
                # print(soup)
                data = (str(soup.select('script')[2]).replace('\n','').replace("<script>    GV.set('initialData', JSON.parse('","").split('GV.set')[0].replace("'));",""))
                data = (json.loads(eval(json.dumps(data))))
                if data.pop('checkViewCaptchaImage',False):
                    print('캡차이미지')
                    
                    if self.wheretobuy == '위메프':
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인""")
                        self.WeLogin(self.info,headless=False)
                    continue
                total = len(data['purchase'])
            except Exception:
                print('위메프 세션 실패 재로그인')
                if self.wheretobuy == '위메프':
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인""")
                    if os.path.isfile(self.cookiename):
                        os.remove(self.cookiename)
                    self.WeLogin(self.info,headless=False)
                    continue
        
        if total == None: 
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
            return False

        if total == 0:
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
            return False

        print('전체주문:',total)
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
        return True



    def InvoiceCheck_wemarket(self,info):
        result = []
        self.info = info
        
        print(self.info)
        self.beforeclass = info['self']
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '옥션', 'loginId': 'kys980531', 'loginPass': 'qaz7410@@', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션옥션kys980531.pkl'}
        self.cookiename = self.info['cookiename']
    
        islogin = self.islogin()
        if islogin == False: return False


        # 여기까지 기본 
        page = 1
        while True:

            url = f'https://front.wemakeprice.com/mypage/orders?page={page}'
            res = self.we.get(url)
            if (res.text) == '':
                return result

            soup = BeautifulSoup(res.text,'html.parser')
            data = (str(soup.select('script')[2]).replace('\n','').replace("<script>    GV.set('initialData', JSON.parse('","").split('GV.set')[0].replace("'));",""))
            data = (json.loads(eval(json.dumps(data))))
            self.total = len(data['purchase'])
            if self.total == 0:
                break

            print(f'{self.cookiename} 전체주문:',self.total)
            for i in data['purchase']:
                res = {'invoicenum':'','courier':''}
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                res['wheretobuy'] = self.wheretobuy

                k = i['bundle'][0]['orderProd'][0]
                res['inNo'] = str(i['bundle'][0]['bundleNo'])
                res['ordNo'] = str(i['purchaseNo'])
                res['PayNo'] = res['ordNo'] # 주문 번호
                res['prdNm'] = k['prodNm']
                res['Status'] = i['bundle'][0]['bundleStatus'][0]
                res['detailurl'] = f'https://front.wemakeprice.com/mypage/order/{res["ordNo"]}'
                res['qty'] = k['prodQty']
                res['paytime'] = i['purchaseDateDetail']

                try:
                    res.update(self.InvoiceDetail_we(res['ordNo'])) # 디테일
                except Exception:
                    continue
                if res['Status'] == '배송중' or res['Status'] == '배송완료':
                    res.update(self.deliveryCheck_we(res['inNo'])) # 운송장 조회
                
                print(res)
                print('='*30)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                result.append(res)
                # break
            page+=1


        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")                
        return result

    def InvoiceDetail_we(self,ordNo):
        res = {}
        url = f'https://front.wemakeprice.com/mypage/order/{ordNo}'
        # print(url)
        response = self.we.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        data = str(soup.select('script')[2]).replace('\n','').replace("<script>    GV.set('initialData', JSON.parse('","").split('GV.set')[0].replace("'));","")
        data = json.loads(eval(json.dumps(data)))
        # input(data)

        res['name'] = data['shipAddress']['receiverNm']
        res['addressnum'] = data['shipAddress']['zipcode']
        res['address'] = data['shipAddress']['addr1'] +' '+data['shipAddress']['addr2']
        res['pay'] =  ' '.join(data['payment']['paymentMethod'])
        res['paydetail'] = ''
        res['price'] = data['payment']['totalPgPaymentPrice']
        # if res['name'] == '하점종':
        #     print(data)
        return res

    def deliveryCheck_we(self,ordNo):
        url = f'https://front.wemakeprice.com/open/mypage/delivery/status?deliveryNo={ordNo}&deliveryType=O'
        # print(url)
        # url = 'https://front.wemakeprice.com/open/mypage/delivery/status?deliveryNo=305200890&deliveryType=O'
        response = self.we.get(url)
        
        res={'invoicenum':'','courier':''}
        soup = BeautifulSoup(response.text,'lxml')
        # print(soup)
        # input(url)
        try:
            data = (str(soup.select('script')[2]).replace('\n','').replace("<script>    GV.set('initialData', JSON.parse('","").split('GV.set')[0].replace("'));",""))
            data = (json.loads(eval(json.dumps(data))))
        except Exception:
            return res
        # print(data)
        try:
            res['courier'] = data['ship']['shipMethod']
            res['invoicenum'] = ''
        except Exception:
            res['courier'] = data['ship']['companyNm']
            res['invoicenum'] = data['ship']['invoiceNo']
        print(res)
        # try:
        # except Exception:
        #     pass
        return res
    def WeLogin(self,info,headless=True):
        '''위메프 로그인'''
        

        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)

        url = 'https://front.wemakeprice.com/user/login?returnUrl=https%3A%2F%2Ffront.wemakeprice.com%2Fmain&type=GENERAL&orderYN=N&selectionYN=N'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','_loginId').send_keys(info['loginId']),time.sleep(2)
        self.driver.find_element('id','_loginPw').send_keys(info['loginPass'])
        # if headless:
        #     input('캡차우회후에 엔터눌러주세요')
        self.driver.find_element('id','_userLogin').click(),time.sleep(2)
        # https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fis_popup%3Dfalse%26ka%3Dsdk%252F1.39.8%2520os%252Fjavascript%2520sdk_type%252Fjavascript%2520lang%252Fko-KR%2520device%252FMacIntel%2520origin%252Fhttps%25253A%25252F%25252Fmw.wemakeprice.com%26auth_tran_id%3Dtzvy9fnzmbkf1d96d72f09dc4c0a2c3bc670e9e17d5kvm5amzf%26response_type%3Dcode%26state%3Df493f04152db602a68e5617a6559b7c865484b95207ca36c3903c24ef29151afc2bff3ef197e9d1027d29758a0ff6828015a48799b7fd14942ccc966274c09ff820819258c364fcb3407abd80598e64b587c9a1989c5ca875f9e3c0f2fbe0276%257CreturnUrl%253D%25252Fmypage%257CselectionYn%253DN%26redirect_uri%3Dhttps%253A%252F%252Fmw.wemakeprice.com%252Fsnslogin%252Foauth%252Fauth%252Fcallback%26client_id%3Df1d96d72f09dc4c0a2c3bc670e9e17d5
        # input('pass')
        time.sleep(4)
        self.driver.get('https://front.wemakeprice.com/main')
        time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))

        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()     

##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프##위메프 WEMARKEPRICE ##위메프