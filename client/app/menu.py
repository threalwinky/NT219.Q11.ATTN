# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menuOwAupO.ui'
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
    QSizePolicy, QStatusBar, QWidget, QLabel)
import os

class Ui_MenuWindow(object):
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
        
        button_font = QFont()
        button_font.setFamily("Segoe UI")
        button_font.setPointSize(16)
        button_font.setBold(True)
        
        button_style = """
            QPushButton {
                background-color: rgba(0, 102, 204, 0.9);
                color: white;
                border: 2px solid #0066CC;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 153, 255, 0.95);
                border: 2px solid #0099FF;
            }
            QPushButton:pressed {
                background-color: rgba(0, 82, 164, 0.95);
            }
        """
        
        # Search button
        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setGeometry(QRect(300, 140, 300, 65))
        self.search_button.setFont(button_font)
        self.search_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_button.setStyleSheet(button_style)
        
        # View button
        self.view_button = QPushButton(self.centralwidget)
        self.view_button.setObjectName(u"view_button")
        self.view_button.setGeometry(QRect(300, 225, 300, 65))
        self.view_button.setFont(button_font)
        self.view_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.view_button.setStyleSheet(button_style)
        
        # Upload button
        self.upload_button = QPushButton(self.centralwidget)
        self.upload_button.setObjectName(u"upload_button")
        self.upload_button.setGeometry(QRect(300, 310, 300, 65))
        self.upload_button.setFont(button_font)
        self.upload_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 170, 102, 0.9);
                color: white;
                border: 2px solid #00AA66;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 204, 119, 0.95);
                border: 2px solid #00CC77;
            }
            QPushButton:pressed {
                background-color: rgba(0, 136, 85, 0.95);
            }
        """)
        
        # Update button
        self.update_button = QPushButton(self.centralwidget)
        self.update_button.setObjectName(u"update_button")
        self.update_button.setGeometry(QRect(300, 395, 300, 65))
        self.update_button.setFont(button_font)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 140, 0, 0.9);
                color: white;
                border: 2px solid #FF8C00;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 165, 0, 0.95);
                border: 2px solid #FFA500;
            }
            QPushButton:pressed {
                background-color: rgba(204, 112, 0, 0.95);
            }
        """)
        
        logout_font = QFont()
        logout_font.setFamily("Segoe UI")
        logout_font.setPointSize(12)
        logout_font.setBold(True)
        
        self.logout_button = QPushButton(self.centralwidget)
        self.logout_button.setObjectName(u"logout_button")
        self.logout_button.setGeometry(QRect(350, 540, 200, 45))
        self.logout_button.setFont(logout_font)
        self.logout_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(220, 53, 69, 0.9);
                color: white;
                border: 2px solid #DC3545;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 75, 90, 0.95);
                border: 2px solid #FF4B5A;
            }
            QPushButton:pressed {
                background-color: rgba(180, 43, 56, 0.95);
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

        # User info label
        self.text_label = QLabel(self.centralwidget)
        self.text_label.setObjectName(u"text_label")
        self.text_label.setGeometry(QRect(300, 490, 300, 40))
        info_font = QFont()
        info_font.setFamily("Segoe UI")
        info_font.setPointSize(12)
        info_font.setBold(True)
        self.text_label.setFont(info_font)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("""
            color: #FFFFFF;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            padding: 8px;
        """)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hospital Records System - Main Menu", None))
        self.search_button.setText(QCoreApplication.translate("MainWindow", u"Search Records", None))
        self.view_button.setText(QCoreApplication.translate("MainWindow", u"View Records", None))
        self.upload_button.setText(QCoreApplication.translate("MainWindow", u"Upload New Record", None))
        self.update_button.setText(QCoreApplication.translate("MainWindow", u"Update Record", None))
        self.logout_button.setText(QCoreApplication.translate("MainWindow", u"Logout", None))