import os
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m
from .kakaologin import Kakao


##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓
class InvoiceCenter11st(Kakao):

    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '11번가'
        count = 1 
        for _ in range(2):
            try:
                print('쿠키네임 : ',self.cookiename)
                cookies = pickle.load(open(self.cookiename, "rb"))
            except Exception:
                print(f'{self.wheretobuy} 세션 없음')
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 중""")
                if self.info['loginType'] == self.wheretobuy:
                    a = self.eleven11stLogin(self.info)
                    if a == False: self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""") ;return False
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                    # input('dd')
                continue
            

            # 쿠키를 확인하는 부분
            self.elevenst = requests.Session()
            for cookie in cookies:    
                self.elevenst.cookies.set(cookie['name'], cookie['value'])

            ## 11번가 배송준비중일때도 긁기
            # 결제완료 = payment ,배송중 = delivery
            # 모든거
            # res= self.elevenst.get('https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo=')
            url = 'http://www.11st.co.kr/register/getGradeInfo.tmall?method=getGrade'
            res = self.elevenst.get(url)
            # res = requests.get(url)
            if '로그인 페이지로 이동' in res.text: 
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 재 로그인 중 ({count})""")
                count +=1
                if self.info['loginType'] == self.wheretobuy:
                    self.eleven11stLogin(self.info)
                    continue
                if self.info['loginType'] == '카카오':
                    self.isCookieLive(self.info)
                    continue
            else: 
                # 주문 있는 지 없는지 .
                # url ='https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=delivery&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo='
                url ='https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo='
                res = self.elevenst.get(url)
                soup = res.json()
                # input(len(soup['data']['products']))
                # input(soup)
                if len(soup['data']['products']) == 0:
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 주문이 없습니다.""")
                    return False
                else:
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
                    return True
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
        return False

    def InvoiceCheck_11st(self,info):
        self.info = info
        # input(self.info)
        print(self.info)
        self.beforeclass = info['self']
        # self.info = {'groupId': '', 'id': 0, 'isAuth': 'True', 'nickName': '', 'mallName': '옥션', 'loginType': '옥션', 'loginId': 'kys980531', 'loginPass': 'qaz7410@@', 'memo': '메모장', 'emailId': 'kys053123@naver.com', 'emailPass': 'fkaustkfl12!', 'cookiename': 'D:\\Dropbox\\zerowater\\billy\\DATA\\COOKIE\\옥션옥션kys980531.pkl'}
        self.cookiename = self.info['cookiename']
    
        islogin = self.islogin()
        if islogin == False: return False
        # 여기까지 기본

        result = []
        ## 11번가 배송준비중일때도 긁기
        # 결제완료 = payment ,배송중 = delivery
        # 모든거
        # res= self.elevenst.get('https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo=')
        for sta in ['payment','delivery','dlvReady','dlvEnd']:
        # for sta in ['delivery']:
            # print(sta)
            nextPagePendingFailOrdNo = ''
            nextPageOrdDtYmdhis = ''

            while True:
                # print(sta)
                # #첫번째 콜
                # 'https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=delivery&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo='
                # #두번째 콜
                # 'https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=delivery&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=20211104011659&shPendingFailOrdNo=20211104294071540&shDateFrom=&shDateTo='
                url = f'https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat={sta}&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis={nextPageOrdDtYmdhis}&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo={nextPagePendingFailOrdNo}&shDateFrom=&shDateTo='
                res = self.elevenst.get(url)
                # print(url)
                # res = self.elevenst.get('https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=payment&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo=')
                #배송중만 ?
                # url ='https://m.11st.co.kr/MW/MyPage/api/V1/orderProductList.tmall?firstCall=true&shSvcClfCdTab=00&shDateType=13&shSortDt=orderdt&shOrdPrdStat=delivery&shPrdNm=&shCustActService=&encodeShPrdNm=&shOrderDtYmdhis=&shStatChgDt=&shCustActDtlsNo=&shFreeOrderBuyDt=&shPendingOrdNo=&shPendingFailOrdNo=&shDateFrom=&shDateTo='
                
                # soup = BeautifulSoup(self.driver.page_source, 'lxml')
                # soup = json.loads(soup.select_one('body > pre').text)
                soup = res.json()
                # print(soup['data']['hasMorePage'])
                # continue
                # with open ('11stest.txt','w',encoding='utf8') as f :
                #     f.write(str(soup))
                # input('aa')
                # input(soup)
                #만약 hasmorepage가 True면 url의 포맷값이 바뀜
                if soup['data']['hasMorePage']:
                    nextPagePendingFailOrdNo = soup['data']['nextPagePendingOrdNo']
                    nextPageOrdDtYmdhis = soup['data']['nextPageOrdDtYmdhis']
                    print(nextPagePendingFailOrdNo,nextPageOrdDtYmdhis)
                for i in soup['data']['products']:
                    # input(i)
                    res={'invoicenum':'','courier':''}
                    # res['billiid'] = self.info['billiid']
                    res['cookiename'] = self.cookiename
                    res['cookiepath'] = self.cookiename
                    res['wheretobuy'] = '11번가'
                    # if i['ordPrdStatNm'] == '배송완료': i['ordPrdStatNm'] = '배송중'
                    res['Status'] = i['ordPrdStatNm']
                    res['PayNo'] = i['ordNo']
                    res['ordNo'] = i['ordNo'] # 주문 번호
                    # res['detailurl'] = f'https://m.11st.co.kr/MW/MyPage/V1/orderDetailV1.tmall?ordNo={i["ordNo"]}'
                    res['detailurl'] = '-'
                    # res['dlvMthdCd'] = i['orderClaimDelivery']['dlvMthdCd'] # 택배사 코드 ?
                    # print(res['dlvMthdCd'])
                    # if res['dlvMthdCd'] == '01': res['dlvMthdCd'] = '한진택배'
                    res['invoicenum'] = i['orderClaimDelivery']['invcNo'] # 운송장번호
                    # res['courier'] = 
                    # if i['ordNo'] == '20211110301079980':
                    #     input(i)

                    # print(i['statNmSubDesc'])
                    try:
                        res['courier'],res['invoicenum'] = i['statNmSubDesc'].replace(' ','').split('/') #택배사 / 운송장번호
                    except Exception:
                        pass
                    if '도착완료' in res['invoicenum']:
                        fff = self.getjsoninvoice_11st(i['traceDlvNo'])
                        # input(fff)
                        res['invoicenum'] = fff['i']
                        res['courier'] = fff['c']
                        # try:
                        # except Exception:
                        #     continue
                        # res['price'] = i['ordPrdWonStl'] # 내가 실제 구매가격
                    # input(i['statNmSubDesc'])
                    res['prdNm'] = i['prdNm'] # 상품명
                    res['qty'] = i['ordQty'] # 상품수 옵션수량
                    res.update(self.InvoiceDetail_11st(i['ordNo']))
                    result.append(res)
                    print(res)
                    print('='*30)
                    self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                    # input(res)
                    # input(len( soup['data']['products']))

                if soup['data']['hasMorePage'] == False:
                    # print('페이지 끝남')
                    break

        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")                
        return result

    def getjsoninvoice_11st(self,traceDlvNo):
        res = {}
        url = f'http://m.11st.co.kr/MW/DeliveryTrace/api/V1/deliveryTracePop.tmall?dlvNo={traceDlvNo}'
        try:
            data = self.elevenst.get(url).json()
            res['i'] = data['data']['traceListGJ'][0]['deliveryBaseInfo']['trInvcNo']
            res['c'] = data['data']['traceListGJ'][0]['deliveryBaseInfo']['dlvEtprsCdName']
        except Exception:
            # input(data)
            res = self.getrealinvoice_11st(traceDlvNo)
        return res
    
    def getrealinvoice_11st(self,traceDlvNo):
        res = {}
        url = f'http://m.11st.co.kr/MW/DeliveryTrace/deliveryTracePop.tmall?dlvNo={traceDlvNo}'
        # url = f'http://m.11st.co.kr/MW/DeliveryTrace/api/V1/deliveryTracePop.tmall?dlvNo=2105503388'
        # input(url)
        soup = BeautifulSoup(self.elevenst.get(url).text,'lxml')
        try:
            res['c'] = soup.select_one('#trackingInquiryDetail > div.modal_cont > div > div.inquiry_track_wrap > div > div > a').text.split('1')[0]
            res['i'] = soup.select_one('#trackingInquiryDetail > div.modal_cont > div > div.inquiry_track_wrap > div > div > div > span').text
        except Exception:
            # print('요기')
            # input(soup.select('#trackingInquiryDetail div.inquiry_track_info dl'))
            res['c'] = soup.select_one('#trackingInquiryDetail > div.modal_cont > div > div.inquiry_track_wrap > div > div > a').text.split('1')[0]
            res['i'] = soup.select_one('#trackingInquiryDetail > div.modal_cont > div > div.inquiry_track_wrap > div > div > div > span').text

        url = f'https://buy.11st.co.kr/delivery/trace.tmall?dlvNo={traceDlvNo}'
        # url = 'https://buy.11st.co.kr/delivery/trace.tmall?dlvNo=2105503388'
        soup = BeautifulSoup(self.elevenst.get(url).text,'lxml')
        # input(soup)
        try:
            res['c'] = (soup.select('div.delivery_info div.field dd')[1].text.replace(' 1588-1255','').rstrip().lstrip())
            res['i'] =(soup.select('div.delivery_info div.field dd')[2].text.rstrip().lstrip())
        except Exception:
            return res
        return res
        
    def InvoiceDetail_11st(self,ordNo):
        res = {}#https://m.11st.co.kr/MW/MyPage/V1/orderDetailV1.tmall?ordNo=20211110301079980'
        # url = f'https://m.11st.co.kr/MW/MyPage/V1/orderDetailV1.tmall?ordNo={ordNo}'
        url = f'https://m.11st.co.kr/MW/OrderDetail/api/V1/getOrderDetail.tmall?ordNo={ordNo}'
        
        # url = 'https://m.11st.co.kr/MW/MyPage/V1/orderDetailV1.tmall?ordNo=20220104344802714'
        print(url)
        # headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
        #             'authority':'m.11st.co.kr'}
        soup = self.elevenst.get(url).json()
        # soup = BeautifulSoup(self.elevenst.get(url).text,'lxml')
        # data = (soup)
        # info = soup.select('#sec em')
        # input(info)
        # with open ('11stest.json','w') as f :
        #     f.write(str(soup))
        # print(soup.select_one('#divDlvp > div.recipient_infomation > ul > li > em'))
        try:
            res['name'] = soup['data']['myDeliveryInfoV1']['dlvpRcvrNm']
        except Exception:
            # input(soup)
            res['name'] = '11번가이름오류'
        # res['detailurl'] = url
        res['addressnum'] = soup['data']['myDeliveryInfoV1']['dlvpRcvrMailNo']
        res['address'] =soup['data']['myDeliveryInfoV1']['dlvpRcvrBaseAddr']
        # print(res)
        # input(soup)
        # input(soup['data']['myOrderProductV1'])
        res['status'] = soup['data']['myOrderProductV1']['orderProductMngList'][0]['ordPrdStatNm']
        res['pay'] =   soup['data']['orderInfoListJ'][0]['strStlTypeNm']
        res['paytime'] =  soup['data']['orderInfoListJ'][0]['strCrdStlAprvDt']
        res['paydetail'] =''
        # res['price'] = soup['data']['myOrderProductV1']['orderProductMngList'][0]['stlAmt']
        res['price'] = (soup['data']['orderInfoListJ'][0]['stlAmt'].replace(',','').replace('원',''))
        # input(res)
            # print(res['payhistory'])
            # print(res)

        return res
        
    def eleven11stLogin(self,info,headless=True):
        '''11번가 로그인'''
        # headless=False
        options = webdriver.ChromeOptions()
        if info['headless']:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # cookiename = 'G마켓카카오박예찬'
        url = 'https://login.11st.co.kr/auth/front/login.tmall?returnURL=https%3A%2F%2Fwww.11st.co.kr%2F'

        self.driver.get(url),self.driver.implicitly_wait(10),time.sleep(2)
        self.driver.find_element('id','loginName').send_keys(info['loginId'])
        self.driver.find_element('id','passWord').send_keys(info['loginPass'])
        self.driver.find_element('id','loginbutton').click(),time.sleep(2)
        
        time.sleep(4)
        if '비밀번호가 잘못되었습니다' in str(self.driver.page_source ):
            self.driver.close()
            self.driver.quit()   
            return False
        # input('사이트에 로그인 후 엔터를 누르세요.')
        pickle.dump(self.driver.get_cookies() , open(self.cookiename,"wb"))

        print('세션 저장 완료')
        # input('')
        self.driver.close()
        self.driver.quit()     
        return True