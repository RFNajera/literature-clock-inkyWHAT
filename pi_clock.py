#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 17:16:50 2018

@author: tafj0
"""
import sys
#from PyQt5.QtGui import QIcon
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget,QPushButton, QTextEdit, QVBoxLayout, QApplication,QGridLayout,QStackedWidget)

import json
import random
import logging
from datetime import datetime
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

myStyleSheet="""QWidget{ background-color: black; border-radius: 0px; color: gray;}
QPushButton{ border: 1px solid gray; color: gray; border-radius: 5px;background-color: rgb(20, 20, 20);padding-top: 5px;padding-bottom: 5px}
QLabel{ border: 1px solid gray; color: gray;}
QPushButton:checked { background-color: cyan;}
QPushButton:pressed{ background-color: gray;}
QGroupBox{ border: 1px solid grey; padding-top: 5px}
QGroupBox::title {    subcontrol-origin: margin; subcontrol-position: top center; 
   padding: 0 15px;
color: gray;  }
QWidget#tempWidget{  background-color: black ; color: gray;}
QLabel#tempLabel{ background-color: black ; color: gray;}
QLabel#timeLabel,QLabel#authorLabel{color: rgb(230, 230, 230)}
QWidget#optionsWidget{background-color:red; border:3px solid rgb(0, 255, 0);}
"""

class MainWindow():
    def __init__(self):
         self.form=Form()
         self.form.quitButton.clicked.connect(lambda:self.close())
         self.form.clock.quitWidget.button.clicked.connect(lambda:self.close())
         self.form.show()
         log.info("Set up done")
    def close(self):
         log.debug("Close event")
         self.form.close()
         
class quitW(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self)
        vlayout=QVBoxLayout()
        self.button=QtWidgets.QPushButton('Quit?')
        self.font = QtGui.QFont()
        self.font.setFamily("Times")
        self.font.setPointSize(40)
        self.font.setBold(False)
        self.button.setFont(self.font)
        vlayout.addWidget(self.button)
        mainLayout = QGridLayout()
        mainLayout.addLayout(vlayout, 0, 1)
        self.setLayout(mainLayout)
        


class clockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        
        self.default_quote_font_size=40
        self.default_author_font_size=37
        self.min_font_size=10
        
        QtWidgets.QWidget.__init__(self)
        log.debug("new temp/press created")
        self.stackIndex=0
        self.setObjectName("clockWidget")
        self.setStyleSheet(myStyleSheet)
        vlayout=QVBoxLayout()
        self.font = QtGui.QFont()
        self.font.setFamily("Times")
        self.font.setPointSize(self.default_quote_font_size)
        self.font.setBold(False)
        self.font.setWeight(50)
        #self.timeLabel= QtWidgets.QLabel()
        self.timeLabel=QtWidgets.QTextEdit()
        self.timeLabel.setFixedSize(750, 400)
        self.timeLabel.setFont(self.font)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setText("Some great quote goes here!")
        self.timeLabel.setReadOnly(True)
        self.timeLabel.mousePressEvent=self.toggleStack
        self.stack=QStackedWidget()
        self.stack.addWidget(self.timeLabel)
        self.quitWidget=quitW()
        self.stack.addWidget(self.quitWidget)
        self.stack.setCurrentIndex(self.stackIndex)
        
        vlayout.addWidget(self.stack)
        self.authLabel=QtWidgets.QTextEdit()
        self.authLabel.setFixedSize(681, 81)
        self.fonta = QtGui.QFont()
        self.fonta.setFamily("Times")
        self.fonta.setPointSize(self.default_author_font_size)
        self.authLabel.setFont(self.fonta)
        self.authLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.authLabel.setObjectName("authorLabel")
        self.authLabel.setText("Title, Author")
        self.authLabel.setAlignment(QtCore.Qt.AlignRight)
        self.authLabel.setReadOnly(True)
        vlayout.addWidget(self.authLabel)
        mainLayout = QGridLayout()
        mainLayout.addLayout(vlayout, 0, 1)
        
        self.setLayout(mainLayout)
        self.loadData()
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.currentMin=61  #to ensure it triggers time diff check
        self.Time()
        
        self.timer.start(3000)
        
    def closeEvent(self,event):
         log.debug("Form close event")
         self.timer.stop()
         event.accept()
         
    @QtCore.pyqtSlot()
    def toggleStack(self,event):
        print('toggle')
        self.stack.setCurrentIndex(1)
        QtCore.QTimer.singleShot(3000,self.toggleStackOff)
    
    def toggleStackOff(self):    
        self.stack.setCurrentIndex(0)
    
    def Time(self):
        #self.setTime('12:01')
        if datetime.now().minute != self.currentMin:
            self.currentMin=datetime.now().minute
            self.setTime(datetime.now().strftime('%H:%M'))
            log.debug('Update min {}'.format(self.currentMin))
    def loadData(self):
        self.quote_data=dict()
        
        for hours in range(24):
            for mins in range(60):
                time="{:02d}:{:02d}".format(hours,mins)
                filename="docs/times/{:s}.json".format(time)
                try:
                    with open(filename,'r') as jfile:
                        self.quote_data[time]=json.load(jfile)
                except Exception:
                    log.error('Cannot load {}'.format(filename))
    def _getQuote(self,time_str):
        return random.choice(self.quote_data[time_str])
        
    def setTime(self,time_str):
        #set default font sizes - might get reduced later
        self.font.setPointSize(self.default_quote_font_size)
        self.timeLabel.setFont(self.font)
        self.fonta.setPointSize(self.default_author_font_size)
        self.authLabel.setFont(self.fonta)
        
        qt=self._getQuote(time_str)
        qstr="{:s} <b><em><font color =\"white\">{:s}</font></em></b> {:s}".format(qt['quote_first'],qt['quote_time_case'],qt['quote_last'])
        log.info(qstr)
        #self.timeLabel.setText(qstr)
        self.timeLabel.setHtml(qstr)
        authStr="- {:s}, <em><font color =\"white\">{:s}</font></em>".format(qt['title'],qt['author'])
        self.authLabel.setHtml(authStr)
        self.authLabel.setAlignment(QtCore.Qt.AlignRight)
        
        fs=self.default_quote_font_size
       
        while True:
            h=self.timeLabel.document().size().height()
            if h > self.timeLabel.size().height():
                fs=fs-1
                if fs <= self.min_font_size:
                    log.debug('Min font size reached')
                    break
                self.font.setPointSize(fs)
                self.timeLabel.setFont(self.font)
                #print(fs)
            else:
                break
        fs=self.default_author_font_size
        while True:
            h=self.authLabel.document().size().height()
            if h > self.authLabel.size().height():
                fs=fs-1
                if fs <= self.min_font_size:
                    log.debug('Min font size reached')
                    break
                self.fonta.setPointSize(fs)
                self.timeLabel.setFont(self.fonta)
                
            else:
                break
            
                
         
class Form(QtWidgets.QWidget):
    """ creates the main GUI form"""
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
       #self.showFullScreen()
        self.setObjectName("MainWindow")
        self.resize(800, 480)
        self.setMaximumSize(QtCore.QSize(800, 480))
        self.setStyleSheet(myStyleSheet)
        vlayout=QVBoxLayout()
        self.quitButton = QtWidgets.QPushButton()
        self.quitButton.setFixedSize(20,20)
        self.quitButton.setText("Quit")
        #vlayout.addWidget(self.quitButton)
        
        self.clock=clockWidget()
        vlayout.addWidget(self.clock)
        
        mainLayout = QGridLayout()
        mainLayout.addLayout(vlayout, 0, 1)
        self.setLayout(mainLayout)


if __name__ == "__main__":
     app=0
     app = QApplication(sys.argv)
     log.info('Creating main window')
         
     form = MainWindow()
     
     sys.exit(app.exec_())