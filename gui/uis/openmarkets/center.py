import os
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from gui.uis.openmarkets.auction import InvoiceCenterAuction

from qt_core import *
# 031 330 6971
class InvoiceCenter(QThread):

    returnValue = Signal(dict)

    def __init__(self,info,parent=None):
        super().__init__()
        self.info = info
        

    def run(self):

        if self.info['market'] == '옥션':
            self.Auctionmaster = InvoiceCenterAuction().InvoiceCheck_auction(self.info)
            
        self.returnValue.emit({'result':10})
# ##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션    
#     def InvoiceCheck_auction(self,info):
#         # cookiename = '옥션카카오김영수'
#         self.application_path = '/Users/zerowater/Dropbox/zerowater/billy/DATA'
#         cookiename = info['cookiename']
#         page = 1
#         totalpage = 0
#         result = []


        
#         while True:
#             # print(cookiename)
#             # self.KakaoLogin(v,headless=False)
#             # input('dd')

#             for _ in range(5):
#                 try:
#                     cookies = pickle.load(open(cookiename, "rb"))
#                 except Exception:
#                     print('옥션 세션 없음')
#                     return {'result':False,'msg':'NO SESSION','info':info}
                    
#                 self.auction = requests.Session()
#                 input('쿠키확인1')
#                 for cookie in cookies:    
#                     print(cookie['name'], cookie['value'])
#                     self.auction.cookies.set(cookie['name'], cookie['value'])
#                     self.driver.add_cookie(cookie)
#                 self.driver.refresh()
#                 input('쿠키확인2')
#                 defaulturl = 'https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList'
#                 path = f'?pageIndex={page}&pageSize=10&searchPeriod=1M&searchStatus=ALL'
#                 url = '{}{}'.format(defaulturl,path)
#                 # print(url)
#                 # print(page,'페이지 시작')
#                 try:
#                     response = self.auction.get(url)
#                     # input(res.text)
#                 except Exception:
#                     # print('커넥션 에러')
#                     continue

#                 # input(response.text)
#                 if (response.text) == '':
#                     return result
#                 if 'action="./Logout.aspx' in response.text:
#                     # print('있음')
#                     print('옥션 세션 실패 재로그인')
#                     if info['loginType'] == '카카오':
#                         self.KakaoLogin(info)
#                     elif info['loginType'] == '옥션':
#                         self.AuctionLogin(info)
#                     continue
#                 try:
#                     res = response.json()
#                     # print('dd')
#                 except Exception:
#                     print('옥션 세션 실패 재로그인')
#                     if info['loginType'] == '카카오':
#                         self.KakaoLogin(info)
#                     elif info['loginType'] == '옥션':
#                         self.AuctionLogin(info)
#                     continue
# # https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList?pageIndex=1&pageSize=10&searchPeriod=1M&searchStatus=ALL
# # https://mmya.auction.co.kr/MyAuction/Order/GetMyOrderAndVirtualAccountList?pageIndex=1&pageSize=10&searchPeriod=1M&searchStatus=ALL
#                 break


#             # input(res)
#             total = res['orderList']['TotalOrderCount']
#             totalpage = m.ceil(total / 5)
#             print(f'{cookiename} 전체주문:',total,'현재 페이지:',page,'/',totalpage)
#             for i in res['orderList']['PayInfoList']:
                
#                 res={'invoicenum':'','courier':''}
#                 res['cookiename'] = cookiename
#                 res['wheretobuy'] = '옥션'
#                 res['price'] = int(str(i['TotalOrderAmount']).replace('.0',''))
#                 r = i['OrderList'][0]
#                 res['PayNo'] = r['PayNo']
#                 res['ordNo'] = str(r['OrderNo'])
#                 res['prdNm'] = r['ItemName']
#                 res['Status'] = r['Status']
#                 # print(res)
#                 # if res['ordNo'] == '1957321858':
#                 #     input(i)
#                 aaaa =self.InvoiceDetail_auction(r['OrderNo'])
#                 if aaaa:
#                     res.update(aaaa) # 디테일
#                 else:
#                     continue
                
#                 if '배송시작' in str(r['Status']) or '배송중' in str(r['Status']) or '배송완료' in str(r['Status']) or '오늘도착예정' in str(r['Status']):
#                     print('배송추적됨')
#                     res['Status'] = '배송중'
#                     res.update(self.deliveryCheck_auction(r['OrderNo'])) # 운송장 조회
                
#                 print(res)
#                 print('='*30)
#                 result.append(res)
#                 # break

#             if totalpage == page:
#                 print('모든 페이지 완료')
#                 # break
#                 return result

#             page+=1
#         return result

#     def InvoiceDetail_auction(self,ordNo):
#         res = {}
#         # ordNo= '2024187759'
#         url = f'https://ssl.auction.co.kr/Close/BuyAwardInfolayer.aspx?order_no={ordNo}'
#         print(url)
#         while True:
#             try:
#                 r =self.auction.get(url).text
#                 break
#             except Exception:
#                 continue

#         soup = BeautifulSoup(r, 'lxml')
#         # input(soup)
#         try:
#             d = soup.select('table.order-detail-table')[1].select('tr td')
#             res['name'] = d[0].text
#             res['addressnum'] = d[3].text.replace('\n','').replace('\t','').replace('\r','').split(']')[0].replace('[','')
#             res['address'] = d[3].text.replace('\n','').replace('\t','').replace('\r','').split(']')[1].replace('//','')
#             try:
#                 res['pay'] = (soup.select_one('#payInfoTbl div.msg').text.replace('\n','').replace('\t','').replace('\r',''))
#             except Exception:
#                 res['pay'] = '스마일 카드'
#                 # res['pay'] = soup.select_one('#payInfoTbl tr')#.text.replace('\n','').replace('\t','').replace('\r','')
#             res['paytime'] = soup.select_one('#uxazip > div.viply-veiw > div.uxc-vip-tit > div.num-date > p.bar > strong').text
#             res['paydetail'] = ''
#         except Exception:
#             return False
#         return res

#     def deliveryCheck_auction(self,ordNo):
#         url = f'http://escrow.auction.co.kr/Shipment/TraceItem.aspx?orderno={ordNo}'
#         # print(url)
#         soup = BeautifulSoup(self.auction.get(url).text, 'lxml')
#         # input(soup)
        
#         res={}
#         res['courier']=''
#         res['invoicenum']=''
#         try:
#             res['courier'] = soup.select_one('#contents > div > table > tbody > tr > td:nth-child(2)').text.replace('\n','').replace('\t','').replace('\r','')
#             res['invoicenum'] = soup.select_one('#contents > div > table > tbody > tr > td.font_tahoma').text.replace('\n','').replace('\t','').replace('\r','')
#         except:
#             try: 
#                 print(f'옥션 주문번호 문제 url 확인 {url}')
#                 res['courier'] = soup.select_one('#contents > div.myatable03.mtxxs > table > tbody > tr:nth-child(6) > td').text.replace('\n','').replace('\t','').replace('\r','')
#                 res['invoicenum'] = soup.select_one('#contents > div.myatable03.mtxxs > table > tbody > tr:nth-child(7) > td').text.replace('\n','').replace('\t','').replace('\r','')
#             except:
#                 pass

        
#         return res

#     def AuctionLogin(self,v,headless=True):
#         '''옥션 로그인'''
        
#         options = webdriver.ChromeOptions()
#         if headless:
#             options.add_argument("--headless")
#         self.driver = webdriver.Chrome(options=options)
#         # cookiename = 'G마켓카카오박예찬'
#         cookiename = info[6]
#         url = 'https://memberssl.auction.co.kr/Authenticate/?url=http%3a%2f%2fwww.auction.co.kr%2f&return_value=0'

#         self.driver.get(url),time.sleep(5)#,self.driver.implicitly_wait(10),time.sleep(2)
#         # input('pause')
#         self.driver.find_element_by_id('id').send_keys(info[1])
#         self.driver.find_element_by_id('password').send_keys(info[2])
#         try:
#             self.driver.find_element_by_xpath('/html/body/diinfo[2]/div/div/form/div/div/div/diinfo[1]/fieldset/button[1]').click()
#         except Exception:
#             self.driver.find_element_by_xpath('/html/body/diinfo[3]/div/div/form/div/div/div/diinfo[1]/fieldset/button[1]').click()

#             # input('a')  
#         time.sleep(8)#오순애
#         # input('사이트에 로그인 후 엔터를 누르세요.')

#         pickle.dump(self.driver.get_cookies() , open(cookiename,"wb"))


#         print('세션 저장 완료')
#         self.driver.close()
#         self.driver.quit() 
        
# ##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션##AUCTION 옥션

# if __name__ == '__main__':
#     info  = {'isAuth': 'True', 'groupId': '', 'mallName': '옥션', 'loginType': '카카오', 'loginId': 'kys980531@naver.com', 'loginPass': 'qaz7410', 'nickName': 'dPQkddlsp', 'memo': '메모장','naverId':'kys053123@naver.com','naverPass':'fkaustkfl12!'}
#     info['cookiename']= os.path.join('/Users/zerowater/Dropbox/zerowater/billy/DATA','COOKIE',info['mallName']+info['loginType']+info['loginId'].replace('.','').replace('@','')+'.pkl')
#     print(info)
#     InvoiceCenterAuction().InvoiceCheck_auction(info)