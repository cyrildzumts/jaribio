
from django.utils.translation import gettext_lazy as _

REQUEST_METHOD_GET = "GET"
REQUEST_METHOD_POST = "POST"

QUESTION_MAX_LENGTH = 250
DESCRIPTION_MAX_SIZE = 512
MAX_QUIZ_QUESTIONS = 20

QUESTION_TYPE_UNIQUE = 0
QUESTION_TYPE_MCQ = 1
QUESTION_TYPE_BOOLEAN = 2

QUESTION_TYPES = (
    (QUESTION_TYPE_UNIQUE, _('UNIQUE QUESTION')),
    (QUESTION_TYPE_MCQ, _('MULTIPLE CHOICES QUESTION')),
    (QUESTION_TYPE_BOOLEAN, _('TRUE OR FALSE'))
)

ANSWER_ORDER_CONTENT = 0
ANSWER_ORDER_RANDOM = 1
ANSWER_ORDER_NONE = 2

ANSWER_ORDERS = (
    (ANSWER_ORDER_CONTENT, _('CONTENT')),
    (ANSWER_ORDER_RANDOM, _('RANDOM')),
    (ANSWER_ORDER_NONE, _('NONE'))
)

ANSWER_TYPE_CONTENT = 0
ANSWER_TYPE_BOOLEAN = 1

ANSWER_TYPES = (
    (ANSWER_TYPE_CONTENT, _('CONTENT')),
    (ANSWER_TYPE_BOOLEAN, _('TRUE OR FALSE'))
)

ANSWER_SCORE_STANDARD = 0
ANSWER_SCORE_DOUBLE = 1
ANSWER_SCORE_TRIPLE = 2

ANSWER_SCORE_TYPES = (
    (ANSWER_SCORE_STANDARD, _('STANDARD')),
    (ANSWER_SCORE_DOUBLE, _('SCORE COUNT DOUBLE')),
    (ANSWER_SCORE_TRIPLE, _('SCORE COUNT TRIPLE'))
)

GOOD_ANSWER_IN_ROW_BONUS = 0.25

QUIZ_TYPE_CHALLENGE = 0
QUIZ_TYPE_DUEL = 1
QUIZ_TYPE_TOURNAMENT = 2

QUIZ_TYPES = (
    (QUIZ_TYPE_CHALLENGE, _('CHALLENGE')),
    (QUIZ_TYPE_DUEL, _('DUEL')),
    (QUIZ_TYPE_TOURNAMENT, _('TOURNAMENT')),
)