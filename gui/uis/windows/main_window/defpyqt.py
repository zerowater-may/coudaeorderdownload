from PySide6.QtWidgets import *
# from PyQt5.QtWidgets import *
# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

import datetime
# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes
class DefPyQt:
    '''pyqt함수들'''
    # app = QApplication([])

    def __init__(self):
        super().__init__()

        settings = Settings()
        self.settings = settings.items
        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

    def nowtime(self):
        now = datetime.datetime.now()
        # print(now)          # 2015-04-19 12:11:32.669083
        
        nowDate = now.strftime('%Y-%m-%d')
        # print(nowDate)      # 2015-04-19
        return nowDate
        # nowTime = now.strftime('%H:%M:%S')
        # print(nowTime)      # 12:11:32
        
        # nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        # print(nowDatetime)  # 2015-04-19 12:11:32
    def showMessageBoxs(self,title,message):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setStyleSheet(f"""
        background: "{self.themes['app_color']['bg_two']}";
        font: {self.settings["font"]["text_size"]}pt "{self.settings["font"]["family"]}";
        color: {self.themes["app_color"]["text_foreground"]};
        """)
        msgBox.setText(message)
        # msgBox.setIcon(QIcon(Functions.set_svg_icon("icon_settings.svg")))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    # def showMessageBoxsYesNo(self,title,message):
    #     msgBox = QMessageBox()
    #     ret = msgBox.question(self,title,message, msgBox.Yes | msgBox.No)
    #     if ret == msgBox.Yes:
    #         return True
    #     return False
    def showMessageBoxsYesNo(self,title,message):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        # msgBox.setInformativeText("InformativeText")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)
        result = msgBox.exec()
        if result == QMessageBox.Ok:
           return True
        elif result == QMessageBox.Cancel:
           return False
        elif result == QMessageBox.Discard:
            print("Discard")
            
    def msg_update(self, msg,uploadbuttonactive=False):
        '''상태메세지 업데이트'''
        try:
            msg = self.now().strftime("[%H:%M:%S]")+' '+msg
        except Exception:
            pass
        self.textBrowser.append(msg)
        print(msg) # 나중에 로그로 바꾸기

        # 스스업로더할때 상태 업데이트 해줘야함 #리프레쉬
        if uploadbuttonactive:
            self.exceluploader_stratpushButton_3.setEnabled(True)
            self.exceluploader_stratpushButton_3.setText('업로드')
            self.exceluploader_stratpushButton_3.setStyleSheet("QPushButton"
                "{"
                "background-color : rgb(58, 134, 255);"
                "color: white;"
                "border-radius: 5px;"
                "}")
                
    def setKeywords(self, result):
        '''쓰레드에서 데이터 받아서 textedit에 보내기'''
        # key= ''
        global changeresult
        changeresult = result
        allkeywords = []
        openmarekts = ['네이버쇼핑','쿠팡','11번가','지마켓','옥션']
        for i,v in enumerate(openmarekts):
            for key in result['auto'][v]:
                allkeywords.append(key)
            if v == '네이버쇼핑': self.navershoppingkeyword_textEdit.setText(','.join(list(set(result['auto'][v]))))
            if v == '쿠팡': self.coupangkeyword_textEdit.setText(','.join(list(set(result['auto'][v]))))
            if v == '11번가': self.st11keyword_textEdit.setText(','.join(list(set(result['auto'][v]))))
            if v == '옥션': self.auctionkeyword_textEdit.setText(','.join(list(set(result['auto'][v]))))
            if v == '지마켓': self.gmarketkeyword_textEdit.setText(','.join(list(set(result['auto'][v]))))
        print(allkeywords)

        allkeywords = list(set(allkeywords)) # 중복제거
        print(allkeywords)

        self.allkeyword_textEdit.setText(','.join(allkeywords))
        self.relatedkeywords_search_QPushButton.setEnabled(True)
        self.viewtypebutton.setEnabled(True)
        
    def changebutton(self,type):
        '''글로벌로 될까 타입 ( auto , rel )'''
        allkeywords = []
        openmarekts = ['네이버쇼핑','쿠팡','11번가','지마켓','옥션']
        for i,v in enumerate(openmarekts):
            for key in changeresult[type][v]:
                allkeywords.append(key)
            if v == '네이버쇼핑': self.navershoppingkeyword_textEdit.setText(','.join(list(set(changeresult[type][v]))))
            if v == '쿠팡': self.coupangkeyword_textEdit.setText(','.join(list(set(changeresult[type][v]))))
            if v == '11번가': self.st11keyword_textEdit.setText(','.join(list(set(changeresult[type][v]))))
            if v == '옥션': self.auctionkeyword_textEdit.setText(','.join(list(set(changeresult[type][v]))))
            if v == '지마켓': self.gmarketkeyword_textEdit.setText(','.join(list(set(changeresult[type][v]))))
        # print(allkeywords)

        allkeywords = list(set(allkeywords)) # 중복제거
        print(allkeywords)

        self.allkeyword_textEdit.setText(','.join(allkeywords))
        self.relatedkeywords_search_QPushButton.setEnabled(True)
        
    def set_tags(self,result):
        key= ''
        allkeywords = []
        for i,v in enumerate(result): # list안에 dict
            
            for key, value in v.items() :
                print(key, value)
                
                for k in value:
                    allkeywords.append(k)

                if key == '네이버쇼핑 관련태그': 
                    self.allkeyword_textEdit_2.setText(','.join(list(set(value))))
                    self.relatedkeywords_search_QPushButton_2.setEnabled(True)



    

    def navershoppingrelatedtags_copyToclipboard(self):
        '''네이버 연관태그'''
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.allkeyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[관련태그]가 복사되었습니다.')
    
    def copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.allkeyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[전체키워드]가 복사되었습니다.')
    def navershopping_copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.navershoppingkeyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[네이버쇼핑키워드]가 복사되었습니다.')
    def coupang_copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.coupangkeyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[쿠팡키워드]가 복사되었습니다.')
    def st11_copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.st11keyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[11번가키워드]가 복사되었습니다.')
    def auction_copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.auctionkeyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[옥션키워드]가 복사되었습니다.')
    def gmarket_copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.gmarketkeyword_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[지마켓키워드]가 복사되었습니다.')
    def relatedtags_copyToclipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.relatedtags_textEdit.toPlainText(),mode=cb.Clipboard)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[관련태그]가 복사되었습니다.')
        
    # def savekeywordfile(self):
    #     print('저장')
    #     # with open('somefile.txt', 'a') as f:
    #     #     f.write(mytext)
    #     self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[전체키워드]가 저장되었습니다.')
    
    def navershopping_savekeywordfile(self):
        print('저장')
        # with open('somefile.txt', 'a') as f:
        #     f.write(mytext)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[네이버쇼핑키워드]가 저장되었습니다.')
    def coupang_savekeywordfile(self):
        print('저장')
        # with open('somefile.txt', 'a') as f:
        #     f.write(mytext)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[쿠팡키워드]가 저장되었습니다.')
    def st11_savekeywordfile(self):
        print('저장')
        # with open('somefile.txt', 'a') as f:
        #     f.write(mytext)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[11번가키워드]가 저장되었습니다.')
    def auction_savekeywordfile(self):
        print('저장')
        # with open('somefile.txt', 'a') as f:
        #     f.write(mytext)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[옥션키워드]가 저장되었습니다.')
    def gmarket_savekeywordfile(self):
        print('저장')
        # with open('somefile.txt', 'a') as f:
        #     f.write(mytext)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[지마켓키워드]가 저장되었습니다.')
    def relatedtags_savekeywordfile(self):
        print('저장')
        # with open('somefile.txt', 'a') as f:
        #     f.write(mytext)
        self.textBrowser.append(self.now().strftime("[%H:%M:%S]")+'[관련태그]가 저장되었습니다.')