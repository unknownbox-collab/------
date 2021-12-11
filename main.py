try:
    from assets.dataBaseModule import *
    from assets.vote import *

    db_url = 'https://ham2021-main-project-default-rtdb.asia-southeast1.firebasedatabase.app/'
    cred = credentials.Certificate(os.path.join('.','assets','key.json'))
    default_app = firebase_admin.initialize_app(cred, {'databaseURL':db_url})

    userId = ''
    fireBaseData = {}

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

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = LoginWindow()
        sys.exit(app.exec_())
except Exception as e:
    print(e)
    input()