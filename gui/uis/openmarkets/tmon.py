import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao



class InvoiceCenterTmon(Kakao):

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '티몬'
        
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
                print(f'{self.wheretobuy} 세션 있음')
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    a = self.TmonLogin(self.info)
                    if a == False: 
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                        return False
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                continue
            

            # 쿠키를 확인하는 부분
            self.tmon = requests.Session()
            for cookie in cookies:    
                self.tmon.cookies.set(cookie['name'], cookie['value'])

            try:
                url =f'https://login.tmon.co.kr/user/buyInfo/buyList?type=all&deliveryStatus=ALL&page=1'
                print(url)
                res = self.tmon.get(url)

                soup = BeautifulSoup(res.text,'lxml')
                # input(soup)
                # soup.select_one('body > div.buy_lst > table > tbody > tr:nth-child(1) > th > div.date_num > p.buy_num > strong').text
                if '구매내역이 없습니다.' in str(soup):
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                    return False
                
                if '<html><head><script>document.location.reload();</script></head></html>' == str(soup):
                    if os.path.exists(self.cookiename):
                        os.remove(self.cookiename)
                    continue
                print('티몬 로그인 성공')
                break
            except Exception:
                print('tmon 세션 실패 재로그인')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    if a == False: 
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                        return False
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                continue
            
        # if total == 0:
        #     self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
        #     return False
        # if total == False: 
        #     self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
        #     return False
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
        return True

    def InvoiceCheck_tmon(self,info):
        self.info = info
        self.beforeclass = info['self']
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '옥션', 'loginId': 'kys980531', 'loginPass': 'qaz7410@@', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션옥션kys980531.pkl'}
        self.cookiename = self.info['cookiename']
        islogin = self.islogin()
        if islogin == False: return False

        # 여기까지 기본
        page = 1
        counter = 0
        result = []
        while True:
            url = f'https://login.tmon.co.kr/user/buyInfo/buyList?type=all&deliveryStatus=ALL&page={page}'
            print(url)
            
            res = self.tmon.get(url)
            soup = BeautifulSoup(res.text,'lxml')
            # print(soup)
            # input(soup)
            # soup.select_one('body > div.buy_lst > table > tbody > tr:nth-child(1) > th > div.date_num > p.buy_num > strong').text
            if '구매내역이 없습니다.' in str(soup):
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
                return result
            
            if '<html><head><script>document.location.reload();</script></head></html>' == str(soup):
                print('html 끝')
                return result
            
            if page > 50:
                print('페이징 끝')
                input(soup)
                return result

            res={'invoicenum':'','courier':'','cookiename':self.cookiename,'wheretobuy':self.wheretobuy,'address':''}
            for idx,i in enumerate(soup.select('div.buy_lst table tbody tr')):
                # input(i)

                try:
                    ordno  =i.select_one('div.date_num > p.buy_num > strong').text.replace('\n','').replace('\t','').replace('\r','')
                except Exception:
                    pass
                
                if idx != 0:
                    try:
                        if res['ordNo'] != ordno:
                            
                            # if res['courier'] != '': res['Status'] = '배송중'
                            print(res)
                            res['detailurl'] = '-'
                            res['cookiepath'] = self.cookiename
                            try:
                                res['addressnum'] = int(res['addressnum'])
                                res['addressnum'] = str(res['addressnum'])
                            except Exception:
                                res['addressnum'] = ''
                            result.append(res)
                            # input(len(result))
                            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                            res={'invoicenum':'','courier':'','cookiename':self.cookiename,'wheretobuy':self.wheretobuy,'address':''}

                            print(counter,page)
                            counter+=1
                    except Exception:
                        continue

                try:
                    imamd = soup.select('td.expiry > div')[counter]
                except Exception:
                    continue

                # input(imamd)
                prodnm = soup.select('div.tit > strong')[counter]
                try:
                    res['Status'] = (imamd.select_one('strong').text).replace('\n','').replace('\t','').replace('\r','').replace('                            ','').replace('            ','')
                except Exception:
                    res['Status'] = '환불완료'
                res['prdNm'] = prodnm.text.replace('\n','').replace('\t','').replace('\r','').replace('                                    ','').replace('                                ','')
                try:
                    
                    res['courier'] = (imamd.select_one('span a').get('href').split(',')[-1].replace(');','').replace("'",'').replace('"',''))
                    res['invoicenum'] = (imamd.select_one('span a').get('href').split(',')[-2].replace(');','').replace("'",'').replace('"',''))
                except Exception:
                    pass
                
                res['ordNo'] = ordno
                res['PayNo'] = ordno
                try:
                    res['prdNm'] = i.select_one('div.detail > div > strong').text.replace('\n','').replace('\t','').replace('\r','')
                except Exception:
                    pass
                try:
                    res['price'] = i.select_one('div.payment > p.won > em').text.replace(',','').replace('원','').replace('\n','').replace('\t','').replace('\r','')
                except Exception:
                    pass
                try:
                    res['pay'] = i.select_one(f'div.date_num > p.dt').text
                    res['paydetail'] = i.select_one(f'div.date_num > p.dt').text
                    res['paytime'] = i.select_one(f'div.date_num > p.dt').text

                except Exception:
                    pass
                # input(i)
                try:
                    res['name'] = i.select_one('p.addr > span:nth-child(2)').text.split(',')[0].replace(',','').replace('\n','').replace('\t','').replace('\r','')
                except Exception:
                    pass
                try:
                    res['addressnum'] = i.find('span',{'class':'adr'}).attrs['title'].split(')')[0].replace('(','').replace('\n','').replace('\t','').replace('\r','')
                    # print('여기요!')
                except Exception:
                    pass
                # print(res)
                # self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")

            page+=1
            counter = 0

        # self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
        # return result  


    def deliveryCheck_tmon(self,ordNo,invoicenum):
        url = f'https://www.tmon.com/p/delivery/deliverysearch/search?odNo={ordNo}&odSeq=1&invcNo={invoicenum}&procSeq=1'
        headers = {'accept':'application/json, text/plain, */*',
        'content-type':'application/json;charset=UTF-8'}
        data = {"odNo":ordNo}
        response = self.tmon.get(url,headers=headers).text.replace('\\','')
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
  
    
    def TmonLogin(self,info):
        '''지마켓 로그인'''
    
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        url = 'https://login.tmon.co.kr/user/loginform?return_url=&return_url=http%3A%2F%2Fbenefit.tmon.co.kr%2Fpromotions%2Fpage%2Fmembersignup'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','userid').send_keys(info['loginId'])
        self.driver.find_element('id','pwd').send_keys(info['loginPass'])
        
        self.driver.find_element('xpath','/html/body/div[1]/div[2]/div/form/a[2]').click()
        time.sleep(4)
        # self.driver.get('https://www.gmarket.co.kr/')
        if '일치하지' in str(self.driver.page_source):
            self.driver.close()
            self.driver.quit()      
            return False
        # time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))
        
        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()     
        return True
#GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓 