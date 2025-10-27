# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchIFsfKY.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QLineEdit,
    QWidget, QLabel)
import os

class Ui_SearchWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setMinimumSize(900, 650)
        MainWindow.setMaximumSize(900, 650)
        
        # Set window background
        bg_path = os.path.join(os.path.dirname(__file__), '..', 'bg.jpg')
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(True)
        palette = self.centralwidget.palette()
        pixmap = QPixmap(bg_path)
        scaled_pixmap = pixmap.scaled(900, 650, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.centralwidget.setPalette(palette)
        
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        
        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid #0066CC;
                border-radius: 10px;
                padding: 5px 10px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 3px solid #0099FF;
                background-color: white;
            }
        """
        
        # User ID input
        self.userid_textbox = QLineEdit(self.centralwidget)
        self.userid_textbox.setObjectName(u"userid_textbox")
        self.userid_textbox.setGeometry(QRect(300, 140, 300, 50))
        self.userid_textbox.setFont(font)
        self.userid_textbox.setStyleSheet(input_style)
        
        # Name input
        self.name_textbox = QLineEdit(self.centralwidget)
        self.name_textbox.setObjectName(u"name_textbox")
        self.name_textbox.setGeometry(QRect(300, 210, 300, 50))
        self.name_textbox.setFont(font)
        self.name_textbox.setStyleSheet(input_style)
        
        # Collection type label
        collection_label = QLabel(self.centralwidget)
        collection_label.setGeometry(QRect(270, 280, 150, 30))
        collection_label.setText("Record Type:")
        label_font = QFont()
        label_font.setFamily("Segoe UI")
        label_font.setPointSize(12)
        label_font.setBold(True)
        collection_label.setFont(label_font)
        collection_label.setStyleSheet("color: white; background: rgba(0, 0, 0, 0.6); padding: 5px; border-radius: 5px;")
        
        # Collection combo box
        self.combo_box = QComboBox(self.centralwidget)
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.setObjectName(u"combo_box")
        self.combo_box.setGeometry(QRect(460, 280, 200, 35))
        combo_font = QFont()
        combo_font.setFamily("Segoe UI")
        combo_font.setPointSize(9)
        self.combo_box.setFont(combo_font)
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid #0066CC;
                border-radius: 8px;
                padding: 2px 5px;
                color: #333333;
            }
            QComboBox:hover {
                border: 2px solid #0099FF;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        
        # Search button
        self.search_api_button = QPushButton(self.centralwidget)
        self.search_api_button.setObjectName(u"search_api_button")
        self.search_api_button.setGeometry(QRect(325, 360, 250, 60))
        button_font = QFont()
        button_font.setFamily("Segoe UI")
        button_font.setPointSize(16)
        button_font.setBold(True)
        self.search_api_button.setFont(button_font)
        self.search_api_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_api_button.setStyleSheet("""
            QPushButton {
                background-color: #00AA66;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #00CC77;
            }
            QPushButton:pressed {
                background-color: #008855;
            }
        """)
        
        # Back button
        self.back_button = QPushButton(self.centralwidget)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setGeometry(QRect(750, 500, 120, 45))
        back_font = QFont()
        back_font.setFamily("Segoe UI")
        back_font.setPointSize(12)
        back_font.setBold(True)
        self.back_button.setFont(back_font)
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(120, 120, 120, 0.9);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(140, 140, 140, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(100, 100, 100, 0.95);
            }
        """)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 22))
        self.menubar.setStyleSheet("background-color: #0066CC; color: white;")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet("background-color: #0066CC; color: white;")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hospital Records System - Search", None))
        self.userid_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"User ID (Optional)", None))
        self.name_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Patient Name (Optional)", None))
        self.search_api_button.setText(QCoreApplication.translate("MainWindow", u"SEARCH", None))
        self.combo_box.setItemText(0, QCoreApplication.translate("MainWindow", u"health_record", None))
        self.combo_box.setItemText(1, QCoreApplication.translate("MainWindow", u"research_record", None))
        self.combo_box.setItemText(2, QCoreApplication.translate("MainWindow", u"medicine_record", None))
        self.combo_box.setItemText(3, QCoreApplication.translate("MainWindow", u"financial_record", None))
        self.back_button.setText(QCoreApplication.translate("MainWindow", u"Back", None))