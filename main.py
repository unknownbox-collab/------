import sys,os,json,firebase_admin,random,time
from assets.dataBaseModule import *

from firebase_admin import db
from firebase_admin import credentials
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtCore

db_url = 'https://ham2021-main-project-default-rtdb.asia-southeast1.firebasedatabase.app/'
cred = credentials.Certificate(os.path.join('.','assets','key.json'))
default_app = firebase_admin.initialize_app(cred, {'databaseURL':db_url})

userId = ''
voteSubject = []
voteOptions = []
voteCount = []
optionPage = 0
voteCode = ''
fireBaseData = {}
voteAchieveDB = DataBase('vote', result = 'text', date = 'text')

class GetFireBaseInfo(QThread): #getFBI
    update = pyqtSignal(bool)
    def __init__(self, interest):
        QThread.__init__(self) 
        self.interest = interest
        self.working = True
 
    def run(self):
        global fireBaseData
        ref = db.reference(self.interest)
        while self.working:
            info = ref.get()
            if info != fireBaseData:
                fireBaseData = ref.get()
                self.update.emit(True)
            time.sleep(1)


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
        self.addBtn.clicked.connect(self.addSubject)
        self.editBtn.clicked.connect(self.editSubject)
        self.removeBtn.clicked.connect(self.removeSubject)
        self.nextBtn.clicked.connect(self.next)

        self.subjectInput.returnPressed.connect(self.addSubject)
        self.subjectList.clicked.connect(self.showTools)

        self.editBtn.hide()
        self.removeBtn.hide()
        self.subjectList.addItems(voteSubject)
        if len(voteSubject) == 0:
            self.nextBtn.hide()
    
    def goBack(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()
    
    def addSubject(self):
        if self.subjectInput.text() != '':
            if self.subjectList.currentRow() != -1:
                self.subjectList.insertItem(self.subjectList.currentRow(), self.subjectInput.text())
            else:
                self.subjectList.addItem(self.subjectInput.text())
            self.nextBtn.show()
            self.subjectInput.setText('')
    
    def editSubject(self):
        if self.subjectInput.text() != '':
            self.subjectList.currentItem().setText(self.subjectInput.text())
            self.subjectInput.setText('')
    
    def removeSubject(self):
        self.subjectList.takeItem(self.subjectList.currentRow())
        self.hideTools()
        self.subjectList.setCurrentRow(-1)
        if self.subjectList.count() == 0 :
            self.nextBtn.hide()

    def showTools(self):
        self.editBtn.show()
        self.removeBtn.show()
    
    def hideTools(self):
        self.editBtn.hide()
        self.removeBtn.hide()
    
    def next(self):
        global voteSubject
        global voteOptions
        voteSubject = [self.subjectList.item(i).text() for i in range(self.subjectList.count())]
        voteOptions = [[] for i in range(self.subjectList.count())]
        self.voteOptionWindow = MakeVoteOptionWindow()
        self.voteOptionWindow.show()
        self.close()

class MakeVoteOptionWindow(QMainWindow, QWidget, FORM_MAKE_VOTE_OPTION):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.addBtn.clicked.connect(self.addOption)
        self.editBtn.clicked.connect(self.editOption)
        self.removeBtn.clicked.connect(self.removeOption)
        self.nextBtn.clicked.connect(self.nextPage)
        self.subjectNameLabel.setText(f'주제 : {voteSubject[optionPage]}')
        self.optionList.setCurrentRow(-1)
        self.hideTools()

        self.optionInput.returnPressed.connect(self.addOption)
        self.optionList.clicked.connect(self.showTools)

        self.optionList.addItems(voteOptions[optionPage])
        if len(voteOptions[optionPage]) == 0:
            self.nextBtn.hide()
        else:
            self.nextBtn.show()
    
    def addOption(self):
        if self.optionInput.text() != '':
            if self.optionList.currentRow() != -1:
                self.optionList.insertItem(self.optionList.currentRow(), self.optionInput.text())
            else:
                self.optionList.addItem(self.optionInput.text())
            self.nextBtn.show()
            self.optionInput.setText('')
    
    def editOption(self):
        if self.optionInput.text() != '':
            self.optionList.currentItem().setText(self.optionInput.text())
            self.optionInput.setText('')
    
    def removeOption(self):
        self.optionList.takeItem(self.optionList.currentRow())
        self.hideTools()
        self.optionList.setCurrentRow(-1)
        if self.optionList.count() == 0 :
            self.nextBtn.hide()
    
    def showTools(self):
        self.editBtn.show()
        self.removeBtn.show()
    
    def hideTools(self):
        self.editBtn.hide()
        self.removeBtn.hide()
    
    def nextPage(self):
        global optionPage
        global voteOptions
        global voteCode
        global fireBaseData

        voteOptions[optionPage] = [self.optionList.item(i).text() for i in range(self.optionList.count())]
        if optionPage >= len(voteSubject) - 1:
            code = self.makeCode()
            ref = db.reference("vote")
            ref.update({code:[[0 for j in range(len(voteOptions[i]))] for i in range(len(voteSubject))]})
            voteCode = str(code)
            fireBaseData = ref.get()

            self.voteWait = VoteWaitWindow()
            self.voteWait.show()
            self.close()
        else:
            optionPage += 1
            self.optionList.clear()
            self.subjectNameLabel.setText(f'주제 : {voteSubject[optionPage]}')
            self.optionList.addItems(voteOptions[optionPage])
            if len(voteOptions[optionPage]) == 0:
                self.nextBtn.hide()
            else:
                self.nextBtn.show()
    
    def goBack(self):
        global optionPage
        if optionPage == 0:
            self.goBackAlert = GoBackAlertWindow()
            self.goBackAlert.show()
            self.close()
        else:
            optionPage -= 1
            self.optionList.clear()
            self.subjectNameLabel.setText(f'주제 : {voteSubject[optionPage]}')
            self.optionList.addItems(voteOptions[optionPage])
            if len(voteOptions[optionPage]) == 0:
                self.nextBtn.hide()
            else:
                self.nextBtn.show()
    
    def makeCode(self):
        ref = db.reference('vote')
        code = random.randint(0,9999)
        if ref.get() is not None:
            while code in ref.get().keys():
                code = random.randint(0,9999)
        return code

class GoBackAlertWindow(QMainWindow, QWidget, FORM_GO_BACK_ALERT):
    def __init__(self,option = 0):
        super().__init__()
        self.option = option
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        if self.option == 0:
            self.goBackBtn.clicked.connect(self.goBack)
            self.cancelBtn.clicked.connect(self.cancel)
        elif self.option == 1:
            self.voteLabel.setText('정말로 돌아가시겠습니까?\n(현재 진행중인 투표는 중단됩니다.)')
            self.goBackBtn.setText('돌아가기')
            self.goBackBtn.clicked.connect(self.goPre)
            self.cancelBtn.clicked.connect(self.cancelInVote)
        elif self.option == 2:
            self.voteLabel.setText('정말로 투표를 종료하시겠습니까?')
            self.goBackBtn.setText('투표 종료')
            self.goBackBtn.clicked.connect(self.goEnd)
            self.cancelBtn.clicked.connect(self.cancelInVote)
    
    def goBack(self):
        self.subjectVote = SubjectVoteWindow()
        self.subjectVote.show()
        self.close()
    
    def goEnd(self):
        global voteCount
        ref = db.reference('vote')
        items = ref.get()
        voteCount = items[voteCode]
        if len(items.keys()) != 1:
            del items[voteCode]
            ref.set(items)
        else:
            ref = db.reference('vote')
            ref.set({})
        self.endVoteWindow = EndVoteWindow()
        self.endVoteWindow.show()
        self.close()
    
    def cancel(self):
        self.vote = MakeVoteOptionWindow()
        self.vote.show()
        self.close()
    
    def cancelInVote(self):
        self.thisWindow = VoteWaitWindow()
        self.thisWindow.show()
        self.close()
    
    def goPre(self):
        ref = db.reference('vote')
        items = ref.get()
        if len(items.keys()) != 1:
            del items[voteCode]
            ref.set(items)
        else:
            ref = db.reference('vote')
            ref.set({})
        self.MakeVoteOptionWindow = MakeVoteOptionWindow()
        self.MakeVoteOptionWindow.show()
        self.close()

class VoteWaitWindow(QMainWindow, QWidget, FORM_WAIT_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.subjectComboBox.addItems(voteSubject)
        self.endVoteBtn.clicked.connect(self.endVote)
        self.joinCodeLabel.setText(f'참여 코드 : {voteCode}')
        self.subjectComboBox.currentIndexChanged.connect(self.updateOptionList)

        self.th = GetFireBaseInfo('vote')
        self.th.update.connect(self.updateData)
        self.th.start()
        idx = self.subjectComboBox.currentIndex()
        formattedOptions = [f'{voteOptions[idx][i]} : {fireBaseData[voteCode][idx][i]}표' for i in range(len(voteOptions[idx]))]
        self.optionList.addItems(formattedOptions)
    
    def goBack(self):
        self.th.working = False
        self.goBackAlert = GoBackAlertWindow(1)
        self.goBackAlert.show()
        self.close()
    
    def endVote(self):
        self.th.working = False
        self.goBackAlert = GoBackAlertWindow(2)
        self.goBackAlert.show()
        self.close()
    
    def updateOptionList(self):
        self.optionList.clear()
        idx = self.subjectComboBox.currentIndex()
        formattedOptions = [f'{voteOptions[idx][i]} : {fireBaseData[voteCode][idx][i]}표' for i in range(len(voteOptions[idx]))]
        self.optionList.addItems(formattedOptions)

    @pyqtSlot(bool)
    def updateData(self):
        idx = self.subjectComboBox.currentIndex()
        options = voteOptions[idx]
        for i in range(len(options)):
            self.optionList.item(i).setText(f'{options[i]} : {fireBaseData[voteCode][idx][i]}표')

class EndVoteWindow(QMainWindow, QWidget, FORM_END_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.endVoteBtn.clicked.connect(self.ok)
        result = [[(voteOptions[subject][i],voteCount[subject][i]) for i in range(len(voteCount[subject]))] for subject in range(len(voteSubject))]
        rank = [sorted(result[i], key=lambda x: x[1],reverse=True) for i in range(len(voteSubject))]
        rank = [voteSubject[item]+" : "+', '.join([f'{rank[item][i][0]}({rank[item][i][1]}표)' for i in range(len(rank[item]))]) for item in range(len(rank))]
        print(rank)
        self.resultList.addItems(rank)
    
    def ok(self):
        self.vote = VoteWindow()
        self.vote.show()
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