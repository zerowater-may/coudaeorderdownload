import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao


class InvoiceCenterAuction(Kakao):
##AUCTION 옥션 ##AUCTION 옥션 ##AUCTION 옥션 ##AUCTION 옥션 ##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션    
    
    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        # input(self.info)
        
        for _ in range(5):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print('옥션 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 중""")
                if self.info['loginType'] == '옥션':
                    self.AuctionLogin(self.info)
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                continue

            self.auction = requests.Session()
            # input('쿠키확인1')
            for cookie in cookies:    
                # print(cookie['name'], cookie['value'])
                self.auction.cookies.set(cookie['name'], cookie['value'])
                # self.driver.add_cookie(cookie)


            url = 'https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList?pageIndex=1&pageSize=10&searchPeriod=1M&searchStatus=ALL'
            # print(url)
            # print(page,'페이지 시작')
            response = self.auction.get(url)
            # try:
            #     # url = 'http://www.auction.co.kr/?redirect=1'
            #     # if '김영수' in response.text:
            #     #     print('영수잇음')
            #     # input(res.text)
            # except Exception:
            #     # print('커넥션 에러')
            #     continue
#https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList?pageIndex=15&pageSize=10&searchPeriod=1M&searchStatus=ALL
            # input(response.text)
            if (response.text) == '':
                print('주문이 없습니다.')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                return False

            if 'action="./Logout.aspx' in response.text:
                # print('있음')
                print('옥션 세션 실패 재로그인1')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                # input('pause')
                # self.beforeclass.update_msg.emit(f'{self.info["mallName"]}')
                if self.info['loginType'] == '옥션':
                    a = self.AuctionLogin(self.info)
                    if a == False:
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 비밀번호 변경 안내 """)
                        return False
                if self.info['loginType'] == '카카오':
                    a = self.isCookieLive(self.info)
                    print(a,'쿠키데이터')
                continue

            try:
                res = response.json()
                # print('dd')
            except Exception:
                print('옥션 세션 실패 재로그인2')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == '옥션':
                    a = self.AuctionLogin(self.info)
                    if a == False:
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 비밀번호 변경 안내 """)
                        return False
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                continue

            break
        print('옥션 로그인 성공')
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
        return res

    def InvoiceCheck_auction(self,info):
        self.info = info
        self.beforeclass = info['self']
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '옥션', 'loginId': 'kys980531', 'loginPass': 'qaz7410@@', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션옥션kys980531.pkl'}
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션카카오kys980531navercom.pkl'}
        
        # input('쿠키')
        self.cookiename = self.info['cookiename']
        islogin = self.islogin()
        if islogin == False: return False
        # input(islogin)
        # self.cookiename = '옥션카카오김영수'
        # self.application_path = '/Users/zerowater/Dropbox/zerowater/billy/DATA'
        
        page = 1
        
        # totalpage = 0 # 
        result = []
        while True:
            defaulturl = 'https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList'
            path = f'?pageIndex={page}&pageSize=10&searchPeriod=1M&searchStatus=ALL'
            url = '{}{}'.format(defaulturl,path)
            print(url)
            response = self.auction.get(url)
            if response.text == '': 
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
                # break
                return result
            
            res= response.json()
                # print(self.cookiename)
            # self.KakaoLogin(v,headless=False)
            # input('dd')

            # input(res)
            total = res['orderList']['TotalOrderCount']
            totalpage = m.ceil(total / 6)
            # totalpage = 1 # 나중에 풀어주기 테/스트 임

            print(f'{self.cookiename} 전체주문:',total,'현재 페이지:',page,'/',totalpage)
            for i in res['orderList']['PayInfoList']:
                
                res={'invoicenum':'','courier':''}
                # res['billiid'] = self.info['billiid']
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                res['wheretobuy'] = '옥션'
                res['price'] = int(str(i['TotalOrderAmount']).replace('.0',''))
                r = i['OrderList'][0]
                res['PayNo'] = str(r['OrderNo'])
                res['ordNo'] = str(r['OrderNo'])
                res['prdNm'] = r['ItemName']
                res['Status'] = r['Status']
                # print(res)
                # if res['ordNo'] == '1957321858':
                #     input(i)
                aaaa =self.InvoiceDetail_auction(r['OrderNo'])
                if aaaa:
                    res.update(aaaa) # 디테일
                else:
                    continue
                # https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList?pageIndex=17&pageSize=10&searchPeriod=1M&searchStatus=ALL
                if '배송시작' in str(r['Status']) or '배송중' in str(r['Status']) or '배송완료' in str(r['Status']) or '오늘도착예정' in str(r['Status']):
                    print('배송추적됨')
                    res['Status'] = '배송중'
                    res.update(self.deliveryCheck_auction(r['OrderNo'])) # 운송장 조회
                res['courier'] = res['courier'].replace('\r','').replace('\t','').replace('\n','').rstrip().lstrip()
                result.append(res)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/{total}] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                print(res)
                print('='*30)


            if totalpage == page or total == len(result):
                print('모든 페이지 완료')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
                # break
                return result
            

            page+=1
        # return result

    def InvoiceDetail_auction(self,ordNo):
        res = {}
        # ordNo= '2024187759'
        url = f'https://ssl.auction.co.kr/Close/BuyAwardInfolayer.aspx?order_no={ordNo}'
        print(url)
        while True:
            try:
                r = self.auction.get(url).text
                break
            except Exception:
                continue

        soup = BeautifulSoup(r, 'html.parser')
        # input(soup)
        try:
            d = soup.select('table.order-detail-table')[1].select('tr td')
            res['name'] = d[0].text
            res['detailurl'] = url
            res['addressnum'] = d[3].text.replace('\n','').replace('\t','').replace('\r','').split(']')[0].replace('[','')
            res['address'] = d[3].text.replace('\n','').replace('\t','').replace('\r','').split(']')[1].replace('//','')
            try:
                res['pay'] = (soup.select_one('#payInfoTbl div.msg').text.replace('\n','').replace('\t','').replace('\r',''))
            except Exception:
                res['pay'] = '스마일 카드'
                # res['pay'] = soup.select_one('#payInfoTbl tr')#.text.replace('\n','').replace('\t','').replace('\r','')
            res['paytime'] = soup.select_one('#uxazip > div.viply-veiw > div.uxc-vip-tit > div.num-date > p.bar > strong').text
            res['paydetail'] = ''
        except Exception:
            return False
        return res

    def deliveryCheck_auction(self,ordNo):
        url = f'http://escrow.auction.co.kr/Shipment/TraceItem.aspx?orderno={ordNo}'
        # print(url)
        soup = BeautifulSoup(self.auction.get(url).text, 'lxml')
        # input(soup)
        
        res={}
        res['courier']=''
        res['invoicenum']=''
        try:
            res['courier'] = soup.select_one('#contents > div > table > tbody > tr > td:nth-child(2)').text.replace('\n','').replace('\t','').replace('\r','')
            res['invoicenum'] = soup.select_one('#contents > div > table > tbody > tr > td.font_tahoma').text.replace('\n','').replace('\t','').replace('\r','')
        except:
            try: 
                print(f'옥션 주문번호 문제 url 확인 {url}')
                res['courier'] = soup.select_one('#contents > div.myatable03.mtxxs > table > tbody > tr:nth-child(6) > td').text.replace('\n','').replace('\t','').replace('\r','')
                res['invoicenum'] = soup.select_one('#contents > div.myatable03.mtxxs > table > tbody > tr:nth-child(7) > td').text.replace('\n','').replace('\t','').replace('\r','')
            except:
                pass

        
        return res

    def AuctionLogin(self,info,headless=False):
        '''옥션 로그인'''
        # headless=False
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # self.cookiename = 'G마켓카카오박예찬'
        
        url = 'https://memberssl.auction.co.kr/Authenticate/?url=http%3a%2f%2fwww.auction.co.kr%2f&return_value=0'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','id').send_keys(info['loginId'])
        self.driver.find_element('id','password').send_keys(info['loginPass'])
        
        try:
            self.driver.find_element('xpath','/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/button[1]').click()
        except Exception:
            self.driver.find_element('xpath','/html/body/div[3]/div/div/form/div/div/div/div[1]/fieldset/button[1]').click()

        time.sleep(3)
        if '특수문자 3가지' in str(self.driver.page_source):
            print('비밀번호 변경안내')
            self.driver.close()
            self.driver.quit() 
            return False
        self.driver.get('http://www.auction.co.kr/')
        self.driver.implicitly_wait(10),time.sleep(2)
        # input('사이트에 로그인 후 엔터를 누르세요.')

        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))

        defaulturl = 'https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList'
        path = f'?pageIndex=1&pageSize=10&searchPeriod=1M&searchStatus=ALL'
        url = '{}{}'.format(defaulturl,path)
        # input('ddd')
        

        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit() 
        return True
        
##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션

if __name__ == '__main__':
    info  = {'isAuth': 'True', 'groupId': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '메모장','naverId':'kys053123@naver.com','naverPass':'fkaustkfl12!'}
    info['self.cookiename']= os.path.join('/Users/zerowater/Dropbox/zerowater/billy/DATA','COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
    print(info)
    InvoiceCenterAuction().InvoiceCheck_auction(info)