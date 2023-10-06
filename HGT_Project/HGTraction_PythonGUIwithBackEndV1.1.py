"""
HGTraction_Main_V1.1.py
Edward Katz
07/17/2023

This code uses pre-designed code created in PyQT Designer, usually included
in PyQt5 tools. The code from the design is simply copied into this file, hense
the "Ui_Form" class in the beginning of the code. Actual running code begins later.
PyQt5 can be downloaded to your device by running the following
command in your device's command module:

pip install pyqt5

No external files are used in this particular code. Every aspect is included in PyQt5 libraries.

"""


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from hx711 import HX711

import socket
import random

import time
import RPi.GPIO as GPIO
import curses
import math


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HGTui_mainScreenV2zNLRLC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################



from pyqtgraph import PlotWidget

#import PyQTResource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setFixedSize(800, 480)
        self.timeDelayLCD = QLCDNumber(Form)
        self.timeDelayLCD.setObjectName(u"timeDelayLCD")
        self.timeDelayLCD.setGeometry(QRect(140, 400, 91, 31))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 400, 101, 31))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 240, 151, 31))
        self.setTensionLCD = QLCDNumber(Form)
        self.setTensionLCD.setObjectName(u"setTensionLCD")
        self.setTensionLCD.setGeometry(QRect(30, 300, 101, 41))
        self.currentWeightLCD = QLCDNumber(Form)
        self.currentWeightLCD.setObjectName(u"currentWeightLCD")
        self.currentWeightLCD.setGeometry(QRect(30, 70, 201, 111))
        self.currentWeightLCD.setAutoFillBackground(False)
        self.currentWeightLCD.setSmallDecimalPoint(False)
        self.currentWeightLCD.setDigitCount(3)
        self.currentWeightLCD.setSegmentStyle(QLCDNumber.Filled)
        self.currentWeightLCD.setProperty("value", 0.000000000000000)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 251, 51))
        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(180, 280, 95, 81))
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayoutWidget_2.sizePolicy().hasHeightForWidth())
        self.verticalLayoutWidget_2.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tensionUp = QPushButton(self.verticalLayoutWidget_2)
        self.tensionUp.setObjectName(u"tensionUp")
        sizePolicy.setHeightForWidth(self.tensionUp.sizePolicy().hasHeightForWidth())
        self.tensionUp.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.tensionUp.setFont(font)

        self.verticalLayout_3.addWidget(self.tensionUp)

        self.tensionDown = QPushButton(self.verticalLayoutWidget_2)
        self.tensionDown.setObjectName(u"tensionDown")
        sizePolicy.setHeightForWidth(self.tensionDown.sizePolicy().hasHeightForWidth())
        self.tensionDown.setSizePolicy(sizePolicy)
        self.tensionDown.setFont(font)

        self.verticalLayout_3.addWidget(self.tensionDown)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(280, 10, 20, 441))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setWeight(50)
        self.line.setFont(font1)
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.VLine)
        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(30, 200, 221, 20))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(30, 370, 221, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(420, 20, 361, 411))
        self.setTension = QWidget()
        self.setTension.setObjectName(u"setTension")
        self.gridLayoutWidget = QWidget(self.setTension)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 150, 331, 261))
        sizePolicy.setHeightForWidth(self.gridLayoutWidget.sizePolicy().hasHeightForWidth())
        self.gridLayoutWidget.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(14)
        self.gridLayoutWidget.setFont(font2)
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.keypad4 = QPushButton(self.gridLayoutWidget)
        self.keypad4.setObjectName(u"keypad4")
        sizePolicy.setHeightForWidth(self.keypad4.sizePolicy().hasHeightForWidth())
        self.keypad4.setSizePolicy(sizePolicy)
        self.keypad4.setFont(font2)

        self.gridLayout.addWidget(self.keypad4, 1, 0, 1, 1)

        self.keypad8 = QPushButton(self.gridLayoutWidget)
        self.keypad8.setObjectName(u"keypad8")
        sizePolicy.setHeightForWidth(self.keypad8.sizePolicy().hasHeightForWidth())
        self.keypad8.setSizePolicy(sizePolicy)
        self.keypad8.setFont(font2)

        self.gridLayout.addWidget(self.keypad8, 2, 1, 1, 1)

        self.keypad2 = QPushButton(self.gridLayoutWidget)
        self.keypad2.setObjectName(u"keypad2")
        sizePolicy.setHeightForWidth(self.keypad2.sizePolicy().hasHeightForWidth())
        self.keypad2.setSizePolicy(sizePolicy)
        self.keypad2.setFont(font2)

        self.gridLayout.addWidget(self.keypad2, 0, 1, 1, 1)

        self.keypad9 = QPushButton(self.gridLayoutWidget)
        self.keypad9.setObjectName(u"keypad9")
        sizePolicy.setHeightForWidth(self.keypad9.sizePolicy().hasHeightForWidth())
        self.keypad9.setSizePolicy(sizePolicy)
        self.keypad9.setFont(font2)

        self.gridLayout.addWidget(self.keypad9, 2, 2, 1, 1)

        self.keypad0 = QPushButton(self.gridLayoutWidget)
        self.keypad0.setObjectName(u"keypad0")
        sizePolicy.setHeightForWidth(self.keypad0.sizePolicy().hasHeightForWidth())
        self.keypad0.setSizePolicy(sizePolicy)
        self.keypad0.setFont(font2)

        self.gridLayout.addWidget(self.keypad0, 3, 1, 1, 1)

        self.keypad7 = QPushButton(self.gridLayoutWidget)
        self.keypad7.setObjectName(u"keypad7")
        sizePolicy.setHeightForWidth(self.keypad7.sizePolicy().hasHeightForWidth())
        self.keypad7.setSizePolicy(sizePolicy)
        self.keypad7.setFont(font2)

        self.gridLayout.addWidget(self.keypad7, 2, 0, 1, 1)

        self.keypadDecimal = QPushButton(self.gridLayoutWidget)
        self.keypadDecimal.setObjectName(u"keypadDecimal")
        sizePolicy.setHeightForWidth(self.keypadDecimal.sizePolicy().hasHeightForWidth())
        self.keypadDecimal.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setPointSize(11)
        self.keypadDecimal.setFont(font3)

        self.gridLayout.addWidget(self.keypadDecimal, 3, 0, 1, 1)

        self.keypadEnter = QPushButton(self.gridLayoutWidget)
        self.keypadEnter.setObjectName(u"keypadEnter")
        sizePolicy.setHeightForWidth(self.keypadEnter.sizePolicy().hasHeightForWidth())
        self.keypadEnter.setSizePolicy(sizePolicy)
        self.keypadEnter.setFont(font3)

        self.gridLayout.addWidget(self.keypadEnter, 3, 2, 1, 1)

        self.keypad1 = QPushButton(self.gridLayoutWidget)
        self.keypad1.setObjectName(u"keypad1")
        sizePolicy.setHeightForWidth(self.keypad1.sizePolicy().hasHeightForWidth())
        self.keypad1.setSizePolicy(sizePolicy)
        self.keypad1.setFont(font2)
        self.keypad1.setContextMenuPolicy(Qt.NoContextMenu)
        self.keypad1.setIconSize(QSize(20, 20))
        self.keypad1.setAutoRepeatDelay(293)

        self.gridLayout.addWidget(self.keypad1, 0, 0, 1, 1)

        self.keypad3 = QPushButton(self.gridLayoutWidget)
        self.keypad3.setObjectName(u"keypad3")
        sizePolicy.setHeightForWidth(self.keypad3.sizePolicy().hasHeightForWidth())
        self.keypad3.setSizePolicy(sizePolicy)
        self.keypad3.setFont(font2)

        self.gridLayout.addWidget(self.keypad3, 0, 2, 1, 1)

        self.keypad6 = QPushButton(self.gridLayoutWidget)
        self.keypad6.setObjectName(u"keypad6")
        sizePolicy.setHeightForWidth(self.keypad6.sizePolicy().hasHeightForWidth())
        self.keypad6.setSizePolicy(sizePolicy)
        self.keypad6.setFont(font2)

        self.gridLayout.addWidget(self.keypad6, 1, 2, 1, 1)

        self.keypad5 = QPushButton(self.gridLayoutWidget)
        self.keypad5.setObjectName(u"keypad5")
        sizePolicy.setHeightForWidth(self.keypad5.sizePolicy().hasHeightForWidth())
        self.keypad5.setSizePolicy(sizePolicy)
        self.keypad5.setFont(font2)

        self.gridLayout.addWidget(self.keypad5, 1, 1, 1, 1)

        self.manualSetTensionLCD = QLCDNumber(self.setTension)
        self.manualSetTensionLCD.setObjectName(u"manualSetTensionLCD")
        self.manualSetTensionLCD.setGeometry(QRect(100, 70, 161, 61))
        self.label_4 = QLabel(self.setTension)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 0, 331, 41))
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setFrameShape(QFrame.Panel)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.line_4 = QFrame(self.setTension)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(0, 40, 341, 20))
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QFrame.HLine)
        self.label_8 = QLabel(self.setTension)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(True)
        self.label_8.setGeometry(QRect(270, 60, 71, 31))
        font4 = QFont()
        font4.setFamily(u"Sitka Subheading")
        font4.setPointSize(14)
        font4.setBold(False)
        font4.setWeight(50)
        self.label_8.setFont(font4)
        self.setMark = QLabel(self.setTension)
        self.setMark.setObjectName(u"setMark")
        self.setMark.setEnabled(True)
        self.setMark.setGeometry(QRect(30, 70, 161, 61))
        self.setMark.setFont(font4)
        self.keypadClear = QPushButton(self.setTension)
        self.keypadClear.setObjectName(u"keypadClear")
        self.keypadClear.setGeometry(QRect(270, 100, 71, 41))
        sizePolicy.setHeightForWidth(self.keypadClear.sizePolicy().hasHeightForWidth())
        self.keypadClear.setSizePolicy(sizePolicy)
        font5 = QFont()
        font5.setPointSize(14)
        font5.setBold(True)
        font5.setWeight(75)
        self.keypadClear.setFont(font5)
        self.tooLargeLabel = QLabel(self.setTension)
        self.tooLargeLabel.setObjectName(u"tooLargeLabel")
        self.tooLargeLabel.setEnabled(True)
        self.tooLargeLabel.setGeometry(QRect(10, 60, 101, 71))
        self.tooLargeLabel.setFont(font4)
        self.tooLargeLabel.setTextFormat(Qt.AutoText)
        self.tooLargeLabel.setScaledContents(False)
        self.tooLargeLabel.setWordWrap(True)
        self.stackedWidget.addWidget(self.setTension)
        self.setTimeDelay = QWidget()
        self.setTimeDelay.setObjectName(u"setTimeDelay")
        self.manualSetTimeDelayLCD = QLCDNumber(self.setTimeDelay)
        self.manualSetTimeDelayLCD.setObjectName(u"manualSetTimeDelayLCD")
        self.manualSetTimeDelayLCD.setGeometry(QRect(100, 70, 161, 61))
        self.label_5 = QLabel(self.setTimeDelay)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 0, 341, 41))
        self.label_5.setLayoutDirection(Qt.LeftToRight)
        self.label_5.setFrameShape(QFrame.Panel)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.line_5 = QFrame(self.setTimeDelay)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(0, 40, 341, 20))
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setLineWidth(3)
        self.line_5.setFrameShape(QFrame.HLine)
        self.gridLayoutWidget_2 = QWidget(self.setTimeDelay)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 150, 331, 261))
        sizePolicy.setHeightForWidth(self.gridLayoutWidget_2.sizePolicy().hasHeightForWidth())
        self.gridLayoutWidget_2.setSizePolicy(sizePolicy)
        self.gridLayoutWidget_2.setFont(font2)
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.keypad0_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad0_2.setObjectName(u"keypad0_2")
        sizePolicy.setHeightForWidth(self.keypad0_2.sizePolicy().hasHeightForWidth())
        self.keypad0_2.setSizePolicy(sizePolicy)
        self.keypad0_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad0_2, 3, 1, 1, 1)

        self.keypad2_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad2_2.setObjectName(u"keypad2_2")
        sizePolicy.setHeightForWidth(self.keypad2_2.sizePolicy().hasHeightForWidth())
        self.keypad2_2.setSizePolicy(sizePolicy)
        self.keypad2_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad2_2, 0, 1, 1, 1)

        self.keypad9_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad9_2.setObjectName(u"keypad9_2")
        sizePolicy.setHeightForWidth(self.keypad9_2.sizePolicy().hasHeightForWidth())
        self.keypad9_2.setSizePolicy(sizePolicy)
        self.keypad9_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad9_2, 2, 2, 1, 1)

        self.keypad1_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad1_2.setObjectName(u"keypad1_2")
        sizePolicy.setHeightForWidth(self.keypad1_2.sizePolicy().hasHeightForWidth())
        self.keypad1_2.setSizePolicy(sizePolicy)
        self.keypad1_2.setFont(font2)
        self.keypad1_2.setContextMenuPolicy(Qt.NoContextMenu)
        self.keypad1_2.setIconSize(QSize(20, 20))
        self.keypad1_2.setAutoRepeatDelay(293)

        self.gridLayout_2.addWidget(self.keypad1_2, 0, 0, 1, 1)

        self.keypad4_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad4_2.setObjectName(u"keypad4_2")
        sizePolicy.setHeightForWidth(self.keypad4_2.sizePolicy().hasHeightForWidth())
        self.keypad4_2.setSizePolicy(sizePolicy)
        self.keypad4_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad4_2, 1, 0, 1, 1)

        self.keypadEnter_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypadEnter_2.setObjectName(u"keypadEnter_2")
        sizePolicy.setHeightForWidth(self.keypadEnter_2.sizePolicy().hasHeightForWidth())
        self.keypadEnter_2.setSizePolicy(sizePolicy)
        self.keypadEnter_2.setFont(font3)

        self.gridLayout_2.addWidget(self.keypadEnter_2, 3, 2, 1, 1)

        self.keypad8_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad8_2.setObjectName(u"keypad8_2")
        sizePolicy.setHeightForWidth(self.keypad8_2.sizePolicy().hasHeightForWidth())
        self.keypad8_2.setSizePolicy(sizePolicy)
        self.keypad8_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad8_2, 2, 1, 1, 1)

        self.keypad6_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad6_2.setObjectName(u"keypad6_2")
        sizePolicy.setHeightForWidth(self.keypad6_2.sizePolicy().hasHeightForWidth())
        self.keypad6_2.setSizePolicy(sizePolicy)
        self.keypad6_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad6_2, 1, 2, 1, 1)

        self.keypad3_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad3_2.setObjectName(u"keypad3_2")
        sizePolicy.setHeightForWidth(self.keypad3_2.sizePolicy().hasHeightForWidth())
        self.keypad3_2.setSizePolicy(sizePolicy)
        self.keypad3_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad3_2, 0, 2, 1, 1)

        self.keypadDecimal_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypadDecimal_2.setObjectName(u"keypadDecimal_2")
        sizePolicy.setHeightForWidth(self.keypadDecimal_2.sizePolicy().hasHeightForWidth())
        self.keypadDecimal_2.setSizePolicy(sizePolicy)
        self.keypadDecimal_2.setFont(font3)

        self.gridLayout_2.addWidget(self.keypadDecimal_2, 3, 0, 1, 1)

        self.keypad5_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad5_2.setObjectName(u"keypad5_2")
        sizePolicy.setHeightForWidth(self.keypad5_2.sizePolicy().hasHeightForWidth())
        self.keypad5_2.setSizePolicy(sizePolicy)
        self.keypad5_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad5_2, 1, 1, 1, 1)

        self.keypad7_2 = QPushButton(self.gridLayoutWidget_2)
        self.keypad7_2.setObjectName(u"keypad7_2")
        sizePolicy.setHeightForWidth(self.keypad7_2.sizePolicy().hasHeightForWidth())
        self.keypad7_2.setSizePolicy(sizePolicy)
        self.keypad7_2.setFont(font2)

        self.gridLayout_2.addWidget(self.keypad7_2, 2, 0, 1, 1)

        self.label_9 = QLabel(self.setTimeDelay)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(270, 60, 71, 31))
        self.label_9.setFont(font4)
        self.setMark_2 = QLabel(self.setTimeDelay)
        self.setMark_2.setObjectName(u"setMark_2")
        self.setMark_2.setEnabled(True)
        self.setMark_2.setGeometry(QRect(30, 70, 161, 61))
        self.setMark_2.setFont(font4)
        self.keypadClear_2 = QPushButton(self.setTimeDelay)
        self.keypadClear_2.setObjectName(u"keypadClear_2")
        self.keypadClear_2.setGeometry(QRect(270, 100, 71, 41))
        sizePolicy.setHeightForWidth(self.keypadClear_2.sizePolicy().hasHeightForWidth())
        self.keypadClear_2.setSizePolicy(sizePolicy)
        self.keypadClear_2.setFont(font5)
        self.tooLargeLabel_2 = QLabel(self.setTimeDelay)
        self.tooLargeLabel_2.setObjectName(u"tooLargeLabel_2")
        self.tooLargeLabel_2.setEnabled(True)
        self.tooLargeLabel_2.setGeometry(QRect(10, 60, 81, 71))
        self.tooLargeLabel_2.setFont(font4)
        self.tooLargeLabel_2.setTextFormat(Qt.AutoText)
        self.tooLargeLabel_2.setScaledContents(False)
        self.tooLargeLabel_2.setAlignment(Qt.AlignCenter)
        self.tooLargeLabel_2.setWordWrap(True)
        self.stackedWidget.addWidget(self.setTimeDelay)
        self.setSchedule = QWidget()
        self.setSchedule.setObjectName(u"setSchedule")
        self.label_6 = QLabel(self.setSchedule)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(0, 0, 341, 41))
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setFrameShape(QFrame.Panel)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.line_6 = QFrame(self.setSchedule)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setGeometry(QRect(0, 40, 341, 20))
        self.line_6.setFrameShadow(QFrame.Plain)
        self.line_6.setLineWidth(3)
        self.line_6.setFrameShape(QFrame.HLine)
        self.stackedWidget.addWidget(self.setSchedule)
        self.tensionHistory = QWidget()
        self.tensionHistory.setObjectName(u"tensionHistory")
        self.label_7 = QLabel(self.tensionHistory)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(0, 0, 341, 41))
        self.label_7.setLayoutDirection(Qt.LeftToRight)
        self.label_7.setFrameShape(QFrame.Panel)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.line_7 = QFrame(self.tensionHistory)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setGeometry(QRect(0, 40, 341, 20))
        self.line_7.setFrameShadow(QFrame.Plain)
        self.line_7.setLineWidth(3)
        self.line_7.setFrameShape(QFrame.HLine)
        self.graphWidget = PlotWidget(self.tensionHistory)
        self.graphWidget.setObjectName(u"graphWidget")
        self.graphWidget.setGeometry(QRect(0, 80, 341, 321))
        self.stackedWidget.addWidget(self.tensionHistory)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(310, 10, 95, 431))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.setTensionButton = QPushButton(self.verticalLayoutWidget)
        self.setTensionButton.setObjectName(u"setTensionButton")
        sizePolicy.setHeightForWidth(self.setTensionButton.sizePolicy().hasHeightForWidth())
        self.setTensionButton.setSizePolicy(sizePolicy)
        font6 = QFont()
        font6.setPointSize(12)
        font6.setBold(True)
        font6.setWeight(75)
        self.setTensionButton.setFont(font6)

        self.verticalLayout.addWidget(self.setTensionButton)

        self.setTimeDelayButton = QPushButton(self.verticalLayoutWidget)
        self.setTimeDelayButton.setObjectName(u"setTimeDelayButton")
        sizePolicy.setHeightForWidth(self.setTimeDelayButton.sizePolicy().hasHeightForWidth())
        self.setTimeDelayButton.setSizePolicy(sizePolicy)
        self.setTimeDelayButton.setFont(font2)
        self.setTimeDelayButton.setMouseTracking(False)

        self.verticalLayout.addWidget(self.setTimeDelayButton)

        self.setScheduleButton = QPushButton(self.verticalLayoutWidget)
        self.setScheduleButton.setObjectName(u"setScheduleButton")
        sizePolicy.setHeightForWidth(self.setScheduleButton.sizePolicy().hasHeightForWidth())
        self.setScheduleButton.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setPointSize(12)
        self.setScheduleButton.setFont(font7)

        self.verticalLayout.addWidget(self.setScheduleButton)

        self.tensionHistoryButton = QPushButton(self.verticalLayoutWidget)
        self.tensionHistoryButton.setObjectName(u"tensionHistoryButton")
        sizePolicy.setHeightForWidth(self.tensionHistoryButton.sizePolicy().hasHeightForWidth())
        self.tensionHistoryButton.setSizePolicy(sizePolicy)
        self.tensionHistoryButton.setFont(font2)

        self.verticalLayout.addWidget(self.tensionHistoryButton)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(140, 320, 31, 16))
        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(240, 410, 41, 16))

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt;\">Time Delay:</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:14pt;\">Set Tension: </span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:20pt;\">Current Tension:</span></p></body></html>", None))
        self.tensionUp.setText(QCoreApplication.translate("Form", u"+", None))
        self.tensionDown.setText(QCoreApplication.translate("Form", u"-", None))
        self.keypad4.setText(QCoreApplication.translate("Form", u"4", None))
        self.keypad8.setText(QCoreApplication.translate("Form", u"8", None))
        self.keypad2.setText(QCoreApplication.translate("Form", u"2", None))
        self.keypad9.setText(QCoreApplication.translate("Form", u"9", None))
        self.keypad0.setText(QCoreApplication.translate("Form", u"0", None))
        self.keypad7.setText(QCoreApplication.translate("Form", u"7", None))
        self.keypadDecimal.setText(QCoreApplication.translate("Form", u".", None))
        self.keypadEnter.setText(QCoreApplication.translate("Form", u"ENTER", None))
        self.keypad1.setText(QCoreApplication.translate("Form", u"1", None))
        self.keypad3.setText(QCoreApplication.translate("Form", u"3", None))
        self.keypad6.setText(QCoreApplication.translate("Form", u"6", None))
        self.keypad5.setText(QCoreApplication.translate("Form", u"5", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Set Tension:</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Lbs. ", None))
        self.setMark.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" color:#ff0303;\">Set.</span></p></body></html>", None))
        self.keypadClear.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.tooLargeLabel.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0303;\">Entry must be &lt;50 lbs. </span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Set Time Delay:</span></p></body></html>", None))
        self.keypad0_2.setText(QCoreApplication.translate("Form", u"0", None))
        self.keypad2_2.setText(QCoreApplication.translate("Form", u"2", None))
        self.keypad9_2.setText(QCoreApplication.translate("Form", u"9", None))
        self.keypad1_2.setText(QCoreApplication.translate("Form", u"1", None))
        self.keypad4_2.setText(QCoreApplication.translate("Form", u"4", None))
        self.keypadEnter_2.setText(QCoreApplication.translate("Form", u"ENTER", None))
        self.keypad8_2.setText(QCoreApplication.translate("Form", u"8", None))
        self.keypad6_2.setText(QCoreApplication.translate("Form", u"6", None))
        self.keypad3_2.setText(QCoreApplication.translate("Form", u"3", None))
        self.keypadDecimal_2.setText(QCoreApplication.translate("Form", u".", None))
        self.keypad5_2.setText(QCoreApplication.translate("Form", u"5", None))
        self.keypad7_2.setText(QCoreApplication.translate("Form", u"7", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Sec.", None))
        self.setMark_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" color:#ff0000;\">Set. </span></p></body></html>", None))
        self.keypadClear_2.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.tooLargeLabel_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; color:#ff0303;\">Entry must be &lt;600 sec. </span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Set Schedule: </span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Tension History: </span></p></body></html>", None))
        self.setTensionButton.setText(QCoreApplication.translate("Form", u"Tension", None))
        self.setTimeDelayButton.setText(QCoreApplication.translate("Form", u"Delay", None))
        self.setScheduleButton.setText(QCoreApplication.translate("Form", u"Schedule", None))
        self.tensionHistoryButton.setText(QCoreApplication.translate("Form", u"History", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:9pt;\">Lbs.</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:9pt;\">Secs.</span></p></body></html>", None))
    # retranslateUi



###########################################################################################



""" 
##########################################

Main Running Code

##########################################
"""



class scoliosisUi(QWidget):
    def __init__(self):
        super(scoliosisUi, self).__init__()
        self.main_win = QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.main_win)
  

        # Initializations for keypads
        self.decimal_1 = False
        self.maxPrecision_1 = False
        self.ui.setMark.setHidden(True)
        self.ui.tooLargeLabel.setHidden(True)
        self.decimal_2 = False
        self.maxPrecision_2 = False
        self.ui.setMark_2.setHidden(True)
        self.ui.tooLargeLabel_2.setHidden(True)

        # Initializations for back end
        self.referenceUnit = -66090

        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(self.referenceUnit)
        self.hx.reset()
        self.hx.tare()
        
        self.dead_band_range = 1.0
        self.slow_mode_range = 5.0
        self.increase_tension = 22
        self.decrease_tension = 27
        self.slow_mode = 17
        self.output_pins = [self.increase_tension , self.decrease_tension , self.slow_mode]
        

        GPIO.setup(self.increase_tension , GPIO.OUT)
        GPIO.setup(self.decrease_tension , GPIO.OUT)
        GPIO.setup(self.slow_mode , GPIO.OUT)
        
        for i in self.output_pins: # Default the output_pins to low
            GPIO.output(i , GPIO.LOW)
            

        # Arrays for tension history
        self.timeArray = []
        self.timeArrayCounter = 0
        self.tensionArray = []


        ########### TEMPORARY FOR KIVY APP ###########
        # Initializing Socket
        global last_time
        last_time = 0
        self.receiver_ip = '192.168.117.95'
        self.receiver_port = 80

        self.sender_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

        self.sender_socket.connect((self.receiver_ip , self.receiver_port))

        self.ui.stackedWidget.setCurrentWidget(self.ui.setTension)

        self.ui.setTensionButton.clicked.connect(self.showSetTension)
        self.ui.setTimeDelayButton.clicked.connect(self.showSetTimeDelay)
        self.ui.setScheduleButton.clicked.connect(self.showSetSchedule)
        self.ui.tensionHistoryButton.clicked.connect(self.showTensionHistory)


        # Connect up and down buttons to setweight
        self.setWeight = 0.00
        self.ui.tensionUp.clicked.connect(self.doTensionUp)
        self.ui.tensionDown.clicked.connect(self.doTensionDown)
        self.ui.setTensionLCD.display(self.setWeight)

        # Set Time Delay Variable
        self.setTimeDelay = 0.00
        self.ui.timeDelayLCD.display(self.setTimeDelay)


        # MANUAL SET TENSION SCREEN #
        self.ui.keypad1.clicked.connect(lambda: self.manualSetTension(1))
        self.ui.keypad2.clicked.connect(lambda: self.manualSetTension(2))
        self.ui.keypad3.clicked.connect(lambda: self.manualSetTension(3))
        self.ui.keypad4.clicked.connect(lambda: self.manualSetTension(4))
        self.ui.keypad5.clicked.connect(lambda: self.manualSetTension(5))
        self.ui.keypad6.clicked.connect(lambda: self.manualSetTension(6))
        self.ui.keypad7.clicked.connect(lambda: self.manualSetTension(7))
        self.ui.keypad8.clicked.connect(lambda: self.manualSetTension(8))
        self.ui.keypad9.clicked.connect(lambda: self.manualSetTension(9))
        self.ui.keypad0.clicked.connect(lambda: self.manualSetTension(0))
        self.ui.keypadEnter.clicked.connect(lambda: self.manualSetTension(11))
        self.ui.keypadDecimal.clicked.connect(lambda: self.manualSetTension(12))
        self.ui.keypadClear.clicked.connect(lambda: self.manualSetTension(13))

        # MANUAL SET TIME DELAY SCREEN #
        self.ui.keypad1_2.clicked.connect(lambda: self.manualSetTimeDelay(1))
        self.ui.keypad2_2.clicked.connect(lambda: self.manualSetTimeDelay(2))
        self.ui.keypad3_2.clicked.connect(lambda: self.manualSetTimeDelay(3))
        self.ui.keypad4_2.clicked.connect(lambda: self.manualSetTimeDelay(4))
        self.ui.keypad5_2.clicked.connect(lambda: self.manualSetTimeDelay(5))
        self.ui.keypad6_2.clicked.connect(lambda: self.manualSetTimeDelay(6))
        self.ui.keypad7_2.clicked.connect(lambda: self.manualSetTimeDelay(7))
        self.ui.keypad8_2.clicked.connect(lambda: self.manualSetTimeDelay(8))
        self.ui.keypad9_2.clicked.connect(lambda: self.manualSetTimeDelay(9))
        self.ui.keypad0_2.clicked.connect(lambda: self.manualSetTimeDelay(0))
        self.ui.keypadEnter_2.clicked.connect(lambda: self.manualSetTimeDelay(11))
        self.ui.keypadDecimal_2.clicked.connect(lambda: self.manualSetTimeDelay(12))
        self.ui.keypadClear_2.clicked.connect(lambda: self.manualSetTimeDelay(13))
        

        # creating a timer object for graph test
        timer = QTimer(self)
        # adding action to timer
        # UPDATES EVERY 1 SECOND
        self.old_time = 0
        timer.timeout.connect(self.updateWeight)
        timer.timeout.connect(self.arrayAppend)
        timer.timeout.connect(self.controller)
        timer.timeout.connect(self.sendData)
        # update the timer every second
        timer.start(100)

    def sendData(self):
        global last_time
        if time.time() - last_time > 1:
            data = self.current_tension
            data_bytes = str(data).encode('utf-8')
            self.sender_socket.send(data_bytes)
            last_time = time.time()
        

    def updateWeight(self):
        new_time = time.time()
        #print(new_time - self.old_time)
        self.current_tension = self.get_tension()
        #print("Updating current weight to: " + str(self.current_tension))
        if math.floor(abs(self.current_tension)) <= 0.0:
            self.ui.currentWeightLCD.display(0.00)
        else:
            self.ui.currentWeightLCD.display(self.current_tension)
        self.old_time = new_time


    def arrayAppend(self):
        if len(self.timeArray) > 60:
            del self.timeArray[0]
            del self.tensionArray[0]
        self.timeArray.append(self.timeArrayCounter)
        self.tensionArray.append(abs(self.current_tension))
        self.timeArrayCounter += 1

        # TENSION HISTORY PLOT #
        self.plot(self.timeArray, self.tensionArray)



    ## Tension History Plotter Function ##
    def plot(self, time, tension):
        #print("Updating plot")
        self.ui.graphWidget.plot(time, tension)
        
        
    ## Set Tension Keypad Function ##
    def manualSetTension(self, pressed):
        if pressed == 11:
            if self.ui.manualSetTensionLCD.value() < 50:
                self.setWeight = self.ui.manualSetTensionLCD.value()
                self.ui.setTensionLCD.display(self.setWeight)
                self.ui.setMark.setHidden(False)
            else:
                self.ui.tooLargeLabel.setHidden(False)
            self.ui.manualSetTensionLCD.display(0)
            self.maxPrecision_1 = False
            self.decimal_1 = False
        elif pressed == 13:
            self.ui.manualSetTensionLCD.display(0)
            self.ui.setMark.setHidden(True)
            self.ui.tooLargeLabel.setHidden(True)
        elif pressed == 12:
            if self.decimal_1 == False:
                    mstLCDstring = (str(int(self.ui.manualSetTensionLCD.value()))+("."))
                    #print (mstLCDstring)
                    self.ui.manualSetTensionLCD.display(mstLCDstring)
                    self.decimal_1 = True
                    self.ui.setMark.setHidden(True)
                    self.ui.tooLargeLabel.setHidden(True)
        else:
            if (self.ui.manualSetTensionLCD.value() == 0) and (self.decimal_1 == False):
                self.ui.manualSetTensionLCD.display(pressed)
                self.ui.setMark.setHidden(True)
                self.ui.tooLargeLabel.setHidden(True)
            else:
                if self.decimal_1 == False:
                    mstLCDstring = (str(int(self.ui.manualSetTensionLCD.value())))+(str(pressed))
                    #print (mstLCDstring)
                    self.ui.manualSetTensionLCD.display(float(mstLCDstring))
                    self.ui.setMark.setHidden(True)
                    self.ui.tooLargeLabel.setHidden(True)
                else:
                    if self.maxPrecision_1 == False:
                        mstLCDstring = str(float(self.ui.manualSetTensionLCD.value()) + (0.1 * int(pressed)))
                        #print (mstLCDstring)
                        self.ui.manualSetTensionLCD.display(mstLCDstring)
                        self.maxPrecision_1 = True
                        self.ui.setMark.setHidden(True)
                        self.ui.tooLargeLabel.setHidden(True)



    ## Set Time Delay Keypad Function##
    def manualSetTimeDelay(self, pressed):
        if pressed == 11: # Enter
            if self.ui.manualSetTimeDelayLCD.value() < 600:
                self.setTimeDelay = self.ui.manualSetTimeDelayLCD.value()
                self.ui.timeDelayLCD.display(self.setTimeDelay)
                self.ui.setMark_2.setHidden(False)
            else:
                self.ui.tooLargeLabel_2.setHidden(False)
            self.ui.manualSetTimeDelayLCD.display(0)
            self.maxPrecision_2 = False
            self.decimal_2 = False
            
        elif pressed == 13: # Clear
            self.ui.manualSetTimeDelayLCD.display(0)
            self.ui.setMark_2.setHidden(True)
            self.ui.tooLargeLabel_2.setHidden(True)
            
        elif pressed == 12: # Decimal
            if self.decimal_2 == False:
                    mstLCDstring = (str(int(self.ui.manualSetTimeDelayLCD.value()))+("."))
                    #print (mstLCDstring)
                    self.ui.manualSetTimeDelayLCD.display(mstLCDstring)
                    self.decimal_2 = True
                    self.ui.setMark_2.setHidden(True)
                    self.ui.tooLargeLabel_2.setHidden(True)
                    
        else: # Any number
            #print("number pressed")
            if (self.ui.manualSetTimeDelayLCD.value() == 0) and (self.decimal_2 == False):
                #print("value is 0 and decimal is false")
                self.ui.manualSetTimeDelayLCD.display(pressed)
                #print("manual set time displayed")
                self.ui.setMark_2.setHidden(True)
                self.ui.tooLargeLabel_2.setHidden(True)
                #print("setmarks hidden")
            else:
                if self.decimal_2 == False:
                    mstLCDstring = (str(int(self.ui.manualSetTimeDelayLCD.value())))+(str(pressed))
                    #print (mstLCDstring)
                    self.ui.manualSetTimeDelayLCD.display(float(mstLCDstring))
                    self.ui.setMark_2.setHidden(True)
                    self.ui.tooLargeLabel_2.setHidden(True)
                else:
                    if self.maxPrecision_2 == False:
                        mstLCDstring = str(float(self.ui.manualSetTimeDelayLCD.value()) + (0.1 * int(pressed)))
                        #print (mstLCDstring)
                        self.ui.manualSetTimeDelayLCD.display(mstLCDstring)
                        self.maxPrecision_2 = True
                        self.ui.setMark_2.setHidden(True)
                        self.ui.tooLargeLabel_2.setHidden(True)
        

    def doTensionUp(self):
        #print("Weight +1.0")
        self.setWeight += 1.0
        #print(self.setWeight)
        self.ui.setTensionLCD.display(self.setWeight)
        

    def doTensionDown(self):
        #print("Weight -1.0")
        self.setWeight -= 1.0
        #print(self.setWeight)
        self.ui.setTensionLCD.display(self.setWeight)


		
    def show(self):
        self.main_win.show()

    def showSetTension(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setTension)

    def showSetTimeDelay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setTimeDelay)

    def showSetSchedule(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setSchedule)

    def showTensionHistory(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.tensionHistory)




    def get_tension(self):
            val = self.hx.get_weight(5)

            #self.hx.power_down()
            #self.hx.power_up()
            #time.sleep(0.1)
            return val


    # Controller is able to compare the current tension to the set point to see if it's within the dead band and within the slow mode range
    def controller(self):
        #print("Updating controller")

        # If the current tension is below the dead band the tension is increased
        if self.setWeight - self.dead_band_range > self.current_tension:

            # If the current tension is below the slow mode range the speed is fast
            if self.setWeight - self.slow_mode_range > self.current_tension:
                GPIO.output(self.slow_mode , GPIO.HIGH)
                speed = "Fast"
            else:
                GPIO.output(self.slow_mode , GPIO.LOW)
                speed = "Slow"
            GPIO.output(self.increase_tension , GPIO.HIGH)
            GPIO.output(self.decrease_tension , GPIO.LOW)
            turning_direction = "Increasing Tension"
        
        # If the current tension is above the dead band the tension is decreased
        elif self.setWeight + self.dead_band_range < self.current_tension:

            # If the current tension is above the slow mode range the speed is fast
            if self.setWeight + self.slow_mode_range < self.current_tension:
                GPIO.output(self.slow_mode , GPIO.HIGH)
                speed = "Fast"
            else:
                GPIO.output(self.slow_mode , GPIO.LOW)
                speed = "Slow"
            GPIO.output(self.decrease_tension , GPIO.HIGH)
            GPIO.output(self.increase_tension , GPIO.LOW)
            turning_direction = "Decreasing Tension"
        
        else:
            speed = ""
            turning_direction = "Stopped"
            for i in self.output_pins:
                GPIO.output(i , GPIO.LOW)
        
        return turning_direction , speed





if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application style to Fusion
    app.setStyle('Fusion')

    # Set a dark palette for the application
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    main_win = scoliosisUi()
    main_win.show()
    
    try:
        sys.exit(app.exec_())
    except:
        #print("Exiting")
        pass


