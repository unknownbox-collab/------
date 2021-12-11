import os
from PyQt5 import uic

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join('.','assets','information.db')

FORM_LOGIN             = uic.loadUiType(os.path.join('.','assets','ui','login.ui'))[0]
FORM_CREDIT            = uic.loadUiType(os.path.join('.','assets','ui','credit.ui'))[0]
FORM_HOW_TO_USE        = uic.loadUiType(os.path.join('.','assets','ui','howToUse.ui'))[0]
FORM_JOIN_VOTE         = uic.loadUiType(os.path.join('.','assets','ui','join.ui'))[0]
FORM_MAIN              = uic.loadUiType(os.path.join('.','assets','ui','main.ui'))[0]
FORM_VOTE              = uic.loadUiType(os.path.join('.','assets','ui','vote.ui'))[0]
FORM_MAKE_VOTE_OPTION  = uic.loadUiType(os.path.join('.','assets','ui','makeVote.ui'))[0]
FORM_SUBJECT_VOTE      = uic.loadUiType(os.path.join('.','assets','ui','voteSetSubject.ui'))[0]
FORM_GO_BACK_ALERT     = uic.loadUiType(os.path.join('.','assets','ui','goBackAlert.ui'))[0]
FORM_WAIT_VOTE         = uic.loadUiType(os.path.join('.','assets','ui','publishedVote.ui'))[0]
FORM_END_VOTE          = uic.loadUiType(os.path.join('.','assets','ui','endVote.ui'))[0]
FORM_VOTE_ACHIEVE      = uic.loadUiType(os.path.join('.','assets','ui','voteAchieve.ui'))[0]
FORM_VIEW_VOTE_ACHIEVE = uic.loadUiType(os.path.join('.','assets','ui','viewVoteAchieve.ui'))[0]
FORM_FAIL_JOIN_VOTING  = uic.loadUiType(os.path.join('.','assets','ui','failToJoinVoting.ui'))[0]
FORM_JOIN_AND_VOTING   = uic.loadUiType(os.path.join('.','assets','ui','joinAndVoting.ui'))[0]

FORM_SHUFFLE_PREPARE   = uic.loadUiType(os.path.join('.','assets','ui','shufflePrepare.ui'))[0]
FORM_SHUFFLE_SETTING   = uic.loadUiType(os.path.join('.','assets','ui','shuffleSetting.ui'))[0]
FORM_SHUFFLE_MAIN      = uic.loadUiType(os.path.join('.','assets','ui','shuffleMain.ui'))[0]
FORM_SHUFFLE_RESULT    = uic.loadUiType(os.path.join('.','assets','ui','shuffleResult.ui'))[0]