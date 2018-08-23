#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 17:16:50 2018

@author: tafj0
"""
import sys
from PyQt4.QtCore import pyqtSlot,QTimer,QSize,Qt
from PyQt4.QtGui import (QWidget,QPushButton, QTextEdit, QVBoxLayout, QApplication,QGridLayout,QStackedWidget)
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QFont
import json
import random
import logging
from datetime import datetime
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

myStyleSheet="""QWidget{ background-color: black; border-radius: 0px; color: gray;}
QPushButton{ border: 1px solid gray; color: gray; border-radius: 5px;background-color: rgb(20, 20, 20);padding-top: 5px;padding-bottom: 5px}
QTextEdit{background-color: black;}
QPushButton:checked { background-color: cyan;}
QPushButton:pressed{ background-color: gray;}
"""

class MainWindow():
    def __init__(self,argv):
         if len(argv)>1:
             fixedTime=argv[1]
             log.info('Fixing time to {}'.format(fixedTime))
         else:
             fixedTime=''
         self.form=Form(fixedTime=fixedTime)
         self.form.quitButton.clicked.connect(lambda:self.close())
         self.form.clock.quitWidget.button.clicked.connect(lambda:self.close())
         QApplication.setOverrideCursor(Qt.BlankCursor)
         self.form.show()
         log.info("Set up done")
    def close(self):
         log.debug("Close event")
         self.form.close()
         
class quitW(QWidget):
    def __init__(self, parent=None):
        QPushButton.__init__(self)
        vlayout=QVBoxLayout()
        self.button=QPushButton('Quit?')
        self.font = QFont()
        self.font.setFamily("Times")
        self.font.setPointSize(40)
        self.font.setBold(False)
        self.button.setFont(self.font)
        vlayout.addWidget(self.button)
        mainLayout = QGridLayout()
        mainLayout.addLayout(vlayout, 0, 1)
        self.setLayout(mainLayout)
        


class clockWidget(QWidget):
    def __init__(self, parent=None,fixedTime=''):
        self.fixedTime=fixedTime
        self.default_quote_font_size=40
        self.default_author_font_size=37
        self.min_font_size=10
        
        QWidget.__init__(self)
        log.debug("new temp/press created")
        self.stackIndex=0
        self.setObjectName("clockWidget")
        self.setStyleSheet(myStyleSheet)
        vlayout=QVBoxLayout()
        self.font = QFont()
        self.font.setFamily("Times")
        self.font.setPointSize(self.default_quote_font_size)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.timeLabel=QTextEdit()
        self.timeLabel.setFixedSize(750,340)# 400)
        self.timeLabel.setFont(self.font)
#        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setText("Some great quote goes here!")
        self.timeLabel.setReadOnly(True)
        self.timeLabel.mousePressEvent=self.toggleStack
        self.timeLabel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.stack=QStackedWidget()
        self.stack.addWidget(self.timeLabel)
        self.quitWidget=quitW()
        self.stack.addWidget(self.quitWidget)
        self.stack.setCurrentIndex(self.stackIndex)
        
        vlayout.addWidget(self.stack)
        self.authLabel=QTextEdit()
        self.authLabel.setFixedSize(680, 81)
        self.fonta = QFont()
        self.fonta.setFamily("Times")
        self.fonta.setPointSize(self.default_author_font_size)
        self.authLabel.setFont(self.fonta)
#        self.authLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.authLabel.setObjectName("authorLabel")
        self.authLabel.setText("Title, Author")
        self.authLabel.setAlignment(Qt.AlignRight)
        self.authLabel.setReadOnly(True)
        self.authLabel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        vlayout.addWidget(self.authLabel)
        mainLayout = QGridLayout()
        mainLayout.addLayout(vlayout, 0, 1)
        
        self.setLayout(mainLayout)
        self.loadData()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.currentMin=61  #to ensure it triggers time diff check
        self.Time()
        
        self.timer.start(3000)
        
    def closeEvent(self,event):
         log.debug("Form close event")
         self.timer.stop()
         event.accept()
         
    @pyqtSlot()
    def toggleStack(self,event):
        #print('toggle')
        self.stack.setCurrentIndex(1)
        QTimer.singleShot(3000,self.toggleStackOff)
    
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
  
        if not self.fixedTime:
            qt=self._getQuote(time_str)
        else:
            qt=self._getQuote(self.fixedTime)
            log.debug('fixed time')
        
        qstr=u"{:s} <b><em><font color =\"white\">{:s}</font></em></b> {:s}".format(qt['quote_first'],qt['quote_time_case'],qt['quote_last'])
        log.info(qstr)
        #self.timeLabel.setText(qstr)
        self.timeLabel.setHtml(qstr)
        authStr=u"- {:s}, <em><font color =\"white\">{:s}</font></em>".format(qt['title'],qt['author'])
        self.authLabel.setHtml(authStr)
        self.authLabel.setAlignment(Qt.AlignRight)
        log.info(authStr)
        
        #met=QFontMetrics(self.font)
        #bb=met.boundingRect(self.timeLabel.geometry(),Qt.TextWordWrap,qstr)
        #print(bb.height())
        
        #met=QFontMetrics(self.fonta)
        #bb=met.boundingRect(self.authLabel.geometry(),Qt.TextWordWrap,authStr)
        #print(bb)
        fs=self.default_quote_font_size
        log.debug('quote')
        while True:
            h=self.timeLabel.document().size().height()
            met=QFontMetrics(self.font)
            bb=met.boundingRect(self.timeLabel.geometry(),Qt.TextWordWrap,qstr)
            h=bb.height()
        
            #print('h {} fs {} labelsize {}'.format(h,fs,self.timeLabel.size().height()))
            if h > self.timeLabel.size().height():
                fs=fs-1
                #print('h {} fs {} labelsize {}'.format(h,fs,self.timeLabel.size().height()))
                if fs <= self.min_font_size:
                    log.debug('Min font size reached')
                    break
                self.font.setPointSize(fs)
                self.timeLabel.setFont(self.font)
                #print(fs)
            else:
                break
        log.debug('author')
        fs=self.default_author_font_size
        while True:
            h=self.authLabel.document().size().height()
            met=QFontMetrics(self.fonta)
            bb=met.boundingRect(self.authLabel.geometry(),Qt.TextWordWrap,authStr)
            h=bb.height()
        
            
            #print('h {} fs {} labelsize {}'.format(h,fs,self.authLabel.size().height()))
            
            if h > self.authLabel.size().height():
                
                fs=fs-1
                #print('h {} fs {} labelsize {}'.format(h,fs,self.authLabel.size().height()))
                if fs <= self.min_font_size:
                    log.debug('Min font size reached')
                    break
                self.fonta.setPointSize(fs)
                self.authLabel.setFont(self.fonta)
                #self.authLabel.setFontPointSize(10)
            else:   #make the font a bit smaller still if possible
                if fs>self.min_font_size+4:
                    fs=fs-4
                    self.fonta.setPointSize(fs)            
                    self.authLabel.setFont(self.fonta) 
                break
         
class Form(QWidget):
    """ creates the main GUI form"""
    def __init__(self, parent=None,fixedTime=''):
        super(Form, self).__init__(parent)
        self.showFullScreen()
        self.setObjectName("MainWindow")
        self.resize(800, 480)
        self.setMaximumSize(QSize(800, 480))
        self.setStyleSheet(myStyleSheet)
        vlayout=QVBoxLayout()
        self.quitButton = QPushButton()
        self.quitButton.setFixedSize(20,20)
        self.quitButton.setText("Quit")
        #vlayout.addWidget(self.quitButton)
        
        self.clock=clockWidget(fixedTime=fixedTime)
        vlayout.addWidget(self.clock)
        
        mainLayout = QGridLayout()
        mainLayout.addLayout(vlayout, 0, 1)
        self.setLayout(mainLayout)


if __name__ == "__main__":
     app=0
     app = QApplication(sys.argv)
     log.info('Creating main window')
         
     form = MainWindow(sys.argv)
     
     sys.exit(app.exec_())
