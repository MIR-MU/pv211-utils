import unittest
from typing import List

from pv211_utils.arqmath.entities import ArqmathQueryBase, ArqmathQuestionBase, ArqmathAnswerBase


QUERY_ID = 123
QUERY_TITLE_INPUT = 'some  title'
QUERY_TITLE_OUTPUT = ['some', 'title']
QUERY_BODY_INPUT = 'some body  text'
QUERY_BODY_OUTPUT = ['some', 'body', 'text']
QUERY_TAGS = ['some', 'tags']

ANSWER_DOCUMENT_ID = '456'
ANSWER_BODY_INPUT = 'some  body text'
ANSWER_BODY_OUTPUT = ['some', 'body', 'text']
ANSWER_UPVOTES = 456
ANSWER_IS_ACCEPTED = True

QUESTION_DOCUMENT_ID = '123'
QUESTION_TITLE_INPUT = 'some  title'
QUESTION_TITLE_OUTPUT = ['some', 'title']
QUESTION_BODY_INPUT = 'some  body text'
QUESTION_BODY_OUTPUT = ['some', 'body', 'text']
QUESTION_TAGS = ['some', 'tags']
QUESTION_UPVOTES = 456
QUESTION_VIEWS = 789
QUESTION_ANSWER_DOCUMENT_IDS = [ANSWER_DOCUMENT_ID]


class ArqmathQuery(ArqmathQueryBase):
    def __init__(self, query_id: int, title: str, body: str, tags: List[str]):
        title = title.split()
        body = body.split()
        super().__init__(query_id, title, body, tags)


class ArqmathAnswer(ArqmathAnswerBase):
    def __init__(self, document_id: str, body: str, upvotes: int, is_accepted: bool):
        body = body.split()
        super().__init__(document_id, body, upvotes, is_accepted)


class ArqmathQuestion(ArqmathQuestionBase):
    def __init__(self, document_id: str, title: str, body: str, tags: List[str],
                 upvotes: int, views: int, answers: List[ArqmathAnswerBase]):
        title = title.split()
        body = body.split()
        super().__init__(document_id, title, body, tags, upvotes, views, answers)


class TestArqmathQueryBase(unittest.TestCase):
    def setUp(self):
        self.query = ArqmathQuery(QUERY_ID, QUERY_TITLE_INPUT, QUERY_BODY_INPUT, QUERY_TAGS)

    def test_query_id(self):
        self.assertEqual(QUERY_ID, self.query.query_id)

    def test_query_title(self):
        self.assertEqual(QUERY_TITLE_OUTPUT, self.query.title)

    def test_query_body(self):
        self.assertEqual(QUERY_BODY_OUTPUT, self.query.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_TAGS, self.query.tags)


class TestArqmathAnswerBase(unittest.TestCase):
    def setUp(self):
        self.answer = ArqmathAnswer(ANSWER_DOCUMENT_ID, ANSWER_BODY_INPUT, ANSWER_UPVOTES, ANSWER_IS_ACCEPTED)

    def test_answer_document_id(self):
        self.assertEqual(ANSWER_DOCUMENT_ID, self.answer.document_id)

    def test_answer_body(self):
        self.assertEqual(ANSWER_BODY_OUTPUT, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestArqmathQuestionBase(unittest.TestCase):
    def setUp(self):
        self.answer = ArqmathAnswer(ANSWER_DOCUMENT_ID, ANSWER_BODY_INPUT, ANSWER_UPVOTES, ANSWER_IS_ACCEPTED)
        self.question = ArqmathQuestion(QUESTION_DOCUMENT_ID, QUESTION_TITLE_INPUT, QUESTION_BODY_INPUT, QUESTION_TAGS,
                                        QUESTION_UPVOTES, QUESTION_VIEWS, [self.answer])

    def test_question_document_id(self):
        self.assertEqual(QUESTION_DOCUMENT_ID, self.question.document_id)

    def test_question_title(self):
        self.assertEqual(QUESTION_TITLE_OUTPUT, self.question.title)

    def test_question_body(self):
        self.assertEqual(QUESTION_BODY_OUTPUT, self.question.body)

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        answer_document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, answer_document_ids)
