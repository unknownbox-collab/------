import sqlite3,sys,os,json
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtCore

FORM_LOGIN      = uic.loadUiType(os.path.join('.','assets','ui','login.ui'))[0]
FORM_CREDIT     = uic.loadUiType(os.path.join('.','assets','ui','credit.ui'))[0]
FORM_HOW_TO_USE = uic.loadUiType(os.path.join('.','assets','ui','howToUse.ui'))[0]
FORM_IN_VOTE    = uic.loadUiType(os.path.join('.','assets','ui','inVote.ui'))[0]
FORM_JOIN_VOTE       = uic.loadUiType(os.path.join('.','assets','ui','join.ui'))[0]
FORM_MAIN       = uic.loadUiType(os.path.join('.','assets','ui','main.ui'))[0]
FORM_VOTE       = uic.loadUiType(os.path.join('.','assets','ui','vote.ui'))[0]
FORM_MAKE_VOTE_OPTION  = uic.loadUiType(os.path.join('.','assets','ui','makeVote.ui'))[0]
FORM_SUBJECT_VOTE  = uic.loadUiType(os.path.join('.','assets','ui','vote_set_subject.ui'))[0]

userId = ''

class LoginWindow(QMainWindow, QWidget, FORM_LOGIN):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.howToUseBtn.clicked.connect(self.openHowToUse)
        self.creditBtn.clicked.connect(self.openCredit)
        self.loginBtn.clicked.connect(self.login)
        self.numberInput.returnPressed.connect(self.login)
    
    def openHowToUse(self):
        self.howToUse = HowToUseWindow()
        self.howToUse.show()
        self.close()
    
    def openCredit(self):
        self.credit = CreditWindow()
        self.credit.show()
        self.close()

    def login(self):
        global userId
        userId = self.numberInput.text()
        self.main = MainWindow()
        self.main.show()
        self.close()

class HowToUseWindow(QMainWindow, QWidget, FORM_HOW_TO_USE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
    
    def goBack(self):
        self.LoginWindow = LoginWindow()
        self.LoginWindow.show()
        self.close()

class CreditWindow(QMainWindow, QWidget, FORM_CREDIT):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
    
    def goBack(self):
        self.LoginWindow = LoginWindow()
        self.LoginWindow.show()
        self.close()

class MainWindow(QMainWindow, QWidget, FORM_MAIN):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.logoutBtn.clicked.connect(self.logout)
        self.msgBtn.clicked.connect(self.openMessenger)
        self.shuffleBtn.clicked.connect(self.openShuffle)
        self.voteBtn.clicked.connect(self.openVote)
        self.welcomeLabel.setText(f'{userId}님 반갑습니다!')
    
    def openMessenger(self):
        self.messenger = MessengerWindow()
        self.messenger.show()
        self.close()
    
    def openShuffle(self):
        self.shuffle = ShuffleWindow()
        self.shuffle.show()
        self.close()
    
    def openVote(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()
    
    def logout(self):
        global userId
        userId = ''
        self.LoginWindow = LoginWindow()
        self.LoginWindow.show()
        self.close()

class VoteWindow(QMainWindow, QWidget, FORM_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.makeBtn.clicked.connect(self.openMakeVote)
        self.joinBtn.clicked.connect(self.openJoinVote)
        self.achieveBtn.clicked.connect(self.openAchieve)
    
    def goBack(self):
        self.main = MainWindow()
        self.main.show()
        self.close()
    
    def openMakeVote(self):
        self.makeVote = SubjectVoteWindow()
        self.makeVote.show()
        self.close()
    
    def openJoinVote(self):
        self.joinVote = JoinVoteWindow()
        self.joinVote.show()
        self.close()
    
    def openAchieve(self):
        self.achieve = AchieveWindow()
        self.achieve.show()
        self.close()

class SubjectVoteWindow(QMainWindow, QWidget, FORM_SUBJECT_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.subjectInput.returnPressed.connect(self.addSubject)
    
    def openMakeVote(self):
        self.makeVote = MakeVoteOptionWindow()
        self.makeVote.show()
        self.close()
    
    def goBack(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()
    
    def addSubject(self):
        if self.subjectInput.text() != '':
            self.subjectList.addItem(self.subjectInput.text())
            self.subjectInput.setText('')

class MakeVoteOptionWindow(QMainWindow, QWidget, FORM_MAKE_VOTE_OPTION):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
    
    def goBack(self):
        self.subjectVote = SubjectVoteWindow()
        self.subjectVote.show()
        self.close()

class JoinVoteWindow(QMainWindow, QWidget, FORM_JOIN_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
    
    def goBack(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())