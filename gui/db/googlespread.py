import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time




class GoogleSpreadSheet:

    def isapi(self,path):
        self.path = path
        try:
            with open(path, 'r') as file_obj:
                client_credentials = json.load(file_obj)
        except Exception:
            return 'api 키가 없습니다. 연동 후 사용하세요.'
        
        return client_credentials['client_email']
    
    def getWorksheet(self,spreadsheet_url,sheet_name):
        '''setting.json 을 읽고 연동함'''
        try:
            scope = ['https://spreadsheets.google.com/feeds']
            try:
                json_file_name = self.path
            except Exception:
                json_file_name = './DATA/setting.json'

            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
            gc = gspread.authorize(credentials)
            doc = gc.open_by_url(spreadsheet_url)
            self.worksheet = doc.worksheet(sheet_name)
            return self.worksheet,True
        except Exception as e:
            return (e),False

    def getAllValues(self):
        '''값을 리스트로 받아옴'''

        return self.worksheet.get_all_values()
        # try:
        # except Exception as e:
        #     print(e)
        #     return False


    def updateCells(self,cells):
        '''여러개 셀을 수정함'''
        for _ in range(60):
            try:
                self.worksheet.update_cells(cells)
                return True
            except Exception as e:
                print(e)
                time.sleep(1)
        return False

            
    def updateCell(self,row,col,value):
        '''한개의 셀을 수정함'''
        try:
            self.worksheet.update_cell(row,col,value)
        except Exception as e:
            print(e)
            return False


    