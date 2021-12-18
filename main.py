import sys,os,firebase_admin,threading,time,hashlib

from firebase_admin.db import reference
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from firebase_admin import credentials

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

from assets.dataBaseModule import *
from assets.vote import *
from assets.shuffle import *
try:
    msgArchiveDB = DataBase('message', userId = 'text', by = 'text', content = 'text', new = 'BOOLEAN', date = 'text')
    ID = 0
    USER_ID = 1
    BY = 2
    CONTENT = 3
    NEW = 4
    DATE = 5

    msgArchiveData = None

    class GetMessage(QThread):
        update = pyqtSignal(bool)
        def __init__(self):
            QThread.__init__(self)
            self.working = True
            self.daemon = True

        def run(self):
            while self.working:
                m = hashlib.sha256()
                m.update(userId.encode('utf-8'))
                userHash = m.hexdigest()
                ref = db.reference(f'message/{userHash}')
                infoList = ref.get()
                archive = msgArchiveDB.select(f'userId = "{userId}"')
                now = datetime.now()
                now = str(now.strftime("%Y.%m.%d/%H:%M"))
                popped = 0
                if infoList is not None:
                    for i in range(len(infoList)):
                        info = infoList[i-popped]
                        if not (userId,info[0],str([info[1],info[2],info[3]]),True,info[4]) in archive:
                            ref = db.reference(f'message/{userHash}/{i-popped}')
                            ref.delete()
                            msgArchiveDB.add((userId,info[0],str([info[1],info[2],info[3]]),True,info[4]))
                            popped += 1
                            self.update.emit(True)
                time.sleep(0.5)

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
            settingShuffleModule(userId)
            settingVoteModule(userId)
            loginId = open(os.path.join('.','assets','login.txt'),'w')
            loginId.write(userId)
            loginId.close()
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
            self.newMessage.hide()
            archive = msgArchiveDB.select(f"userId = '{userId}' AND new = True")
            if len(archive) != 0 :
                self.newMessage.show()
            msgGetter.start()
            msgGetter.update.connect(self.newMessage.show)

        def openMessenger(self):
            if teacherPermission:
                self.messenger = MessengerMenuWindow()
            else:
                self.messenger = ReceiveMessengerWindow()
            self.messenger.show()
            self.close()

        def openShuffle(self):
            self.shuffle = ShufflePrepareWindow()
            self.shuffle.show()
            self.close()

        def openVote(self):
            self.vote = VoteWindow()
            self.vote.show()
            self.close()

        def logout(self):
            global userId,teacherPermission
            userId = ''
            loginId = open(os.path.join('.','assets','login.txt'),'w')
            loginId.write('')
            loginId.close()
            teacherPermission = False
            self.LoginWindow = LoginWindow()
            self.LoginWindow.show()
            self.close()
    
################################################################################################
    class ReceiveMessengerWindow(QMainWindow, QWidget, FORM_RECEIVE_MESSAGE):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()

        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            self.receiveList.itemDoubleClicked.connect(self.view)
            self.archive = msgArchiveDB.select(f'userId = "{userId}"')[::-1]
            msgGetter.update.connect(self.checkNew)
            if len(self.archive):
                for history in self.archive:
                    when, where, msg = eval(history[CONTENT])
                    self.receiveList.addItem(f'{history[BY]}({history[DATE]}) : {msg[:10] + ("..." if len(msg) > 10 else "")}')

        def view(self):
            self.vote = ViewVoteArchiveWindow(self.archive[self.receiveList.currentRow()])
            self.vote.show()
            self.close()

        def removeArchive(self):
            deletedItemId = self.archive[self.receiveList.currentRow()][ID]
            msgArchiveDB.excute(f'''
                DELETE FROM 'vote' WHERE id = {deletedItemId}
            ''')
            self.receiveList.takeItem(self.receiveList.currentRow())
            self.archive = msgArchiveDB.select(f'userId = "{userId}"')
            self.receiveList.setCurrentRow(-1)
            self.removeBtn.hide()
            self.viewBtn.hide()

        def goBack(self):
            if not teacherPermission:
                self.pre = MainWindow()
                self.pre.show()
            else:
                self.pre = MessengerMenuWindow()
                self.pre.show()
            self.close()
        
        @pyqtSlot(bool)
        def checkNew(self):
            self.archive = msgArchiveDB.select(f'userId = "{userId}" AND new = True')
            if len(self.archive):
                for history in self.archive:
                    when, where, msg = eval(history[CONTENT])
                    self.receiveList.addItem(f'{history[BY]}({history[DATE]}) : {msg[:10] + ("..." if len(msg) > 10 else "")}')
    
    class MessengerMenuWindow(QMainWindow, QWidget, FORM_MESSAGE_MENU):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()

        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            self.sendBtn.clicked.connect(self.goSend)
            self.quickSendBtn.clicked.connect(self.goSend)
            self.archiveBtn.clicked.connect(self.goArchive)
            self.newMessage.hide()
            archive = msgArchiveDB.select(f"userId = '{userId}' AND new = True")
            if len(archive) != 0 :
                self.newMessage.show()
            msgGetter.start()
            msgGetter.update.connect(self.newMessage.show)
        
        def goBack(self):
            self.pre = MainWindow()
            self.pre.show()
            self.close()
        
        def goSend(self):
            self.post = MessengerSendWindow()
            self.post.show()
            self.close()

        def goArchive(self):
            self.post = ReceiveMessengerWindow()
            self.post.show()
            self.close()
    
    class MessengerSendWindow(QMainWindow, QWidget, FORM_SEND_MESSAGE):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()

        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            self.sendBtn.clicked.connect(self.send)
        
        def send(self):
            option = (self.option_1.isChecked()*1 + self.option_2.isChecked()*2)
            targetGrade = self.gradeNumberSpinBox.value()
            targetClass = self.classNumberSpinBox.value()
            targetName = self.nameComboBox.currentText()
            
            targetEnter = self.enterNumberLineEdit.text()
            
            dueTime = self.dueTimeEdit.dateTime().toString(self.dueTimeEdit.displayFormat())
            whereToGo = self.whereInput.text()
            additionalMsg = self.msgInput.toPlainText()
            if option == 1:
                target = f'{str(targetGrade)}.{str(targetClass)}.{targetName}'
                m = hashlib.sha256()
                m.update(target.encode('utf-8'))
                targetHash = m.hexdigest()
            elif option == 2:
                target = targetEnter
                m = hashlib.sha256()
                m.update(target.encode('utf-8'))
                targetHash = m.hexdigest()
            now = datetime.now()
            now = str(now.strftime("%Y.%m.%d/%H:%M"))
            ref = db.reference(f"message/{targetHash}")
            info = ref.get()
            if info is not None:
                ref.update({len(info):[userId,dueTime,whereToGo,additionalMsg,now]})
            else:
                ref.update({0 : [userId,dueTime,whereToGo,additionalMsg,now]})
            self.pre = MessengerMenuWindow()
            self.pre.show()
            self.close()

        def goBack(self):
            self.pre = MessengerMenuWindow()
            self.pre.show()
            self.close()
    
    class FailJoinVoteWindow(QMainWindow, QWidget, FORM_FAIL_JOIN_VOTING):
        def __init__(self,option = 0):
            super().__init__()
            self.option = option
            self.initUI()
            self.show()

        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            self.reasonLabel.setText('성공적으로 송신되었습니다!')
            self.goBackBtn.setText('확인')
            self.goBackBtn.setStyleSheet('''
                background-color : #516BEB;
                border-radius : 5px;
            ''')

        def goBack(self):
            self.vote = MessengerSendWindow()
            self.vote.show()
            self.close()
    
    class ViewVoteArchiveWindow(QMainWindow, QWidget, FORM_VIEW_MESSAGE_ARCHIVE):
        def __init__(self,data):
            super().__init__()
            self.data = data
            self.initUI()
            self.show()

        def initUI(self):
            self.setupUi(self)
            msgArchiveDB.update(f'id = "{self.data[ID]}"','new',0)
            self.goBackBtn.clicked.connect(self.goBack)
            self.checkBtn.setIcon(QIcon(os.path.join('.','assets','image','yes.png')))
            self.checkBtn.setIconSize(QSize(101,101))
            self.notForNowBtn.setIcon(QIcon(os.path.join('.','assets','image','no.png')))
            self.notForNowBtn.setIconSize(QSize(101,101))
            self.fromLbl.setText(f'{self.data[BY]}님 발신({self.data[DATE]})')
            when, where, msg = eval(self.data[CONTENT])
            self.whereLbl.setText(f'{where} (으)로')
            self.dueTimeLbl.setText(f'{when} 까지')
            self.additionalMsg.setPlainText(msg)

        def goBack(self):
            self.pre = ReceiveMessengerWindow()
            self.pre.show()
            self.close()
    
    if __name__ == '__main__':
        db_url = 'https://ham2021-main-project-default-rtdb.asia-southeast1.firebasedatabase.app/'
        cred = credentials.Certificate(os.path.join('.','assets','key.json'))
        default_app = firebase_admin.initialize_app(cred, {'databaseURL':db_url})

        userId = ''
        teacherPermission = False

        msgGetter = GetMessage()
        msgGetter.start()

        settingShuffleModule(userId,MainWindow)
        settingVoteModule(userId,MainWindow)
        app = QApplication(sys.argv)
        loginId = open(os.path.join('.','assets','login.txt'),'r')
        tempId = loginId.read()
        loginId.close()
        if tempId == '':
            win = LoginWindow()
        else:
            userId = tempId
            settingShuffleModule(userId)
            settingVoteModule(userId)
            win = MainWindow()
        sys.exit(app.exec_())

except Exception as e:
    print(e)
    input()