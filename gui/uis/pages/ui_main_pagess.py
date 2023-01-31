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

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        MainPages.setObjectName("MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName("main_pages_layout")
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName("pages")
        self.page_2 = QWidget()
        self.page_2.setStyleSheet("font-size: 14pt")
        self.page_2.setObjectName("page_2")
        self.page_1_layout = QVBoxLayout(self.page_2)
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName("page_1_layout")
        self.pages.addWidget(self.page_2)
        self.page_1 = QWidget()
        self.page_1.setObjectName("page_1")
        self.page_2_layout = QVBoxLayout(self.page_1)
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName("page_2_layout")
        self.scroll_area = QScrollArea(self.page_1)
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.contents = QWidget()
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet("background: transparent;")
        self.contents.setObjectName("contents")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QLabel(self.contents)
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.description_label = QLabel(self.contents)
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)
        self.description_label.setObjectName("description_label")
        self.verticalLayout.addWidget(self.description_label)
        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName("row_1_layout")
        self.verticalLayout.addLayout(self.row_1_layout)
        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName("row_2_layout")
        self.verticalLayout.addLayout(self.row_2_layout)
        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName("row_3_layout")
        self.verticalLayout.addLayout(self.row_3_layout)
        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName("row_4_layout")
        self.verticalLayout.addLayout(self.row_4_layout)
        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName("row_5_layout")
        self.verticalLayout.addLayout(self.row_5_layout)
        self.scroll_area.setWidget(self.contents)
        self.page_2_layout.addWidget(self.scroll_area)
        self.pages.addWidget(self.page_1)
        self.page_3 = QWidget()
        self.page_3.setStyleSheet("QFrame {\n"
"    font-size: 16pt;\n"
"}")
        self.page_3.setObjectName("page_3")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName("page_3_layout")
        self.label = QLabel(self.page_3)
        self.label.setObjectName("label")
        self.page_3_layout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.page_3_layout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.page_3_layout.addLayout(self.verticalLayout_2)
        self.pages.addWidget(self.page_3)
        self.main_pages_layout.addWidget(self.pages)
        
        self.retranslateUi(MainPages)
        self.pages.setCurrentIndex(2)
        QMetaObject.connectSlotsByName(MainPages)

    def retranslateUi(self, MainPages):
        _translate = QCoreApplication.translate
        MainPages.setWindowTitle(_translate("MainPages", "Form"))
        self.title_label.setText(_translate("MainPages", "Custom Widgedsdsts Page"))
        self.description_label.setText(_translate("MainPages", "fuck"))
        self.label.setText(_translate("MainPages", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainPages = QWidget()
    ui = Ui_MainPages()
    ui.setupUi(MainPages)
    MainPages.show()
    sys.exit(app.exec_())
