
from http import cookies
import json
import os
from random import betavariate
from bs4 import BeautifulSoup
from selenium import webdriver
import pickle,time
import requests

from config import ConfigFile
from .naverlogin import Naver

class Kakao:
    def __init__(self):
        self.config = ConfigFile()
        self.naver = Naver()
        self.application_path = self.config.read()['system']['dir']
        # print('러러러',self.application_path)
        self.driver = None
    def close(self):
        try:
            self.driver.close()
            self.driver.quit()
            self.driver = None
        except Exception:
            pass

    def kakaologinmaster(self,info,onlylogin=False):
        while True:
            iscookie = self.isCookieLive(info,iscookielive=True)
            if iscookie: # 쿠키랑 세션이랑 한번에 확인하기
                print('쿠키가 있음.')
                issessionalive = self.isCookieLive(info,issessionlive=True)
                print(issessionalive)
                if issessionalive['result']:
                    print('쿠키가 있고 세션이 살아있음')
                    print(issessionalive)
                    if onlylogin: 
                        
                        if self.seleniumLogin(info) == 'ANOTHER LINK': continue
                        return True
                else:
                    print('쿠키가 없고 세션이 죽었음.')
                    if onlylogin: return False
                    if self.seleniumLogin(info) == 'ANOTHER LINK': continue
            else:
                print('쿠키가없음')
                if onlylogin: return False
                if self.seleniumLogin(info) == 'ANOTHER LINK': continue
            return True


    def set_driver(self,headless=False):
        if self.driver == None:
            print('실행중인 크롬이없으므로 실행함')
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('headless')
            options.add_argument('no-sandbox') # 크롬일 경우
            options.add_argument('disable-dev-shm-usage')
            # options.add_argument(f'--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25')
            self.driver = webdriver.Chrome(options=options)
            print(self.driver)
        print('실행중인 크롬이있음')

    def login(self,info,value=False):
        url = "https://accounts.kakao.com/kakao_accounts/login.json"

        payload = {
            'email':info['loginId'],
            'password':info['loginPass'],
        }

        response = requests.request("POST", url, data=payload)

        jsondata = (response.json())
        print(jsondata)
        if value: return jsondata
        if jsondata['status'] == -451:
            return True
        return False
    
    def find_elem(self,by,elem,value=False):
        try:
            element = self.driver.find_element(by,elem)
            element.location_once_scrolled_into_view

            if value:
                element.send_keys(value)

            element.click()
            return True
        except Exception:
            return False
    
    def isCookieLive(self,info,headless=False,driver=None,iscookielive=False,issessionlive=False):
        
        if iscookielive == False:
            self.set_driver(info['headless'])

        kakaocookiename = info['cookiename'].replace(os.path.basename(info['cookiename']),os.path.basename(info['cookiename']).replace(info['mallName'],''))
        # kakaocookiename = r'C:\Users\user\Dropbox\zerowater\billy\DATA\COOKIE1\카카오ybbang0202navercom.pkl'
        print(kakaocookiename,'카카오쿠키네임')
        try:
            cookies = pickle.load(open(kakaocookiename, "rb"))
            if iscookielive: return {'result':True,'msg':'IS SESSION','info':info}
        except Exception:
            print(f'{info["cookiename"]} / {kakaocookiename} 세션 없음')
            return {'result':False,'msg':'NO SESSION','info':info}

        if issessionlive: # 세션이 살아있는지 확인 
            url='https://developers.kakao.com/'
            self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
            # with open('output.json', 'w') as f:
            #     json.dump(json_object, f, indent=2)

            # with open('islogin1.txt','w',encoding='utf8') as f:
            #     f.write(str(self.driver.page_source))
            # input('함 ?')
            print('로그인 체크 해보세요')

            for cookie in cookies:    
                self.driver.add_cookie(cookie)
            
            self.driver.refresh()
            time.sleep(1)
            # with open('islogin2.txt','w',encoding='utf8') as f:
            #     f.write(str(self.driver.page_source))
            soup = BeautifulSoup(self.driver.page_source,'html.parser')
            islogin = json.loads(eval(json.dumps(str(soup.select_one('script#__NEXT_DATA__')).replace('<script id="__NEXT_DATA__" type="application/json">','').replace('</script>',''))))['props']['pageProps']['developer']
            # input(islogin)
            print('디벨롭 현재 로그인 상태 :',islogin)
            if islogin == None:
                print('로그인이 되지않았음.')
            # if '로그아웃' not in self.driver.page_source:
                return {'result':False,'msg':'NO SESSION','info':info}
            print('로그인이 되었음.')
            print(islogin)
            return {'result':True,'msg':'ALIVE','info':info}
        # print('카카오인지확인')
        # input(info['cookiename'])
        if '카카오' in info['cookiename']:



            url='https://developers.kakao.com/'
            self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)

            for cookie in cookies:    
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            if 'btn_email' not in self.driver.page_source:
                return {'result':False,'msg':'NO SESSION','info':info}
            # input(info)
            if info['mallName'] == 'G마켓' or info['mallName'] == '지마켓':
                url = 'https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/'
                loginbutton = '/html/body/div[2]/div/div/form/div[3]/div[1]/div[2]/div[2]/div[1]/a[1]'
            if info['mallName'] == 'SSG':
                url = 'https://member.ssg.com/member/popup/popupLogin.ssg?originSite=https%3A//www.ssg.com&t=&gnb=login&retURL=https%3A%2F%2Fwww.ssg.com%2F'
                loginbutton = '/html/body/div[1]/div/div/div/div[2]/div[1]/form/ul/li[2]/a/span[1]/span'
                # loginbutton = '/html/body/div[1]/div/div/div/div[2]/div[1]/form/ul/li[2]/a'
            if info['mallName'] == '인터파크':
                url = 'https://accounts.interpark.com/login/form'
                # url = 'https://accounts.interpark.com/authorize/shop-pc?origin=http%3A%2F%2Fwww.interpark.com&postProc=IFRAME'
                loginbutton = '/html/body/form[1]/div/div/div[2]/a[2]'
            if info['mallName'] == '옥션':
                loginbutton = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/div[3]/button'
                url = 'https://memberssl.auction.co.kr/Authenticate/?url=http%3a%2f%2fwww.auction.co.kr&return_value=0'
            if info['mallName'] == '롯데온':
                url = 'https://www.lotteon.com/p/member/login/common?rtnUrl=https://www.lotteon.com/p/order/mylotte/orderDeliveryList'
                loginbutton = '/html/body/div[1]/main/div/div[1]/div/div[4]/button[1]/span'
                # loginbutton = '/html/body/div[1]/main/div[1]/div/div/div[4]/button[1]/span'
            if info['mallName'] == '11번가':
                url = 'https://login.11st.co.kr/auth/front/login.tmall?returnURL=https%3A%2F%2Fwww.11st.co.kr%2F%3Fgclid%3DEAIaIQobChMIzra5ucGY-QIVQcuWCh2S1wYaEAAYASAAEgLZVfD_BwE%26utm_term%3DE_11%25B9%25F8%25B0%25A1.%26utm_campaign%3D%25C0%25CF%25C4%25A1%2BPC%26utm_source%3D%25B1%25B8%25B1%25DB_PC_S%26utm_medium%3D%25B0%25CB%25BB%25F6'
                loginbutton = '/html/body/div/form[1]/fieldset/div[4]/section/ul/li[1]/a/span'
            
            if info['mallName'] == '알리익스프레스':
                url = 'https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26redirect_uri%3Dhttp%253A%252F%252Fthirdparty.aliexpress.com%252Fkakaocallback.htm%26state%3DKP1XFbZhjt6TZ1trBHYHWdSHdNzHwT6HdVk58rsknORCMqe7rKJ0npt8bAEl0of7ETa%252BK%252F8A7arIpO2FyIk7q2C%252FJDRxz1f4jO2AGCQ0GyBzkxRHtOxDCnsY16McleQcbGhdNT8nsFPaAfK3r6Q8eBGlIw1bg5EsRgHI0BY7xrged8lVHxxKWzo7zv9X8j5ZTPlIpwMlPmVV82GJIaeH0w%253D%253D%26through_account%3Dtrue%26client_id%3D85049409d359d55bcd989753cdaf3a93'
                loginbutton = '/html/body/div/form[1]/fieldset/div[4]/section/ul/li[1]/a/span'
            
            # if info['mallName'] == 'NS몰':
            #     url = 'https://www.nsmall.com/LogonForm?catalogId=97001&langId=-9&storeId=13001&form=&loginGubun=2&url=https%3A%2F%2Fwww.nsmall.com%2F&scrollYn=&func=&isMemBtn=&nonMemberNoPurchase=N'
            #     loginbutton = '/html/body/div[1]/div/div[6]/div/div[2]/ul/li[3]/a'
            # if info['mallName'] == '나100샵':
            #     url = 'https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.na100shop.com%253A433%252FkakaoLogin%26client_id%3Dd012dc5d531139cc9cf9699f9a967aea'
                                
            self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        
            try:
                alert = self.driver.switch_to_alert()
                alert.accept()
            except Exception:
                pass
            
            # self.driver.find_element_by_class_name('.openid.kakao').click(),time.sleep(3)
            try:
                self.find_elem('xpath',loginbutton)
                time.sleep(3)
            except Exception:
                pass       
            pickle.dump(self.driver.get_cookies() , open(info['cookiename'],"wb"))
            print(info['cookiename'],'세션 저장 완료')
            self.close()
            # input('완료 ?')
            return True


    def seleniumLogin(self,info,headless=True,naver=False):

        '''카카오로 로그인'''
        # headless = False
        self.set_driver(headless=info['headless'])
        # input('헤드리스?')
        # options = webdriver.ChromeOptions()
        # if headless:
        #     options.add_argument("--headless")
        # # options.add_argument(f'--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25')
        # self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        cookiename = info['cookiename'].replace(os.path.basename(info['cookiename']),os.path.basename(info['cookiename']).replace(info['mallName'],''))
        
        url = 'https://accounts.kakao.com/login?continue=https%3A%2F%2Fdevelopers.kakao.com%2Flogin%3Fcontinue%3Dhttps%253A%252F%252Fdevelopers.kakao.com%252F&lang=ko'
        # url='https://developers.kakao.com/'

        # while True:
        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        print(self.driver.current_url)
        otherlink = False
        if self.driver.current_url != url:
            print('링크가 다름')
            # element = self.driver.find_element("id","__next") #iframe 태그 엘리먼트 찾기
            # self.driver.switch_to.frame(element) #프레임 이동
            # self.close()
            # self.driver.switch_to.default_content()
            # return 'ANOTHER LINK'
            print('fldzmfekfma')
            elem = self.driver.find_element('id','loginKey--1')
            elem.send_keys(info['loginId'])
            elem = self.driver.find_element('id','password--2')
            elem.send_keys(info['loginPass'])

            # if self.find_elem('id','loginKey--1',value=info['loginId']):
            #     print('아이디 넣기 성공')

            # if self.find_elem('id','password--2',value=info['loginPass']):
            #     print('비밀번호 넣기 성공')
            # self.find_elem('xpath','/html/body/div/div/div/main/article/div/div/form/div[1]',value=info['loginId'])
            # self.find_elem('xpath','/html/body/div/div/div/main/article/div/div/form/div[2]',value=info['loginPass'])
            time.sleep(1)

            if '보안문자 2분 후 만료' in str(self.driver.page_source):
                print('보안문자 ::: 재실행')
                return False
            print('로그인버튼클릭')
            self.find_elem('xpath','/html/body/div[1]/div/div/main/article/div/div/form/div[4]/button[1]')
            time.sleep(3)

            otherlink = True

            # input('끝 ?')
            # # continue
        else:
            print('제대로된 링크')
            self.find_elem('id','id_email_2',value=info['loginId'])
            self.find_elem('id','id_password_3',value=info['loginPass'])

            if '보안문자 2분 후 만료' in str(self.driver.page_source):
                print('보안문자 ::: 재실행')
                return False

            self.find_elem('xpath','/html/body/div/div/div/main/article/div/div/form/div[4]/button[1]')
            self.find_elem('xpath','/html/body/div[1]/div[2]/div/div/div/div/div/div/form/fieldset/div[8]/button[1]')

        
        time.sleep(5)
        # link_certify
        if 'pageTwoStepVerificationTms' in self.driver.current_url or 'two_step_verification' in self.driver.current_url:
            print('2단계 인증 -> 이메일로 인증합니다.')
            # input('임시로 하고넘어가기')
            self.naver.login(info,twostep=True)
            beforemailid = self.naver.getCertificationNumber(beforeMailid=False)
            print(beforemailid)

            if otherlink:
                # 이메일 인증하기 버튼 누르기
                self.find_elem('xpath','/html/body/div/div/div/main/article/div/div/a')
            else:
                if self.find_elem('xpath','/html/body/div[1]/div[15]/div[2]/div/div/div/a') == False:
                    print('첫번째 이메일로 인증하기 실패 두번째 시도')
                    self.find_elem('xpath','/html/body/div[1]/div[16]/div[2]/div/div/div/a')
            
            print('이메일 인증 버튼 클릭')
            
            for _ in range(2):
                for _ in range(40):
                    CertificationNumber = self.naver.getCertificationNumber(beforeMailid=beforemailid)
                    print('인증번호 :',CertificationNumber)
                    time.sleep(1)
                    if CertificationNumber: break
                #mArticle > div > a
                # /html/body/div[1]/div[15]/div[2]/div/div/div/a
                if CertificationNumber == False:
                    print('2차인증 실패 - 재요청')
                    self.find_elem('/html/body/div[1]/div[18]/div[2]/div/div/div/form/div[1]/button')
                    print('재요청 이메일 인증 버튼 클릭')
                    time.sleep(1)
                    self.find_elem('/html/body/div[1]/div[22]/div[2]/div/div[2]/div[2]/button[1]')
                    print('인증메일 재발송 클릭')
                    continue
                break

            if CertificationNumber == False:
                print('2차인증실패')
                return False

            # print(CertificationNumber)
            if otherlink:
                # 넣는 버튼
                self.find_elem('id','input-passcode',value=CertificationNumber)
                # ㅎ확인 버튼
                self.find_elem('xpath','/html/body/div/div/div/main/article/div/div/form/div[4]/button')
            else:
                self.find_elem('id','id_passcode_5',value=CertificationNumber)
                print('버튼 클릭')

                if self.find_elem('xpath','/html/body/div[1]/div[17]/div[2]/div/div/div/form/div[3]/button') == False:
                    if self.find_elem('xpath','/html/body/div[1]/div[18]/div[2]/div/div/div/form/div[3]/button')== False:
                        if self.find_elem('xpath','/html/body/div[1]/div[18]/div[2]/div/div/div/form/div[6]/button') == False:
                            return False

            
            time.sleep(5)
        # input('dd')
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        head = (soup.select_one('div#kakaoHead'))
        # input(head)
        if '로그인' in head:
            print('developer kakao 로그인 실패')
            return False
            
        pickle.dump(self.driver.get_cookies() , open(cookiename,"wb"))
        print('세션 저장 완료')
        
        if headless == False:
            self.driver.close()

        return True

 