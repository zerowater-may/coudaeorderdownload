import datetime
import os
import re
from urllib import response
import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
import time
import math as m

from gui.uis.openmarkets.naverlogin import Naver
from .kakaologin import Kakao


##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓##GMARKET 지마켓 G마켓
class InvoiceCenterNaverShopping(Kakao):
    def __init__(self):
        super().__init__()
        self.naver =  Naver()
        
    def islogin(self):
        '''로그인 되어있는지 확인하기'''
        self.wheretobuy = '네이버쇼핑'
        r = self.naver.login(self.info)
        print(r)
        if r: 
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 성공""")
        else:
            self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 로그인 실패""")
        return r

    def InvoiceCheck_navershopping(self,info):
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
        
        lastId0,hasmore,page = '0',True,1
        while hasmore:
            url = f'https://order.pay.naver.com/home/more?tabMenu=SHOPPING&serviceGroup=SHOPPING&lastId={lastId0}'
            if page == 1: url ='https://order.pay.naver.com/home?tabMenu=SHOPPING'
            response = self.naver.get(url)
            
            soup = BeautifulSoup(response.text,'html.parser')
            if '내역이 없습니다' in str(soup): 
                print('완료')
                break

            l = f'input#_lastId{lastId0}'
            h = f'input#_hasMore{lastId0}'
            # print(lastId0,hasmore)
       
            lastId0 = (soup.select_one(l)['value'])
            hasmore = bool(soup.select_one(h)['value'])

            for i in soup.select('div.goods_pay_section div.goods_group ul.goods_group_list'):
                res={'invoicenum':'','courier':''}
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                try:
                    res['ordNo'] = i.select_one('a.goods_thumb')['href'].split('/')[-1]
                except Exception:
                    continue
                res['PayNo'] = res['ordNo']
                res['wheretobuy'] = self.wheretobuy
                r = i.select_one('ul.info').text.split('\n')
                # print(r)
                # r[1] = '25500무료교환반품'
                res['price'] = re.sub(r'[^0-9]', '', r[1])
                res['paytime'] = r[2].replace('상품구매날짜','').replace(' ','')
                try:
                    res['Status'] = i.select_one('span.state._statusName').text
                except Exception:
                    res['Status'] = i.select_one('a.state._statusName').text
                res['prdNm'] = i.select_one('img')['alt']

                res['invoicecode']  = False
                
                # 디테일 정보
                if res.update(self.InvoiceDetail_navershopping(res['ordNo'])) == {}:
                    continue

                # 운송장 정보
                if res['invoicecode']:
                    res.update(self.getrealinvoice_navershopping(res['invoicecode']))
                
                # if res['PayNo'] == '2022112519141501': input('지금')
                if 'name' not in res: continue 

                print(res)
                print('='*30)
                result.append(res)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                # if len(result) ==100 : break
            page+=1
            # if len(result) == 100 : break
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")                
        return result
    
    def InvoiceCheck_navershopping_apiv2(self,info):
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
        
        lastId0,hasmore,page = '0',True,1
        while hasmore:
            url = f'https://new-m.pay.naver.com/api/timeline/v2/search?page={page}&from=PC_PAYMENT_HISTORY'
            # try:
            response = self.naver.get(url).json()
            # except Exception:
            # rr = response['result']['items']
            if len(response['result']['items']) == 0: break
            print(url)
            for idx,i in enumerate(response['result']['items']):
                res={'invoicenum':'','courier':''}
                res['cookiename'] = self.cookiename
                res['cookiepath'] = self.cookiename
                res['wheretobuy'] = self.wheretobuy
                if i['serviceType'] != 'ORDER': continue
                res['ordNo'] = i['additionalData']['orderNo']
                res['PayNo'] = i['additionalData']['orderNo']
                res['detailurl'] = i['orderDetailUrl']
                res['price'] = i['additionalData']['orderAmount']
                
                res['paytime'] = (datetime.datetime.utcfromtimestamp(int(str(i['date'])[:-3]))+ datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
                try:
                    res['Status'] = i['status']['text']
                except Exception:
                    res['Status'] = '직접조회요청'
                res['prdNm'] = i['product']['name']
# https://order.pay.naver.com/o/orderStatus/deliveryTracking/2023011290896991/ORDER_DELIVERY/api?returnUrl=https%3A%2F%2Forder.pay.naver.com%2Fo%2ForderStatus%2F2023011265551061%3FreturnUrl%3Dhttps%253A%252F%252Fnew-m.pay.naver.com%252Fpcpay
# https://order.pay.naver.com/o/orderStatus/deliveryTracking/2023011290897011/ORDER_DELIVERY/api?returnUrl=https%3A%2F%2Forder.pay.naver.com%2Fo%2ForderStatus%2F2023011265551061%3FreturnUrl%3Dhttps%253A%252F%252Fnew-m.pay.naver.com%252Fpcpay
                # 디테일 정보
                if res.update(self.InvoiceDetail_navershopping_apiv2(res['ordNo'])) == {}:
                    print('업로드')
                    continue
    

                # 운송장 정보
                # if res['invoicecode']:
                res.update(self.getrealinvoice_navershopping(i['additionalData']['uniqueKey']))
                
                # if 'name' not in res: continue 

                print(res)
                print('='*30)
                result.append(res)
                self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] [{len(result)}/-] {res['paytime']} | {res['Status']} | {res['ordNo']} | {res['price']}원 | {res['name']} | {res['courier']} | {res['invoicenum']}""")
                # if len(result) ==2 : break

            page+=1
            # if len(result) == 2 : break
        self.beforeclass.update_msg.emit(f"""[{self.info['mallName']}/{self.info['loginType']}/{self.info['loginId']}] 수집완료""")                
        return result

    def InvoiceDetail_navershopping(self,ordNo):
        res = {}
        try:
            url = f'https://order.pay.naver.com/orderStatus/{ordNo}'
            # url = 'https://order.pay.naver.com/orderStatus/2022112519141501'
            # url = 'https://order.pay.naver.com/orderStatus/2022112517361801'
            # res["detailurl"] = url
            response = self.naver.get(url)
            print(url)
            try:
                soup = BeautifulSoup(response.text,'html.parser')
            except Exception:
                return res
            
            if str(soup) == '': 
                # input(soup)
                
                return res
                #content > div > table.tb_list2.tb_input > tbody > tr:nth-child(1) > td > table > tbody > tr.gap > td
            res['name'] = soup.select_one('tr.gap > td').text
            try:
                a = soup.select_one('div.inp_area._deliveryPlace > table > tbody > tr:nth-child(4) > td').text.replace('\n','').split('\t')
                try:
                    res['addressnum'] = a[1]
                except Exception:
                    a = soup.select_one('div.inp_area._deliveryPlace > table > tbody > tr:nth-child(3) > td').text.replace('\n','').split('\t')
                    res['addressnum'] = a[1]

                    
                res['address'] = a[2]+' '+a[3]
            except Exception:
                res['addressnum'] = ''
                res['address'] = ''
            res['invoicecode'] = soup.select_one('span.thm.ordernum2').text # 이게 운송장 code 
            
            try:
                p = soup.select_one('td.money.btm_line._primaryPayAdmission td').text.replace('\t','').split('\n')
                res['pay'] = p[1]
                res['paytime'] = p[-2].replace(')','').replace('(','')
            except Exception:
                res['pay'] = '네이버페이'
                res['pay'] = '네이버페이'
            res['paydetail'] = ''
            print(res)
        except Exception:
            return {}
        return res
    
    def InvoiceDetail_navershopping_apiv2(self,ordNo):
        res = {}
        # ordNo = '2023011532470621'
        url = f'https://order.pay.naver.com/o/orderStatus/{ordNo}'
        res['pay'] = ''
        res['paydetail'] = ''
        # res["detailurl"] = url
        response = self.naver.get(url)
        print(url)
        try:
            soup = BeautifulSoup(response.text,'html.parser')
        except Exception:
            return res
        
        if str(soup) == '': 
            # input(soup)
            return res
        res['addressnum'] = ''
        res['address'] = ''
        try:
            res['name'] = soup.select('div#content ul.info_list.person_info.delivery li')[0].select_one('span').text
            res['addressnum'] = soup.select('div#content ul.info_list.person_info.delivery li')[2].select_one('span').text
            res['address'] = soup.select('div#content ul.info_list.person_info.delivery li')[2].text
        except Exception:
            res['name'] = soup.select('div#content ul.info_list.person_info li')[0].select_one('span').text
        if '-' in res['addressnum']:
            res['addressnum'] = soup.select('div#content ul.info_list.person_info.delivery li')[3].select_one('span').text
            res['address'] = soup.select('div#content ul.info_list.person_info.delivery li')[3].text
            
        
        return res

    def getrealinvoice_navershopping(self,invoicecode):
        # 여기서 부터 운송장가져오기
        res = {}
        headers = {
            'referer':'https://order.pay.naver.com/home?tabMenu=SHOPPING',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            }
        url = f'https://order.pay.naver.com/o/orderStatus/deliveryTracking/{invoicecode}/ORDER_DELIVERY/api'
        
        response = self.naver.get(url,headers=headers)
        print(url)
        soup = BeautifulSoup(response.text,'html.parser')
        if soup != '': 
            c = soup.select('span.item_value')
            # print(c)
            if len(c) != 0:
                try:
                    res['invoicenum'] = c[0].text
                    res['courier'] = c[1].text.split('\n')[0]
                except Exception:
                    res['invoicenum'] = ''
                    res['courier'] = ''
                # print(res)
        return res  
