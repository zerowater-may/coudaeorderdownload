import os
from urllib import parse, response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

class InvoiceCenterAliexpress(Kakao):

    def loginforali(self,type=False):
        '''알리익스프레스 개빡쎔'''
        if type == False:
            # Enable Performance Logging of Chrome.
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        
            # Create the webdriver object and pass the arguments
            options = webdriver.ChromeOptions()
        
            # Chrome will start in Headless mode
            # options.add_argument('headless')
        
            # Ignores any certificate errors if there is any
            options.add_argument("--ignore-certificate-errors")
        
            # Startup the chrome webdriver with executable path and
            # pass the chrome options and desired capabilities as
            # parameters.
            self.driver = webdriver.Chrome(
                                    chrome_options=options,
                                    desired_capabilities=desired_capabilities)
            # Send a request to the website and let it load
            self.driver.get('https://ko.aliexpress.com'),self.driver.implicitly_wait(10),time.sleep(2)
            cookies = pickle.load(open(self.cookiename, "rb"))
            for cookie in cookies:    
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            self.aliexpress = requests.Session()
            for cookie in self.driver.get_cookies():    
                self.aliexpress.cookies.set(cookie['name'], cookie['value'])
        
            # Sleeps for 10 seconds
            time.sleep(5)
            self.driver.get("https://www.aliexpress.com/p/order/index.html")
        else:
            self.driver.get("https://www.aliexpress.com/p/order/detail.html")
        time.sleep(5),self.driver.implicitly_wait(10)
        if 'login.aliexpress.com' in self.driver.current_url:
            print('로그인이 되지않음')
            return False

        # 주문더보기 클릭
        try:
            elem = self.driver.find_element('css selector','button.comet-btn.comet-btn-large.comet-btn-borderless')
            elem.location_once_scrolled_into_view
            # input('pause')
            elem.click()
            ismanyorders = True
        except Exception:
            print('주문더보기 없음')
            ismanyorders = False


        time.sleep(5)
        # Gets all the logs from performance in Chrome
        logs =  self.driver.get_log("performance")
        # input(logs)
        # Opens a writable JSON file and writes the logs in it
        with open("network_log.json", "w", encoding="utf-8") as f:
            f.write("[")
    
            # Iterates every logs and parses it using JSON
            for log in logs:
                network_log = json.loads(log["message"])["message"]
                # print(log)
                # Checks if the current 'method' key has any
                # Network related value.
                if("Network.response" in network_log["method"]
                        or "Network.request" in network_log["method"]
                        or "Network.webSocket" in network_log["method"]):
    
                    # Writes the network log to a JSON file by
                    # converting the dictionary to a JSON string
                    # using json.dumps().
                    f.write(json.dumps(network_log)+",")
            f.write("{}]")
    
        print("Quitting Selenium WebDriver")
        # self.driver.quit()
    
        # Read the JSON File and parse it using
        # json.loads() to find the urls containing images.
        json_file_path = "network_log.json"
        with open(json_file_path, "r", encoding="utf-8") as f:
            logs = json.loads(f.read())
    
        # Iterate the logs
        if ismanyorders:
            for log in logs:
                try:
                    if 'buyer.order.list' in str(log):
                        # input(log)
                        url = log["params"]["request"]["url"]
                        if 'buyer.order.list' in url and type == False:
                            if log["params"]["request"]["method"] == 'POST':
                                input(log)
                                self.postData = log["params"]["request"]["postData"]
                                self.headers = log["params"]["request"]["headers"]
                                self.url = log["params"]["request"]["url"]
                                # response = self.aliexpress.post(url,headers=headers,data=postData)
                                # soup = BeautifulSoup(response.text,'lxml')
                                # input(soup)
                except Exception:
                    pass

        for log in logs:
            # Except block will be accessed if any of the
            # following keys are missing.
            # input(log)
            try:
                # URL is present inside the following keys
                url = log["params"]["request"]["url"]
                # print(url)
                # if 'acs.aliexpress.com' in url:
                if 'buyer.order.list' in url and type == False:
                    # input(log)
                    print('appKey:@@@@@@@@@@@@@@',url.split('&')[1]+'&'+url.split('&')[2]+'&'+url.split('&')[3])
                    return url.split('&')[1]+'&'+url.split('&')[2]+'&'+url.split('&')[3]

                if 'buyer.order.detail' in url and type == 'detail':
    
                    print('appKey:buyer.order.detail',url.split('&')[1]+'&'+url.split('&')[2]+'&'+url.split('&')[3])
                    return url
                    return url.split('&')[1]+'&'+url.split('&')[2]+'&'+url.split('&')[3]

                # # Checks if the extension is .png or .jpg
                # if url[len(url)-4:] == ".png" or url[len(url)-4:] == ".jpg":
                #     print(url, end='\n\n')
            except Exception as e:
                pass

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        # from selenium import webdriver
        # import time
        # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        # # import chromedriver_binary # If you're using conda like me.

        # yoururl = 'https://best.aliexpress.com/'

        # caps = DesiredCapabilities.CHROME
        # caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        # driver = webdriver.Chrome(desired_capabilities=caps)

        # driver.get(yoururl)
        # time.sleep(10) # wait for all the data to arrive. 
        # perf = driver.get_log('performance')
        # print(perf)
        # input('pause')
        self.wheretobuy = '알리익스프레스'
        
        for _ in range(2):
            try:
                # if os.path.exists(self.cookiename):
                #     os.remove(self.cookiename)
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
                print(f'{self.wheretobuy} 세션 있음')
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    a = self.AliexpressLogin(self.info)
                    if a == False: 
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                        return False
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                continue

            # input(alipayload)
            # self.driver = self.driver = webdriveWr.Chrome()
            # self.driver.get('https://ko.aliexpress.com'),self.driver.implicitly_wait(10),time.sleep(2)
            # for cookie in cookies:    
            #     self.driver.add_cookie(cookie)
            # self.driver.refresh()
            
            # # input('확인좀')
            # pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))
            # # input('확인좀1')
            # # # 쿠키를 확인하는 부분
            # cookies = self.driver.get_cookies()
            
    
            self.alipayload = self.loginforali()
            if self.alipayload == False:
                print('로그인이 되지않아서 다시 하기')
                os.remove(self.cookiename)
                continue
            
            self.aliexpress = requests.Session()
            for cookie in self.driver.get_cookies():    
                self.aliexpress.cookies.set(cookie['name'], cookie['value'])
            
            # self.driver.quit()
            # self.aliexpress = HTMLSession()
            # for cookie in cookies:    
                # self.aliexpress.cookies.set(cookie['name'], cookie['value']) 

            try:
                # alipayload = 'appKey=24815441t=1669737584699sign=495e49827e25d882925ed5482561078a'
                # url ='https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.list/1.0/?jsv=2.5.1&appKey=12574478&t=1669739689382&sign=e69fcae90f51e75a3212c2ea8e335e8c&api=mtop.aliexpress.trade.buyer.order.list&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22statusTab%22%3Anull%2C%22renderType%22%3A%22init%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D'
                url = f'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.list/1.0/?jsv=2.5.1&{self.alipayload}&api=mtop.aliexpress.trade.buyer.order.list&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22statusTab%22%3Anull%2C%22renderType%22%3A%22init%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D'
                
                # url ='https://ko.aliexpress.com/'
                print(url)
                self.driver.get(url)
                # response = self.aliexpress.get(alipayload)
                response = self.aliexpress.get(url)

                soup = BeautifulSoup(response.text,'lxml')
                # input(soup)
                # 로그인하십시오
                try:
                    res = json.loads(eval(json.dumps(str(soup).replace('<html><body><p>mtopjsonp1(','').replace(')</p></body></html>',''))))
                    print(res['ret'])
                    if 'SUCCESS' in res['ret'][0]:
                        print(f'{self.wheretobuy} 로그인 성공')
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
                        return True
                    
                    elif 'FAIL' in res['ret'][0]:
                        print(f'{self.wheretobuy} 로그인 fail')
                        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                        return False
                    
                except Exception:
                    print(f'{self.wheretobuy} 로그인 fail')
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패했습니다. 확인해주세요""")
                    return False
                

                if '구매내역이 없습니다.' in str(soup):
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                    return False
                
                    continue
                break
            except Exception:
                print(f'{self.wheretobuy} 세션 실패 재로그인')
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
        

    def InvoiceCheck_aliexpress(self,info):
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
            if page == 1:
                url = f'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.list/1.0/?jsv=2.5.1&{self.alipayload}&api=mtop.aliexpress.trade.buyer.order.list&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22statusTab%22%3Anull%2C%22renderType%22%3A%22init%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D'
                # url = 'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.list/1.0/?jsv=2.5.1&appKey=12574478&t=1671630276526&sign=a33b763838d961aaa9342b25f7e031a8&api=mtop.aliexpress.trade.buyer.order.list&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22statusTab%22%3Anull%2C%22renderType%22%3A%22init%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D'
                print(url)
                response = self.aliexpress.get(url)
                soup = BeautifulSoup(response.text,'lxml')
                soup = json.loads(eval(json.dumps(str(soup).replace('<html><body><p>mtopjsonp1(','').replace(')</p></body></html>',''))))
                with open('page1data.json', 'w', encoding='utf-8') as f:
                    json.dump(soup, f)
                input(soup)
            else:
                # self.alipayload = self.loginforali() # list appKey를 다시 받아야함
                url = f'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.list/1.0/?jsv=2.5.1&{self.alipayload}&v=1.0&post=1&type=originaljson&timeout=15000&dataType=originaljsonp&isSec=1&ecode=1&api=mtop.aliexpress.trade.buyer.order.list&method=POST&needLogin=true'
                # url = f'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.list/1.0/?jsv=2.5.1&{self.alipayload}&v=1.0&post=1&type=originaljson&timeout=15000&dataType=originaljsonp&isSec=1&ecode=1&api=mtop.aliexpress.trade.buyer.order.list&method=POST&needLogin=true'
                input(url)
                nextdata = {
                        'params':{
                            'data':{'pc_om_list_body_109702':soup['data']['data']['pc_om_list_body_109702']},
                            'linkage':soup['data']['linkage'],
                            'hierarchy':soup['data']['hierarchy'],
                            'endpoint':soup['data']['endpoint'],
                            'operator':'pc_om_list_body_109702',
                            }
                            }
                nextdata['params']['data']['pc_om_list_body_109702']['fields']['pageIndex'] = page
                nextdata['params']['hierarchy'].pop('component')
                nextdata['params']['hierarchy'].pop('root')
                # input((nextdata))
                headers= {'Accept': 'application/json', 'Content-type': 'application/x-www-form-urlencoded', 'Referer': 'https://www.aliexpress.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
                # response = self.aliexpress.post(url,headers=headers,data=json.dumps(nextdata))
                input(self.postData)
                response = self.aliexpress.post(self.url,headers=self.headers,data=self.postData)
                soup = BeautifulSoup(response.text,'lxml')
                soup = json.loads(eval(json.dumps(str(soup).replace('<html><body><p>','').replace('</p></body></html>',''))))
                input(soup)
                with open('page2data.json', 'w', encoding='utf-8') as f:
                    json.dump(soup, f,ensure_ascii=False)
            page +=1
            # print(url)

            # # soup.select_one('body > div.buy_lst > table > tbody > tr:nth-child(1) > th > div.date_num > p.buy_num > strong').text
            # if '구매내역이 없습니다.' in str(soup):
            #     self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")
            #     return result

            # if page > 50:
            #     print('페이징 끝')
            #     input(soup)
            #     return result
            
            # hasMore = soup['data']['data']['pc_om_list_body_109702']['fields']['hasMore']
            # print('hasmore:',hasMore)

            # queryParams = soup['data']['linkage']['common']['queryParams']
            # submitParams = soup['data']['linkage']['common']['submitParams']
            # validateParams = soup['data']['linkage']['common']['validateParams']

            # self.alipayload = self.loginforali(type='detail') # detail appKey를 다시 받아야함
            # for index,i in enumerate((soup['data']['data'])):
            #     res={'invoicenum':'','courier':'','cookiename':self.cookiename,'wheretobuy':self.wheretobuy,'address':''}
            #     if 'pc_om_list_order_' not in str(i): continue
            #     # res['ordNo'] = i[f'pc_om_list_order_{}']
            #     res['ordNo'] = i.split('_')[-1] 
            #     res['detailurl'] = url
            #     res['cookiepath'] = self.cookiename
            #     de = soup['data']['data'][f'pc_om_list_order_{res["ordNo"]}']['fields']
            #     res['prdNm'] = de['orderLines'][0]['itemTitle']
            #     res['price'] = de['totalPriceText']
            #     res['detailurl'] = de['orderDetailUrl']
            #     res['paytime'] = de['orderDateText']
            #     res['pay'] = de['orderDateText']
            #     res['paydetail'] = de['orderDateText']
            #     res['Status'] = de['statusText']
            #     res.update(self.deliveryCheck_aliexpress(res['ordNo']))
            #     print(res)
            #     print(f'페이지:{page} | {index}/{len(soup["data"]["data"])}')
            #     print('==='*30)
            # page+=1

    def deliveryCheck_aliexpress(self,ordNo):
        res = {}
        # input(ordNo)
        # url = f'''https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.detail/1.0/?jsv=2.5.1&'''+self.alipayload+'''&api=mtop.aliexpress.trade.buyer.order.detail&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data='''+parse.quote('''{"tradeOrderId":"'''+ordNo+'''","clientPlatform":"pc","timeZone":"GMT+0900"}''')
        url = f'''https://track.aliexpress.com/logistic/getDetail.json?tradeId={ordNo}'''
        print(url)
        # 'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.detail/1.0/?jsv=2.5.1&https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.detail/1.0/?jsv=2.5.1&appKey=12574478&t=1669955475700&sign=6daf32caf023fb353964995497924d37&api=mtop.aliexpress.trade.buyer.order.detail&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22tradeOrderId%22%3A%228159321113046223%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D&api=mtop.aliexpress.trade.buyer.order.detail&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22tradeOrderId%22%3A%228159320151586223%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D'
        # 'https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.detail/1.0/?jsv=2.5.1&https://acs.aliexpress.com/h5/mtop.aliexpress.trade.buyer.order.detail/1.0/?jsv=2.5.1&appKey=12574478&t=1669955475700&sign=6daf32caf023fb353964995497924d37&api=mtop.aliexpress.trade.buyer.order.detail&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22tradeOrderId%22%3A%228159321113046223%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D&api=mtop.aliexpress.trade.buyer.order.detail&method=GET&v=1.0&needLogin=true&timeout=15000&dataType=originaljsonp&type=originaljsonp&callback=mtopjsonp1&data=%7B%22tradeOrderId%22%3A%228158993743616223%22%2C%22clientPlatform%22%3A%22pc%22%2C%22timeZone%22%3A%22GMT%2B0900%22%7D'
        # url = self.alipayload
        self.driver.get(url)
        # input(url)
        response = self.aliexpress.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        # input(soup)
        soup = json.loads(eval(json.dumps(str(soup).replace('<html><body><p>','').replace('</p></body></html>',''))))
        print(soup)
        
        return res
    
    def AliexpressLogin(self,info):
        '''알리익스 로그인'''
    
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
            
        self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        url = 'https://login.aliexpress.com/?return_url=https%3A%2F%2Fm.aliexpress.com%2Faccount%2Findex.html%3Fspm%3Da2g0n.best.header.3.5279423a29wl6Y'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        # input('pause')
        self.driver.find_element('id','fm-login-id').send_keys(info['loginId'])
        self.driver.find_element('id','fm-login-password').send_keys(info['loginPass'])
        
        self.driver.find_element('xpath','/html/body/div[2]/div/div/div[1]/div[2]/div/div/button[2]').click()
        time.sleep(4)
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 2차인증 또는 슬라이드를 밀고 창이 닫힐 때 까지 기다려주세요.""")
        while True:
            if 'aliexpress.com/account/index.html' in str(self.driver.current_url):
                print('대기중')
                break
            
        # self.driver.get('https://www.gmarket.co.kr/')
        # if '암호가 잘못' in str(self.driver.page_source):
        #     self.driver.close()
        #     self.driver.quit()      
        #     return False
        # input('ss')
        # time.sleep(4)
        # input('사이트에 로그인 후 엔터를 누르세요.')
        self.driver.get('https://ko.aliexpress.com/?spm=a2g0s.buyerloginandregister.0.0.144655a3h5AzUF&gatewayAdapt=glo2kor'),self.driver.implicitly_wait(10),time.sleep(3)
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))
        print('세션 저장 완료')
        self.driver.close()
        self.driver.quit()     
        return True
#GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓 