import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from gui.uis.windows.main_window.defpyqt import DefPyQt
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao


##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓
class InvoiceCenterGmarket(Kakao):

    def __init__(self):
        super().__init__()
        self.default = DefPyQt()
        
    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '지마켓'
        
        if '지마켓지마켓' in  self.cookiename:
            if os.path.isfile(self.cookiename):
                os.remove(self.cookiename)
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    a = self.GmarketLogin(self.info)
                    if a == False: 
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                        return False
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
                'searchStatus':'',
                'page':'1',
                'pageSize':'5',
            }
            res = self.gmarket.post('https://myg.gmarket.co.kr/ContractList/GeneralContractListAjax',data=data)
                # 주문이 없는 경우 추가해야함
                # self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
            # input(res.json())
            
            try:
                res = res.json()
                # break
            except Exception:
                if '로그인에 실패하였습니다.' in res.text:
                    print('지마켓 세션 만료')
                    if os.path.isfile(self.cookiename):
                        os.remove(self.cookiename)
                        
                    if self.info['loginType'] == '카카오':
                        self.isCookieLive(self.info)
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                    elif self.info['loginType'] == 'G마켓':
                        a = self.GmarketLogin(self.info)
                        if a == False: 
                            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                            return False
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                        continue
            # total = False
            try:
                total = res['total']
                print('전체주문:',total)
                self.total = total
            except TypeError:
                if 'G마켓 점검중!' in res.text:
                    print('서버 점검중')
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 지마켓 서버 점검중 ...""")
                    return False
            try:
                if total == 0:
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                    return False
            except UnboundLocalError:
                continue
            
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
        # 필터링
        # self.gmarket.post.('https://myg.gmarket.co.kr/ContractList/GetSumOfDeliveryStatusData',)
        failcount = 1
        result = []
        # for serachStatus in ['ORDER_ING','CLAIM_ING','DELIVERY_CMPL','ORDER_ING']:
        for serachStatus in ['']:
            page = 1
            while True:
                data = {
                        # 'searchSDT': '2021-09-29',
                        # 'searchEDT': '2021-10-28',
                        'searchStatus':serachStatus,
                        'page':str(page),
                        'pageSize':'5',
                    }
                # print(data)
                print('현재페이지:',page)
                    
                try:
                    res = (self.gmarket.post('https://myg.gmarket.co.kr/ContractList/GeneralContractListAjax',data=data))
                    res = res.json()
                    # input(res)
                except Exception:
                    print('지마켓 실패')
                    if failcount == 1: 
                        failcount +=1
                        continue
                    else: return False

                try:
                    total = res['total']
                    print('전체주문:',total)
                except TypeError:
                    if 'G마켓 점검중!' in res.text:
                        print('서버 점검중')
                        return []
                try:
                    if len(res['data']) == 0:
                        print('데이터가 비어있음 페이지:',page)
                        break
                except Exception:
                    return []
                

                for i in res['data']:
                    # input(i)
                    res={'invoicenum':'','courier':''}
                    # res['billiid'] = self.info['billiid']
                    res['cookiename'] = self.cookiename
                    res['cookiepath'] = self.cookiename
                    res['wheretobuy'] = self.wheretobuy
                    res['PayNo'] = i['RefNo'] # 주문 번호

                    res['ordNo'] = i['RefNo'] # 주문 번호
                    # res['detailurl'] = f'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo=5078166660'
                    # print(res['ordNo'])
                    # if res['ordNo'] == '3703997096':
                    #     continue
                    # if res['ordNo'] == '4970342921':
                    #     continue
                    res['Status'] = i['Status']
                    if i['Status'] == 'DeliveryReady':
                        res['Status'] = '배송대기'
                    if i['Status'] == 'DeliveryRequest':
                        res['Status'] = '배송요청'
                    if i['Status'] == 'DeliveryStart':
                        res['Status'] = '배송시작'
                    if i['Status'] == 'DeliveryInToday':
                        res['Status'] = '오늘도착'
                    if i['Status'] == 'DeliveryCmplWait':
                        res['Status'] = '배송완료대기'
                    if i['Status'] == 'DeliveryCmpl':
                        res['Status'] = '배송완료'
                    if i['Status'] == 'DeliveryIng':
                        res['Status'] = '배송중'
                    if i['Status'] == 'ClaimCancelCmpl':
                        res['Status'] = '반품취소완료'
                    if i['Status'] == 'ClaimReturnCmpl':
                        res['Status'] = '반품완료'
                    if i['Status'] == 'ClaimReturnRequest':
                        res['Status'] = '반품요청'
                    res['CartNo'] = i['CartNo'] #지마켓 장바구니로 구분함 디테일을
                    res['detailurl'] = f'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo={i["CartNo"]}'
                    # print(i['RefNo'])
                    # print(i['ThirdColumn'])
                    if '배송추적' in str(i['ThirdColumn']):
                        # print('배송추적됨')
                        res.update(self.deliveryCheck_gmarket(i['RefNo'])) # 운송장 조회

                    res.update(self.InvoiceDetail_gmarket(i['CartNo'])) # 디테일
                    # try:
                    # except Exception:
                    #     continue
                    if res['prdNm'] == '': continue
                    result.append(res)
                    print(res)
                    print('===='*10)
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/{total}] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                    # break
                    # total 맞춰야함 ;;;;;; 지금바로할것 
                    # [18:28:52] [지마켓/카카오/ybbang0202@naver.com] [67/59]  | 배송중 | 3834021538 | 0원 | 노주현 | 롯데택배 | 24312646423
                page +=1
                # if page == 2: break
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
        return result  

    def InvoiceDetail_gmarket(self,ordNo):
        res = {}
        url = f'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo={ordNo}'
        # url = 'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo=5079464275'
        # print(url)
        if url == 'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo=4970342921':
            res['prdNm'] = 'fuck'
            return res
        # url = 'https://myg.gmarket.co.kr/Contract/ContractDetail?cartNo=5098480791'
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
                res['address'] = soup.select_one('#detailContents > div.detail_table_info.box__delivery.box__delivery-member > table > tbody > tr:nth-child(3) > td').text.split(']')[1].replace(' ','').replace('\n','').replace('\t','').replace('\r','')
            except Exception:
                res['prdNm'] = ''
                return res

    
        try:
            res['pay'] = '스마일페이'
            res['paytime'] = soup.select_one('body > div.detail_wrap > div.top > p > span.tit_date').text.replace('\n','').replace('\t','').replace('\r','')
            res['paydetail'] = ''
            res['price'] = (str(soup.select_one('table.last_price td.last_num > strong').text).replace('\n','').replace('\t','').replace('\r','').replace('\n','').replace('\t','').replace('\r','').replace("2.innerText = '",'').replace("'",'').replace(',','').replace('원','').rstrip().lstrip().strip())
            res['price'] = res['price'].replace('\n','').replace('\r','').replace('\t','').rstrip().lstrip().replace('원','')
            return res
        except Exception:
            pass
        
        pay = soup.select('#detailContents table.w_table_grey tbody tr td')
        if len(pay) == 0: 
            pay = soup.select('#CashPlusPayTable > thead > tr:nth-child(2) td:nth-child(2)')
            try:
                res['pay'] = (str(soup.select('script')[-2]).replace('\n','').replace('\t','').replace('\r','').split('newCell')[5].replace('1.innerText = "','').replace('\n','').replace('\t','').replace('\r','').replace('";','').rstrip().lstrip().strip())
                res['paytime'] = (str(soup.select('script')[-2]).replace('\n','').replace('\t','').replace('\r','').split('newCell')[5].replace('1.innerText = "','').replace('\n','').replace('\t','').replace('\r','').replace('";','').rstrip().lstrip().strip())
                res['paydetail'] = (str(soup.select('script')[-2]).replace('\n','').replace('\t','').replace('\r','').split('newCell')[5].replace('1.innerText = "','').replace('\n','').replace('\t','').replace('\r','').replace('";','').rstrip().lstrip().strip())
                res['price'] = (str(soup.select('script')[-2]).replace('\n','').replace('\t','').replace('\r','').split('newCell')[6].replace('\n','').replace('\t','').replace('\r','').split(';')[0].replace("2.innerText = '",'').replace("'",'').replace(',','').replace('원','').rstrip().lstrip().strip())
                res['price'] = res['price'].replace('\n','').replace('\r','').replace('\t','').rstrip().lstrip().replace('원','')
                return res
            except Exception:
                pass
        try:
            res['pay'] = pay[1].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
            res['paytime'] = pay[4].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
            if '원' in res['paytime']: res['paytime'] = pay[3].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
            res['paydetail'] = pay[2].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
        except Exception:
            res['pay'] = pay[0].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
            res['paytime'] = pay[1].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
            res['paydetail'] = pay[1].text.replace('\n','').replace('\t','').replace('\r','').rstrip().lstrip()
            # input(len(soup.select('div.detail_table_info table')))

        try:
            res['price'] = pay[5].text.replace(',','').replace('원','')
        except Exception:
            try:
                res['price'] = pay[4].text.replace(',','').replace('원','')
            except Exception:
                try:
                    res['price'] = soup.select_one('td.info_price').text.replace(',','').replace('원','')
                except Exception:
                    res['price'] = soup.select_one('td.last_num').text.replace(',','').rstrip().lstrip().replace('원','')

        res['price'] = res['price'].replace('\n','').replace('\r','').replace('\t','').rstrip().lstrip().replace('원','')
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
  
    
    def GmarketLogin(self,info):
        '''지마켓 로그인'''
        
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        url = 'https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','id').send_keys(info['loginId'])
        self.driver.find_element('id','pwd').send_keys(info['loginPass'])
        
        self.driver.find_element('xpath','/html/body/div[2]/div/div/form/div[3]/div[1]/div[2]/div[1]/div[3]/button').click()
        time.sleep(4)
        if '로그인에 실패했' in str(self.driver.page_source):
            self.driver.close()
            self.driver.quit()      
            return False
        if 'GetAuthMethod' in str(self.driver.current_url):
            while True:
                if 'GetAuthMethod' not in str(self.driver.current_url):
                    break
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 지마켓 2차인증을 진행해주세요.""")
                time.sleep(2)

            return True
        
        self.driver.get('https://www.gmarket.co.kr/')
        time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))
        
        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()     
#GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓 