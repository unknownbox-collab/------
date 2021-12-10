import os
from PyQt5 import uic

DATABASE_PATH = os.path.join('.','assets')

FORM_LOGIN            = uic.loadUiType(os.path.join('.','assets','ui','login.ui'))[0]
FORM_CREDIT           = uic.loadUiType(os.path.join('.','assets','ui','credit.ui'))[0]
FORM_HOW_TO_USE       = uic.loadUiType(os.path.join('.','assets','ui','howToUse.ui'))[0]
FORM_JOIN_VOTE        = uic.loadUiType(os.path.join('.','assets','ui','join.ui'))[0]
FORM_MAIN             = uic.loadUiType(os.path.join('.','assets','ui','main.ui'))[0]
FORM_VOTE             = uic.loadUiType(os.path.join('.','assets','ui','vote.ui'))[0]
FORM_MAKE_VOTE_OPTION = uic.loadUiType(os.path.join('.','assets','ui','makeVote.ui'))[0]
FORM_SUBJECT_VOTE     = uic.loadUiType(os.path.join('.','assets','ui','voteSetSubject.ui'))[0]
FORM_GO_BACK_ALERT    = uic.loadUiType(os.path.join('.','assets','ui','goBackAlert.ui'))[0]
FORM_WAIT_VOTE        = uic.loadUiType(os.path.join('.','assets','ui','publishedVote.ui'))[0]
FORM_END_VOTE         = uic.loadUiType(os.path.join('.','assets','ui','endVote.ui'))[0]