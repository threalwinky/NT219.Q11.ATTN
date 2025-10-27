# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pushdatanEjIvS.ui'
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

class Ui_PushWindow(object):
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
                border: 2px solid #00AA66;
                border-radius: 10px;
                padding: 5px 10px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 3px solid #00CC77;
                background-color: white;
            }
        """
        
        # UID input
        self.UID = QLineEdit(self.centralwidget)
        self.UID.setObjectName(u"UID")
        self.UID.setGeometry(QRect(280, 130, 340, 45))
        self.UID.setFont(font)
        self.UID.setStyleSheet(input_style)
        
        # Name input
        self.NAME = QLineEdit(self.centralwidget)
        self.NAME.setObjectName(u"NAME")
        self.NAME.setGeometry(QRect(280, 195, 340, 50))
        self.NAME.setFont(font)
        self.NAME.setStyleSheet(input_style)
        
        # File name input (read-only)
        self.FileName = QLineEdit(self.centralwidget)
        self.FileName.setObjectName(u"FileName")
        self.FileName.setGeometry(QRect(280, 265, 340, 45))
        self.FileName.setReadOnly(True)
        self.FileName.setFont(font)
        self.FileName.setStyleSheet("""
            QLineEdit {
                background-color: rgba(240, 240, 240, 0.95);
                border: 2px solid #00AA66;
                border-radius: 10px;
                padding: 5px 10px;
                color: #555555;
            }
        """)
        
        # Browse button
        self.browse_button = QPushButton(self.centralwidget)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.setGeometry(QRect(630, 265, 110, 45))
        browse_font = QFont()
        browse_font.setFamily("Segoe UI")
        browse_font.setPointSize(11)
        browse_font.setBold(True)
        self.browse_button.setFont(browse_font)
        self.browse_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #0066CC;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0099FF;
            }
            QPushButton:pressed {
                background-color: #0052A3;
            }
        """)
        
        # Collection type label
        collection_label = QLabel(self.centralwidget)
        collection_label.setGeometry(QRect(290, 335, 150, 30))
        collection_label.setText("Record Type:")
        label_font = QFont()
        label_font.setFamily("Segoe UI")
        label_font.setPointSize(12)
        label_font.setBold(True)
        collection_label.setFont(label_font)
        collection_label.setStyleSheet("color: white; background: rgba(0, 0, 0, 0.6); padding: 5px; border-radius: 5px;")
        
        # Collection combo box
        self.collection = QComboBox(self.centralwidget)
        self.collection.addItem("")
        self.collection.addItem("")
        self.collection.addItem("")
        self.collection.addItem("")
        self.collection.setObjectName(u"collection")
        self.collection.setGeometry(QRect(450, 335, 220, 35))
        combo_font = QFont()
        combo_font.setFamily("Segoe UI")
        combo_font.setPointSize(9)
        self.collection.setFont(combo_font)
        self.collection.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid #00AA66;
                border-radius: 8px;
                padding: 2px 5px;
                color: #333333;
            }
            QComboBox:hover {
                border: 2px solid #00CC77;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        
        # Push button
        self.push_button = QPushButton(self.centralwidget)
        self.push_button.setObjectName(u"push_button")
        self.push_button.setGeometry(QRect(310, 410, 280, 65))
        button_font = QFont()
        button_font.setFamily("Segoe UI")
        button_font.setPointSize(18)
        button_font.setBold(True)
        self.push_button.setFont(button_font)
        self.push_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button.setStyleSheet("""
            QPushButton {
                background-color: #00AA66;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 18px;
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
        self.back_button.setGeometry(QRect(750, 550, 120, 45))
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
        self.menubar.setStyleSheet("background-color: #00AA66; color: white;")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet("background-color: #00AA66; color: white;")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hospital Records System - Upload", None))
        self.UID.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Patient UID", None))
        self.NAME.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Patient Name", None))
        self.FileName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select a file to upload...", None))
        self.browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.push_button.setText(QCoreApplication.translate("MainWindow", u"UPLOAD", None))
        self.collection.setItemText(0, QCoreApplication.translate("MainWindow", u"health_record", None))
        self.collection.setItemText(1, QCoreApplication.translate("MainWindow", u"research_record", None))
        self.collection.setItemText(2, QCoreApplication.translate("MainWindow", u"medicine_record", None))
        self.collection.setItemText(3, QCoreApplication.translate("MainWindow", u"financial_record", None))
        self.back_button.setText(QCoreApplication.translate("MainWindow", u"Back", None))