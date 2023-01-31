# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import json
import os
import sys

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# APP THEMES
# ///////////////////////////////////////////////////////////////
class Themes(object):
    # LOAD SETTINGS
    # ///////////////////////////////////////////////////////////////
    setup_settings = Settings()
    _settings = setup_settings.items
    notfile = False
    # APP PATH
    # ///////////////////////////////////////////////////////////////
    json_file = f"gui/themes/{_settings['theme_name']}.json"
    app_path = os.path.abspath(os.getcwd())
    
    jsonthemepath = os.path.normpath(os.path.join(app_path, json_file))
    if not os.path.isfile(jsonthemepath):
        print(f"WARNING: \"gui/themes/{_settings['theme_name']}.json\" not found! check in the folder {jsonthemepath}")
        notfile = True
    # INIT SETTINGS
    # ///////////////////////////////////////////////////////////////
    def __init__(self):
        super(Themes, self).__init__()

        # DICTIONARY WITH SETTINGS
        self.items = {}
        if self.notfile:
            if getattr(sys, 'frozen', False):
                self.jsonthemepath = os.path.dirname(sys.executable)
            elif __file__:
                self.jsonthemepath = os.path.dirname(__file__)
            if self.jsonthemepath == '':        
                self.jsonthemepath = os.getcwd()
            print('@@@',self.jsonthemepath)
            self.jsonthemepath = os.path.normpath(os.path.join(self.jsonthemepath,self.json_file))
            print('@@@',self.jsonthemepath)
            # print('@@@@@@@@@@')
            # input(self.jsonthemepath)
        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def serialize(self):
        # WRITE JSON FILE
        with open(self.jsonthemepath, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def deserialize(self):
        # READ JSON FILE
        with open(self.jsonthemepath, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings


    def customWidget(self):
        '''위젯'''
        self.stylesheet = f"""
            QMainWindow (((
                background-color : {self.items['app_color']['bg_one']};
                border-radius:8px;
            )))
            QWidget (((
                background-color : {self.items['app_color']['bg_one']};
                border-radius:8px;
            )))
            QTabWidget::pane (((
            border: 1px solid lightgray;
            top:-1px; 
            background-color : {self.items['app_color']['bg_one']};
            border-radius:8px;
            ))) 

            QTabBar::tab (((
            background-color : {self.items['app_color']['bg_one']};
            border: 1px solid lightgray; 
            padding: 8px;
            border-radius:8px;
            ))) 

            QTabBar::tab:selected ((( 
                color: rgb(100, 83, 149);
                background-color: white;
                border: 2px solid rgb(12, 83, 149);
                border-radius: 8px;
            )))
            QTextEdit (((
                background-color : #FFFFFF;
                border-radius:8px;
            )))
            QCheckBox (((
                background-color : rgb(207, 226, 243);
                border-radius:8px;
            )))
            QLineEdit (((
                background-color: {self.items["app_color"]["dark_one"]};
                border-radius: 8px;
                border: 2px solid transparent;
                padding-left: 10px;
                padding-right: 10px;
                selection-color: {self.items["app_color"]["white"]};
                selection-background-color: {self.items["app_color"]["context_color"]};
                color: {self.items["app_color"]["text_foreground"]};
            )))
            QLineEdit:focus (((
                border: 2px solid {self.items["app_color"]["context_color"]};
                background-color: {self.items["app_color"]["dark_three"]};
            )))
            QPushButton:pressed (((	
                background-color: {self.items["app_color"]["dark_four"]};
            )))
            QPushButton(((
                color: {self.items["app_color"]["text_foreground"]};
                background-color: {self.items["app_color"]["dark_one"]};
                border-radius: 8px;
            )))
            QPushButton:hover (((
                background-color: {self.items["app_color"]["dark_three"]};
                color: {self.items["app_color"]["text_foreground"]};
            )))
            QPushButton:disabled (((
                background-color : rgb(204, 204, 204 );
                border-radius:8px;
            )))
            QLabel (((
                color: {self.items["app_color"]["text_foreground"]};
                border-radius:8px;
            )))
            QMenuBar (((
                background-color : {self.items['app_color']['dark_one']};
                border-radius:8px;
            )))
            QStatusBar (((
                background-color : {self.items['app_color']['dark_one']};
                border-radius:8px;
            )))

            QGroupBox (((
            border: 1px solid gray;
            border-color: #FFFFFF;
            font-size: 14px;
            border-radius:8px;
            )))
            QGroupBox::title (((
            background-color: #FFFFFF;
            color: {self.items["app_color"]["text_foreground"]};
            border-radius:8px;
            )))
            QHeaderView::section(((
            background-color: #FFFFFF;
            color: {self.items["app_color"]["text_foreground"]};
            border-radius:8px;
            )))                         
            """.replace('(((','{').replace(')))','}')
        # print(self.stylesheet)
        return self.stylesheet
        # style = f'''
        #     font: {self.settings["font"]["text_size"]}pt "{self.settings["font"]["family"]}";
        #     color: {self.items["app_color"]["text_foreground"]};
        # '''