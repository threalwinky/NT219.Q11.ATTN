# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginduDxgn.ui'
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
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QWidget, QLineEdit, QLabel)
import os

class Ui_LoginWindow(object):
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
        
        # Username input
        self.username_textbox = QLineEdit(self.centralwidget)
        self.username_textbox.setObjectName(u"username_textbox")
        self.username_textbox.setGeometry(QRect(300, 200, 300, 50))
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.username_textbox.setFont(font)
        self.username_textbox.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid #0066CC;
                border-radius: 10px;
                padding: 5px 10px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 3px solid #0099FF;
                background-color: rgba(255, 255, 255, 1);
            }
        """)
        
        # Password input
        self.password_textbox = QLineEdit(self.centralwidget)
        self.password_textbox.setObjectName(u"password_textbox")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_textbox.setGeometry(QRect(300, 270, 300, 50))
        self.password_textbox.setFont(font)
        self.password_textbox.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid #0066CC;
                border-radius: 10px;
                padding: 5px 10px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 3px solid #0099FF;
                background-color: rgba(255, 255, 255, 1);
            }
        """)
        
        # Login button
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(350, 370, 200, 60))
        button_font = QFont()
        button_font.setFamily("Segoe UI")
        button_font.setPointSize(18)
        button_font.setBold(True)
        self.pushButton.setFont(button_font)
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("""
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hospital Records System - Login", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"LOGIN", None))
        self.username_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.password_textbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
