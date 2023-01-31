


import datetime
import os
import time
import requests


class Custom_Library:
    '''변형된 라이브러리'''
    
    # def print_log
    def _make_request(self,requests_type,url,headers=False,proxies=False,data=False):
        count = 1
        res = False
        # while True:
        for _ in range(5):
            # if proxies:
            #     proxy = random.choice(self.proxylist)
            #     # print(proxy)
            #     proxies = {'http': f'http://{proxy}','https': f'http://{proxy}'}
            try:
                # print('proxy->',proxy)
                res = requests.request(requests_type,url,headers=headers,proxies=proxies,data=data,timeout=5)
                break
            except Exception as e:
                print('실패',count,url,e)
                count+=1
                time.sleep(2)
                continue
        return res 
        
    def createFolder(self,directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory.' + directory)


    def now(self):
        now = datetime.datetime.now()
        # formattedDate = now.strftime("%Y%m%d_%H%M%S")
        # formattedDate = now.strftime("[%H:%M:%S]")
        return now


    def listtofile(self,keyword,data,type=''):
        result = False

        if keyword.split('_')[1] == '':
            # print('려차')
            result = False
        else:
            if type == 'txt':
                with open(f'./DATA/키워드/{self.now().strftime("%Y%m%d_%H%M%S")}_{keyword}','w',encoding='utf8') as f :
                    f.write(data)
                result = True

            elif type == 'xlsx':
                print('엑셀은 준비중~')
                result = True

        return result




