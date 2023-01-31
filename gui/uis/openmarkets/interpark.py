import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao


##LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 G마켓
class InvoiceCenterInterPark(Kakao):

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '인터파크'
        print(self.info)
        page = 1
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    print('인터파크로그인')
                    if self.InterparkLogin(self.info) == False:
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
                        return False                
                if self.info['loginType'] == '카카오':
                    print('인터파크카카오로그인')
                    self.isCookieLive(self.info)
                continue
            

            # 쿠키를 확인하는 부분
            self.interpark = requests.Session()
            for cookie in cookies:    
                self.interpark.cookies.set(cookie['name'], cookie['value'])
            url = f'http://www.interpark.com/mypage/order/OrderSearchList.do?_method=initial&logintgt=mypage&sid1=gb&sid2=svc&sc.page={page}'

            headers = {'accept':'application/json, text/plain, */*','content-type':'application/json;charset=UTF-8'}
            res = self.interpark.get(url,headers=headers)

            soup = BeautifulSoup(res.text,'lxml')
            url = (str(soup.select_one('script')).replace('<script>location.href=','').replace(';</script>','').replace('"',''))
            # input(url)
            if 'login.do?' in url:
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    print('인터파크로그인')
                    if self.InterparkLogin(self.info) == False:
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
                        return False
                    
                if self.info['loginType'] == '카카오':
                    print('인터파크카카오로그인')
                    self.isCookieLive(self.info)
                continue

            self.total= len(soup.select('table.tb_myPg02 tr'))
            print('몇건?',self.total)

            if self.total == 1:
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                return False
            
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
            return True

    def InvoiceCheck_interpark(self,info):
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

            url = f'http://www.interpark.com/mypage/order/OrderSearchList.do?_method=initial&logintgt=mypage&sid1=gb&sid2=svc&sc.page={page}'

            headers = {'accept':'application/json, text/plain, */*','content-type':'application/json;charset=UTF-8'}
            res = self.interpark.get(url,headers=headers)
            soup = BeautifulSoup(res.text,'lxml')
            if page > 1000: break
            print(url)
            if len(soup.select('table.tb_myPg02 tr')) == 1: break
            for i in soup.select('table.tb_myPg02 tr'):
                # input(len())
                res={'invoicenum':'','courier':''}
                # input(i)
                try:
                    orderday = i.select_one('div.order_date').text
                except Exception:
                    continue
                key = i.select('td')
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                res['wheretobuy'] = 'interpark'
                res['ordNo'] = key[0].text.replace('\n','').replace('\t','').replace('\r','').replace(orderday,'')
                res['PayNo'] = key[0].text.replace('\n','').replace('\t','').replace('\r','').replace(orderday,'')
                res['prdNm'] = key[1].text.replace('\n','').replace('\t','').replace('\r','')
                res['qty'] = key[3].text.replace('\n','').replace('\t','').replace('\r','')
                res['price'] = key[4].text.replace(',','').replace('원','').replace('\n','').replace('\t','').replace('\r','')
                res['Status'] = key[5].text.replace('\n','').replace('\t','').replace('\r','')
                res['detailurl'] = key[5].text.replace('\n','').replace('\t','').replace('\r','')
                res['Status'] = key[5].text.replace('\n','').replace('\t','').replace('\r','')
                try:
                    res['invoicenum'] = key[6].select_one('a').get('href').split(',')[2].replace("'",'').replace("'",'')
                    res['courier'] = key[6].select_one('a').get('href').split(',')[1].replace("'",'').replace("'",'')
                except Exception:
                    pass
                try:
                    res.update(self.InvoiceDetail_interpark(res['ordNo'])) # 디테일
                except Exception:
                    continue

                res['courier'] = res['courier'].replace('(구현대택배)','')
                result.append(res)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                print(res)
                print('='*30)
                # if len(result) == 3: break
            page+=1
            # if len(result) == 3: break

        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
        return result  

    def InvoiceDetail_interpark(self,ordNo):
        res = {}
        # while True:
        breakingpoint = True
        # for _ in range(5):
        url = f'https://www.interpark.com/mypage/order/OrderSearchDetail.do?_method=orderDetailInfo&ordNo={ordNo}'
        print(url)
        # headers = {'accept':'application/json, text/plain, */*',
        #     'content-type':'application/json;charset=UTF-8'}
        response = self.interpark.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        
        res['name'] = soup.find('input',{'name':'rcvrNm'}).attrs['value']
        res['addressnum'] = soup.find('input',{'name':'zipNo'}).attrs['value']
        res['address'] = soup.find('input',{'name':'zipAddrDoro'}).attrs['value'] + ' ' + soup.find('input',{'name':'dtlAddr'}).attrs['value']
        res['pay'] = ''
        res['paydetail'] =''
        res['paytime'] = soup.select_one('#payCompSt').text.replace('\n','').replace('\t','').replace('\r','')
        return res


    def deliveryCheck_interpark(self,ordNo,invoicenum):
        url = f'https://www.interpark.com/p/delivery/deliverysearch/search?odNo={ordNo}&odSeq=1&invcNo={invoicenum}&procSeq=1'
        headers = {'accept':'application/json, text/plain, */*',
        'content-type':'application/json;charset=UTF-8'}
        data = {"odNo":ordNo}
        response = self.interpark.get(url,headers=headers).text.replace('\\','')
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
  
    
    def InterparkLogin(self,info):
        '''인터파크 로그인'''
        
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        url = 'https://accounts.interpark.com/login/form'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','userId').send_keys(info['loginId'])
        self.driver.find_element('id','userPwd').send_keys(info['loginPass'])
        # input('a')
        self.driver.find_element('xpath','/html/body/form[1]/div/div/div[1]/div[2]').click()
        time.sleep(4)
        if '/login' in str(self.driver.current_url):
            self.driver.close()
            self.driver.quit()      
            return False
        
        self.driver.get('https://www.interpark.com/malls/index.html')
        time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))
        
        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()  
        return True
#LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 #LOTTEON 인터파크 G마켓 