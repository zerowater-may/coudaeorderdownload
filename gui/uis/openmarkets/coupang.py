import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao

class InvoiceCenterGmarket(Kakao):

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '쿠팡'
        
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    self.GmarketLogin(self.info)
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                continue
            

            # 쿠키를 확인하는 부분
            self.gmarket = requests.Session()
            for cookie in cookies:    
                self.gmarket.cookies.set(cookie['name'], cookie['value'])

            data = {
                # 'searchSDT': '2021-09-29',
                # 'searchEDT': '2021-10-28',
                'searchStatus':'DELIVERY_CMPL',
                'page':'1',
                'pageSize':'5',
            }
            res = (self.gmarket.post('https://myg.gmarket.co.kr/ContractList/GeneralContractListAjax',data=data))
                # 주문이 없는 경우 추가해야함
                # self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
            try:
                res = res.json()
                break
            except Exception:
                if '로그인에 실패하였습니다.' in res.text:
                    print('지마켓 세션 만료')
                    if os.path.isfile(self.cookiename):
                        os.remove(self.cookiename)
                        
                    if self.info['loginType'] == '카카오':
                        self.isCookieLive(self.info)
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                    elif self.info['loginType'] == 'G마켓':
                        self.GmarketLogin(self.info)
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                        continue
        total = False
        try:
           
            total = res['total']
            print('전체주문:',total)
            self.total = total
        except TypeError:
            if 'G마켓 점검중!' in res.text:
                print('서버 점검중')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 지마켓 서버 점검중 ...""")
                return False
        if total == 0:
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
            return False
        if total == False: 
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
            return False
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
        return True

    def InvoiceCheck_gmarket(self,info):
        self.info = info
        self.beforeclass = info['self']
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '옥션', 'loginId': 'kys980531', 'loginPass': 'qaz7410@@', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션옥션kys980531.pkl'}
        self.cookiename = self.info['cookiename']
        islogin = self.islogin()
        if islogin == False: return False
        # 여기까지 기본

        result = []
        for serachStatus in ['DELIVERY_CMPL','ORDER_ING']:
            page = 1
        result = []
        page=1
        while True:

        # for _ in range(1):
            
            url =f'https://mc.coupang.com/ssr/api/myorders?requestYear=2022&pageIndex={page}&size=10'
            res = self.coupang.get(url).json()
            # input(res)
            print(url)
            # print()
            # print(res['hasNext'],res['nextPageIndex'])
            if res['nextPageIndex'] == 1: break

            for idx,i in enumerate(res['orderList']):
                # input(v)
                # print(i)
                # if i['orderId'] == 24000139195796:
                    # input(i)
                res={'invoicenum':'','courier':''}
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                res['wheretobuy'] = self.wheretobuy
                res['ordNo'] = str(i['orderId']) # 주문 번호
                res['payNo'] = str(i['orderId']) # 주문 번호
                res['detailurl'] = url
                res['address'] = i['deliveryDestination']['address']
                res['addressnum'] = i['deliveryDestination']['zipCode']
                res['qty'] = i['bundleReceiptList'][0]['vendorItems'][0]['quantity']
                
                res['invoicenum'] = i['deliveryGroupList'][0]['invoiceNumber']
                try:
                    res['msg'] = i['deliveryGroupList'][0]['pddMessageForShiptrack']['message']
                except Exception:
                    res['msg'] = ''
                try:
                    res['courier'] = i['deliveryGroupList'][0]['deliveryCompany']['companyName']
                except Exception:
                    pass
                res['price'] = i['bundleReceiptList'][0]['vendorItems'][0]['unitPrice'] +i['bundleReceiptList'][0]['shippingFee']
                res['Status'] = i['deliveryGroupList'][0]['invoiceStatus']
                if res['Status'] == 'DELIVERING': res['Status'] = '배송중 /' + res['msg']
                if res['Status'] == 'FINAL_DELIVERY': res['Status'] = '배송완료 /' + res['msg']
                res['name'] = self.getName(res['ordNo'])['name']
                res['pay'] =  'COUPANG'
                res['paytime'] =  i['orderedAt']
                res['paydetail'] = 'COUPANG'


                result.append(res)
                print(res)
                print('===='*10)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/{self.total}이상] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                # break
                # total 맞춰야함 ;;;;;; 지금바로할것 
                # [18:28:52] [지마켓/카카오/ybbang0202@naver.com] [67/59]  | 배송중 | 3834021538 | 0원 | 노주현 | 롯데택배 | 24312646423
                page +=1
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
        return result  

    def InvoiceDetail_gmarket(self,ordNo):
        res = {}
        url = f'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo={ordNo}'
        # print(url)
        if url == 'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo=4970342921':
            res['prdNm'] = 'fuck'
            return res
        soup = BeautifulSoup(self.gmarket.get(url).text, 'lxml')
        # input(soup)
        print(url)
        try:
            res['prdNm'] = soup.select_one('#detailContents li.tit_info a').text
        except:
            res['prdNm'] = soup.select_one('#detailContents > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > ul > li.tit_info > a').text
        
        # res['detailurl'] = url

        try:
            res['name'] = soup.select_one('#shipInfoNameTd input')['value'].replace('\n','').replace('\t','').replace('\r','')
            res['addressnum'] = soup.select_one('#sz_zip_code')['value'].replace('\n','').replace('\t','').replace('\r','')
            res['address'] = soup.select_one('#detailContents > div:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > input[type=text]:nth-child(1)')['value']
            address1 = soup.select('input.address')[0]['value']
            address2= soup.select('input.address')[1]['value']
            res['address'] = address1 + address2
        except Exception:
            try:
                res['name'] = soup.select_one('#shipInfoNameTd').text.replace(' ','').replace('  ','').replace('\n','').replace('\t','').replace('\r','')
                res['addressnum'] = soup.select_one('#detailContents > div.detail_table_info.box__delivery.box__delivery-member > table > tbody > tr:nth-child(3) > td').text.split(']')[0].replace('[','').replace(' ','').replace('\n','').replace('\t','').replace('\r','')
                res['address'] = ''
            except Exception:
                res['prdNm'] = ''
                return res

        
        # address1 = soup.select('#detailContents > div:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > input')[3]['value']
        # address2 = soup.select_one('#detailContents > div:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > div > input')['value']
        # res['addressnum'] = soup.select('#detailContents > div:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > input')[0]['value']
        pay = soup.select('#detailContents > div:nth-child(3) > table:nth-child(3) > tbody > tr > td')
        if len(soup.select('div.detail_table_info table')) == 7:
            pay = soup.select('#detailContents > div:nth-child(3) > table:nth-child(4) > tbody > tr > td')
        try:
            res['pay'] = pay[1].text
            res['paytime'] = pay[4].text
            res['paydetail'] = pay[2].text
        except Exception:
            res['pay'] = ''
            res['paytime'] = ''
            res['paydetail'] = ''

        try:
            res['price'] = pay[5].text.replace(',','').replace('원','')
        except Exception:
            try:
                res['price'] = pay[4].text.replace(',','').replace('원','')
                res['paytime'] = pay[3].text
                res['paydetail'] = ''
            except Exception:
                try:
                    res['price'] = soup.select_one('td.info_price').text.replace(',','').replace('원','')
                except Exception:
                    res['price'] = 0
                    res['paytime'] = ''
                    res['paydetail'] = ''
            # input(res)
            # input(soup)
            # input(pay)
            # res['price'] = soup.select_one('td.info_price').text
        # print(res['price'])
        return res

    def deliveryCheck_gmarket(self,ordNo):
        url = f'https://myg.gmarket.co.kr/Popup/TrackingView?contractNo={ordNo}&DeliveryType=DELIVERY&isInternalizationDeliveryCompany=true&smileDelivery=N'
        # print(url)
        soup = BeautifulSoup(self.gmarket.post(url).text, 'lxml')
        # print(soup)
        res={'invoicenum':'','courier':''}
        if '아직 발송전' not in str(soup):
            try:
                f = soup.select_one('span.text__delivery-cooper').text.replace('\t','').replace('\r','')
                res['invoicenum'] = f.split(' ')[1]
                res['courier'] = f.split(' ')[0]
            except Exception:
                res['invoicenum'] = '추적서비스를제공하지않음'
                res['courier'] = '추적서비스를제공하지않음'

        return res
    def getName(self,ordNo):
        url = f'https://mc.coupang.com/ssr/api/destination-address/receiver?orderId={ordNo}'
        res = self.coupang.get(url).json()
        return res
    
    def CoupangLogin(self,info):
        '''쿠팡 로그인'''
    
        options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
        options.add_argument("disable-popup-blocking")
        options.add_argument("disable-notifications")
        options.add_argument("disable-gpu")  ##renderer timeout
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

        url = 'https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','login-email-input').send_keys(info['loginId'])
        self.driver.find_element('id','login-password-input').send_keys(info['loginPass'])
        
        self.driver.find_element('xpath','/html/body/div[2]/div/div/form/div[3]/div[1]/div[2]/div[1]/div[3]/button').click()
        time.sleep(4)
        self.driver.get('https://www.gmarket.co.kr/')
        time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))
        if '비밀번호를 다시' in str(self.driver.page_source):
            self.driver.close()
            self.driver.quit()      
            return False
        
        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()     
#GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓 