import unittest

from pv211_utils.trec.entities import TrecQueryBase, TrecDocumentBase


QUERY_ID = 123
QUERY_TITLE_INPUT = 'some  title'
QUERY_TITLE_OUTPUT = ['some', 'title']
QUERY_BODY_INPUT = 'some body  text'
QUERY_BODY_OUTPUT = ['some', 'body', 'text']
QUERY_NARRATIVE_INPUT = 'some narrative'
QUERY_NARRATIVE_OUTPUT = ['some', 'narrative']

DOCUMENT_ID = '123'
DOCUMENT_BODY_INPUT = 'some  body text'
DOCUMENT_BODY_OUTPUT = ['some', 'body', 'text']


class TrecQuery(TrecQueryBase):
    def __init__(self, query_id: int, title: str, body: str, narrative: str):
        title = title.split()
        body = body.split()
        narrative = narrative.split()
        super().__init__(query_id, title, body, narrative)


class TrecDocument(TrecDocumentBase):
    def __init__(self, document_id: str, body: str):
        body = body.split()
        super().__init__(document_id, body)


class TestTrecQueryBase(unittest.TestCase):
    def setUp(self):
        self.query = TrecQuery(QUERY_ID, QUERY_TITLE_INPUT, QUERY_BODY_INPUT, QUERY_NARRATIVE_INPUT)

    def test_query_id(self):
        self.assertEqual(QUERY_ID, self.query.query_id)

    def test_query_title(self):
        self.assertEqual(QUERY_TITLE_OUTPUT, self.query.title)

    def test_query_body(self):
        self.assertEqual(QUERY_BODY_OUTPUT, self.query.body)

    def test_query_narrative(self):
        self.assertEqual(QUERY_NARRATIVE_OUTPUT, self.query.narrative)


class TestTrecDocumentBase(unittest.TestCase):
    def setUp(self):
        self.document = TrecDocument(DOCUMENT_ID, DOCUMENT_BODY_INPUT)

    def test_document_id(self):
        self.assertEqual(DOCUMENT_ID, self.document.document_id)

    def test_document_body(self):
        self.assertEqual(DOCUMENT_BODY_OUTPUT, self.document.body)
