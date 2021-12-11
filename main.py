import sys,os,json,firebase_admin,random,time,hashlib,PyQt5
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
from assets.dataBaseModule import *
from assets.vote import *
try:
    db_url = 'https://ham2021-main-project-default-rtdb.asia-southeast1.firebasedatabase.app/'
    cred = credentials.Certificate(os.path.join('.','assets','key.json'))
    default_app = firebase_admin.initialize_app(cred, {'databaseURL':db_url})

    userId = ''
    fireBaseData = {}

    shuffle_col = 1
    shuffle_row = 1
    shuffle_number = [1]
    shuffle_location = []

    shuffleAchieveDB = DataBase('shuffle', userId = 'text', rowAndCol = 'text', shuffled = 'text', location = 'text', date = 'text')
    ID = 0
    USER_ID = 1
    ROW_AND_COL = 2
    SHUFFLED = 3
    LOCATION = 4
    DATE = 5

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
            self.shuffle = ShufflePrepareWindow()
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
    
    class ShufflePrepareWindow(QMainWindow, QWidget, FORM_SHUFFLE_PREPARE):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()

        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            self.makeBtn.clicked.connect(self.setting)
            self.achieveBtn.clicked.connect(self.achieve)
        
        def setting(self):
            self.settingWindow = ShuffleSettingWindow()
            self.settingWindow.show()
            self.close()
        
        def goBack(self):
            self.back = MainWindow()
            self.back.show()
            self.close()
        
        def achieve(self):
            self.achieveWindow = ShuffleAchieveWindow()
            self.achieveWindow.show()
            self.close()
    
    class ShuffleSettingWindow(QMainWindow, QWidget, FORM_SHUFFLE_SETTING):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()
        
        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            self.okBtn.clicked.connect(self.ok)
            self.rowSpinBox.setValue(shuffle_row)
            self.colSpinBox.setValue(shuffle_col)
            self.numberSpinBox.setValue(max(shuffle_number))
        
        def goBack(self):
            self.back = ShufflePrepareWindow()
            self.back.show()
            self.close()
        
        def ok(self):
            global shuffle_row, shuffle_col, shuffle_number, shuffle_location
            shuffle_row,shuffle_col,shuffle_number = self.rowSpinBox.value(), self.colSpinBox.value(), list(range(1,1+self.numberSpinBox.value()))
            shuffle_location = [[True for x in range(shuffle_row)] for y in range(shuffle_col)]
            self.next = ShuffleMainWindow()
            self.next.show()
            self.close()
        
    class SeatButton:
        def __init__(self,location,color = 'rgb(39, 197, 255)',option = 0) -> None:
            self.x, self.y = location[0],location[1]
            self.button = QPushButton('')
            self.changeColor(color)
            self.button.setMinimumHeight(10)
            self.button.setMinimumWidth(10)
            self.button.setMaximumHeight(100)
            self.button.setMaximumWidth(100)
            if option == 0: self.button.clicked.connect(lambda : self.clicked(self.x,self.y))
            if option == 1:
                if shuffle_location[self.y][self.x]:
                    self.changeColor('rgb(255, 255, 255)')
                else:
                    self.changeColor('rgb(255, 54, 14)')
            if option == 2:
                if (self.x,self.y) in shuffle_location:
                    self.changeColor('rgb(255, 255, 255)')
                else:
                    self.changeColor('rgb(255, 54, 14)')
        
        def clicked(self,x,y):
            global shuffle_location
            shuffle_location[y][x] = not shuffle_location[y][x]
            if shuffle_location[y][x]:
                self.changeColor('rgb(39, 197, 255)')
            else:
                self.changeColor('rgb(255, 54, 14)')
        
        def changeColor(self,color):
            self.button.setStyleSheet(f'''
                font-family: 'Noto Sans CJK KR Black';
                font-size : 12px;
                color : black;
                background-color : {color};
                border-radius : 5px;
            ''')
    
    class ShuffleMainWindow(QMainWindow, QWidget, FORM_SHUFFLE_MAIN):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()
        
        def initUI(self):
            self.setupUi(self)
            self.goBackBtn.clicked.connect(self.goBack)
            for y in range(shuffle_col):
                for x in range(shuffle_row):
                    self.viewer.addWidget(SeatButton((x,y)).button,y,x)
            self.getResultBtn.clicked.connect(self.getResult)
        
        def goBack(self):
            self.back = ShuffleSettingWindow()
            self.back.show()
            self.close()
        
        def getResult(self):
            exceptNums = self.exceptInput.text().split(',')
            for num in exceptNums:
                if num in shuffle_number:
                    del shuffle_number[num]
            random.shuffle(shuffle_number)
            shuffled = shuffle_number
            sumOfAvail = 0
            for y in range(shuffle_col):
                for x in range(shuffle_row):
                    sumOfAvail += int(shuffle_location[y][x])
            fitNum = min(len(shuffled),sumOfAvail)
            shuffled = shuffled[:fitNum]
            location = []
            for i in range(fitNum):
                x = random.randint(0,shuffle_row-1)
                y = random.randint(0,shuffle_col-1)
                while (x,y) in location or not shuffle_location[y][x]:
                    x = random.randint(0,shuffle_row-1)
                    y = random.randint(0,shuffle_col-1)
                location.append((x,y))
            self.result = ShuffleResultWindow(shuffled,location)
            self.result.show()
            self.close()
    
    class ShuffleResultWindow(QMainWindow, QWidget, FORM_SHUFFLE_RESULT):
        def __init__(self,shuffled,location):
            super().__init__()
            self.location = location
            self.shuffled = shuffled
            self.initUI()
            self.show()
        
        def initUI(self):
            self.setupUi(self)
            self.okBtn.clicked.connect(self.end)
            now = datetime.now()
            now = str(now.strftime("%Y.%m.%d/%H:%M:%S"))
            shuffleAchieveDB.add((userId,f'{str(shuffle_row)}x{str(shuffle_col)}',str(self.shuffled),str(self.location),now))
            for y in range(shuffle_col):
                for x in range(shuffle_row):
                    self.viewer.addWidget(SeatButton((x,y),option=1).button,y,x)
            for location in self.location:
                self.viewer.itemAtPosition(location[1],location[0]).widget().setText(str(self.shuffled.pop()))
        
        def end(self):
            self.shufflePrepare = ShufflePrepareWindow()
            self.shufflePrepare.show()
            self.close()
        
    class ShuffleAchieveWindow(QMainWindow, QWidget, FORM_VOTE_ACHIEVE):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.show()
        
        def initUI(self):
            self.setupUi(self)
            self.achieve = shuffleAchieveDB.select(f'userId = "{userId}"')
            self.achieveList.addItems([item[DATE] for item in self.achieve][::-1])
            self.removeBtn.hide()
            self.viewBtn.hide()
            self.achieveList.clicked.connect(self.showTools)
            self.viewBtn.clicked.connect(self.view)
            self.removeBtn.clicked.connect(self.removeAchieve)
            self.goBackBtn.clicked.connect(self.goBack)

        def removeAchieve(self):
            deletedItemId = self.achieve[self.achieveList.currentRow()][ID]
            shuffleAchieveDB.excute(f'''
                DELETE FROM 'shuffle' WHERE id = {deletedItemId}
            ''')
            self.achieveList.takeItem(self.achieveList.currentRow())
            self.achieve = shuffleAchieveDB.select(f'userId = "{userId}"')
            self.achieveList.setCurrentRow(-1)
            self.removeBtn.hide()
            self.viewBtn.hide()

        def view(self):
            self.vote = ViewShuffleAchieveWindow(self.achieve[self.achieveList.currentRow()])
            self.vote.show()
            self.close()
        
        def goBack(self):
            self.pre = ShufflePrepareWindow()
            self.pre.show()
            self.close()

        def showTools(self):
            self.removeBtn.show()
            self.viewBtn.show()
    
    class ViewShuffleAchieveWindow(QMainWindow, QWidget, FORM_SHUFFLE_RESULT):
        def __init__(self,achieve):
            super().__init__()
            self.achieve = achieve
            self.initUI()
            self.show()
        
        def initUI(self):
            global shuffle_location
            self.setupUi(self)
            self.okBtn.clicked.connect(self.goBack)
            row,col = map(int,self.achieve[ROW_AND_COL].split('x'))
            self.location = eval(self.achieve[LOCATION])
            self.shuffled = eval(self.achieve[SHUFFLED])
            shuffle_location = self.location
            for y in range(col):
                for x in range(row):
                    self.viewer.addWidget(SeatButton((x,y),option=2).button,y,x)
            for location in self.location:
                x = location[0]
                y = location[1]
                self.viewer.itemAtPosition(y,x).widget().setText(str(self.shuffled.pop()))

        def goBack(self):
            self.pre = ShuffleAchieveWindow()
            self.pre.show()
            self.close()

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = LoginWindow()
        sys.exit(app.exec_())

except Exception as e:
    print(e)
    input()