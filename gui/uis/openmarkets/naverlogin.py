from rsa import encrypt, PublicKey
from requests import Session
from lzstring import LZString
from uuid import uuid4
from json import dumps
from bs4 import BeautifulSoup
 
 
class Naver(Session):
    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.base = "https://nid.naver.com/nidlogin.login"
        self.bvsd = {
            "uuid": None,
            "encData": None
        }
        self.default = {
            "localechange": "",
            "dynamicKey": None,
            "encpw": None,
            "svctype": "262144",
            "smart_LEVEL": "-1",
            "bvsd": None,
            "encnm": None,
            "locale": "en_US",
            "url": "https:///m.naver.com/aside/",
            "nvlong": "on",
            "appSchemeView": "true",
            "id": "",
            "pw": ""
        }
 
        self.state_footprint = {
            "a": None, # uuidWithCaptchaSequence
            "b": "1.3.4", # bvsdVersion
            "c": False, # deviceTouchable
            "d": [{ # keyboardLogs
                "a": ["0,d,TAB,9"], # keyStrokeLog
                "b": { # inputIntervalLog
                    "a": None, # valueTimelineList
                    "b": 0 # timelineListIndex
                },
                "c": "", # initialValue
                "d": None, # CompleteValue
                "e": False, # secureMode
                "f": False, # hideValueMode
                "i": "id" # inputFieldId
            }, {
                "a": ["0,d,TAB,"], # keyStrokeLog
                "b": { # inputIntervalLog
                    "a": ["0,"], # valueTimelineList
                    "b": 0 # timelineListIndex
                },
                "c": "", # initialValue
                "d": "", # CompleteValue
                "e": True, # secureMode
                "f": False, # hideValueMode
                "i": "pw" # inputFieldId
            }],
            "e": { # deviceOrientation
                "a": {  # firstOrientation
                    "a": 53.9, # Alpha
                    "b": 65.7, # Beta
                    "c": 4.8 # Gamma
                },
                "b": { # currentOrientation
                    "a": 53.9, # Alpha
                    "b": 65.7, # Beta
                    "c": 4.8 # Gamma
                }
            },
            "f": { # deviceMotion
                "a": { # first
                    "a": { # firstAcceleration
                        "a": 999, # X
                        "b": 999, # Y
                        "c": 999 # Z
                    },
                    "b": { # firstAccelerationIncludingGravity
                        "a": 999, # X
                        "b": 999, # Y
                        "c": 999 # Z
                    }
                },
                "b": { # current
                    "a": { # currentAcceleration
                        "a": 999, # X
                        "b": 999, # Y
                        "c": 999 # Z
                    },
                    "b": { # currentAccelerationIncludingGravity
                        "a": 999, # X
                        "b": 999, # Y
                        "c": 999 # Z
                    }
                }
            },
            "g": { # mouseMove
                "a": [], # mouseActiveLogs
                "b": 0, # timelineListIndex
                "c": 0, # pageXDifference
                "d": 0, # pageYDifference
                "e": -1, # totalInterval
                "f": 0 # errorCount
            },
            "h": "7e518ea5eb58651f6d4af5f24ef83781", # fingerprintHash
            "i": { # browserFingerprintComponents
                "a": self.headers["user-agent"],
                "b": "en",
                "c": 24,
                "d": 8,
                "e": 1,
                "f": 4,
                "g": [1680, 1050],
                "h": [1680, 1010],
                "i": -540,
                "j": 1,
                "k": 1,
                "l": 1,
                "z": 1,
                "m": "unknown",
                "n": "Win32",
                "o": "unknown",
                "aa": ["Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf", "Chrome PDF Viewer::::application/pdf~pdf", "Native Client::::application/x-nacl~,application/x-pnacl~"],
                "p": "bb84491f8f0ca552e32aa5b90b350297",
                "q": "ebed6372b259af3e658060d47d3aaadb",
                "r": "Google Inc. (Intel)~ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.100.7324)",
                "s": False,
                "t": False,
                "u": False,
                "v": False,
                "w": False,
                "x": [0, False, False],
                "y": ["Arial", "Arial Black", "Arial Narrow", "Calibri", "Cambria", "Cambria Math", "Comic Sans MS", "Consolas", "Courier", "Courier New", "Georgia", "Helvetica", "Impact", "Lucida Console", "Lucida Sans Unicode", "Microsoft Sans Serif", "MS Gothic", "MS PGothic", "MS Sans Serif", "MS Serif", "Palatino Linotype", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Symbol", "Tahoma", "Times", "Times New Roman", "Trebuchet MS", "Verdana", "Wingdings"]
            },
            "j": 134 # fingerprintProcessingDuration
        }
     
    def form(self):
        return self.default
     
    def new_bvsd_data(self):
        return self.bvsd
     
    def new_bvsd_footprint(self):
        return self.state_footprint
     
    def encode_bvsd_data(bvsd_data):
        return LZString.compressToEncodedURIComponent(dumps(bvsd_data))
 
    def fill_bvsd(self, bvsd, id):
        bvsd_uuid = str(uuid4())+"-0" # 로그인 할때 사용되는 bvsd uuid 생성
        bvsd["uuid"] = bvsd_uuid
 
        bvsd_data = self.new_bvsd_footprint()
        bvsd_data["a"] = bvsd_uuid
        bvsd_data["d"][0]["b"]["a"] = ["0,{}".format(id)]
        bvsd_data["d"][0]["d"] = id
 
        bvsd["encData"] = Naver.encode_bvsd_data(bvsd_data)
 
        return bvsd
     
    def get_finalize(response_text: str):
        if response_text.find("location") > -1:
            return {
                "url": response_text.split('("')[1].split('")')[0],
                "result": True
            }
        else:
            return {
                "result": False
            }
 
    def login(self, info,twostep=False):
        if twostep: 
            NAVER_ID = info['emailId']
            NAVER_PW = info['emailPass']
        else:
            NAVER_ID = info['loginId']
            NAVER_PW = info['loginPass']
        NAVER_ID = NAVER_ID.strip()
        NAVER_PW = NAVER_PW.strip()
        print('카카오 - 네이버 로그인 : ',NAVER_ID,NAVER_PW)
        def download_keys():
            DOM = BeautifulSoup(self.get(self.base, params={
                "svctype": self.default["svctype"] # 모바일 페이지
            }, headers=self.headers).text, 'html.parser')
 
            Keys = DOM.find('input', {'id': "session_keys"}).attrs['value']
 
            session_key, key_name, e, N = Keys.split(",")
 
            return {
                "dynamic_key": DOM.find('input', {'id': 'dynamicKey'}).attrs['value'],
                "session_key": session_key,
                "public_key": PublicKey(int(e, 16), int(N, 16)),
                "key_name": key_name
            }
         
        def encrypt_with_public_key(ID: str, PW: str, Keys: dict) -> str:
            encode_login_info = ''.join([chr(len(s)) + s for s in [Keys['session_key'], ID, PW]]).encode()
 
            return encrypt(encode_login_info, Keys["public_key"]).hex() # 암호화하고 hex 값으로, e와 N값 순서는 네이버가 구라친겁니다.
        
        Keys = download_keys() # 서버의 공개키와 키 세션들을 가져온다.
 
        encrypted_info = encrypt_with_public_key(NAVER_ID, NAVER_PW, Keys) # 공개키를 이용하여 세션키와 함께 로그인 정보를 암호화한다.
        form = self.form() # 새로운 로그인 폼 생성
         
        bvsd = self.fill_bvsd(self.new_bvsd_data(), NAVER_ID) # 새로운 bvsd 폼 생성 후 내용 채우기s
 
        form["dynamicKey"] = Keys["dynamic_key"]
        form["encpw"] = encrypted_info
        form["encnm"] = Keys["key_name"]
        form["bvsd"] = dumps(bvsd)
 
        result = Naver.get_finalize(self.post(self.base, data=form, headers=self.headers).text)
 
        if result["result"]:
            self.get(result["url"], headers=self.headers)
            
            # res = self.get('https://order.pay.naver.com/home?tabMenu=SHOPPING',headers=self.headers)
            
            return True
        else:
            return False
    
    def getCertificationNumber(self,beforeMailid=True):
        '''네이버 이메일'''
        url = 'https://mail.naver.com/json/list/?page=1&sortField=1&sortType=0&folderSN=0&type=&isUnread=false='
        res = self.post(url)
        # input(res.json())
        if beforeMailid == False:
            #만약 첫번째 시도면 메일의 마지막값을 불러옴
            try:
                mailid = res.json()['mailData'][0]['mailSN']
            except Exception:
                mailid = 0
            return mailid

        # 두번째부터는 마지막값보다 커야함
        for i in res.json()['mailData']:
            mailid,name,subject = i['mailSN'],i['from']['name'],i['subject']
            # print(mailid,name,subject)
            if mailid > beforeMailid:
                if name == '카카오팀' or name == 'Kakao Team':
                    if '인증번호' in subject or 'Verification for Kakao' in subject:
                        url = f'https://mail.naver.com/json/read/?charset=&prevNextMail=true&threadMail=false&folderSN=-2&listScrollPosition=0&mailSN={mailid}&previewMode=2'
                        detail = self.post(url).json()

                        soup = BeautifulSoup(detail['mailInfo']['body'],'lxml')

                        try:
                            certificationnum = soup.select_one('html table table table tbody tr:nth-child(5) td:nth-child(4)').text
                        except Exception:
                            certificationnum = 0

                        return certificationnum
        return False

                        # print(i['mailSN'])
                        # print(i['from']['name'])
                        # print(i['subject'])
                        
                        # input(i)

if __name__ == "__main__":
    # TEST FIELD
    import datetime
    lastmessagetime = (datetime.datetime.utcfromtimestamp(1672851621)+ datetime.timedelta(hours=9))#.strftime('%Y/%m/%d %H:%M:%S %Z'))
    print(lastmessagetime)
    Browser = Naver()
    info ={}
    # info['loginId'] ='kys053123'
    # info['loginPass'] = 'fkaustkfl123!'
    info['loginId'] ='sybbbb'
    info['loginPass'] = 'ekfsla1040'
    if Browser.login(info):
        print("성공!")
        # beforemailid = Browser.getCertificationNumber(beforeMailid=False)
        # print(beforemailid)
        # beforemailid = 1
        # num = Browser.getCertificationNumber(beforeMailid=beforemailid)
        # print(num)
        res = Browser.get('https://new-m.pay.naver.com/api/timeline/v2/search?page=7&from=PC_PAYMENT_HISTORY')
        print('??')
        soup = BeautifulSoup(res.text,'lxml')
        print(soup)
    #     for i in soup.select('div.goods_pay_section div.goods_group ul.goods_group_list'):
    #         print(i.select_one('a. '))
    #         input(i)
    else:
        print("실패!")