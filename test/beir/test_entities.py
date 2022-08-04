import unittest

from pv211_utils.beir.entities import BeirQueryBase, BeirDocumentBase


QUERY_ID = 123
QUERY_BODY_INPUT = 'some body  text'
QUERY_BODY_OUTPUT = ['some', 'body', 'text']

DOCUMENT_ID = '123'
DOCUMENT_BODY_INPUT = 'some  body text'
DOCUMENT_BODY_OUTPUT = ['some', 'body', 'text']


class BeirQuery(BeirQueryBase):
    def __init__(self, query_id: int, body: str):
        body = body.split()
        super().__init__(query_id, body)


class BeirDocument(BeirDocumentBase):
    def __init__(self, document_id: str, body: str):
        body = body.split()
        super().__init__(document_id, body)


class TestBeirQueryBase(unittest.TestCase):
    def setUp(self):
        self.query = BeirQuery(QUERY_ID, QUERY_BODY_INPUT)

    def test_query_id(self):
        self.assertEqual(QUERY_ID, self.query.query_id)

    def test_query_body(self):
        self.assertEqual(QUERY_BODY_OUTPUT, self.query.body)


class TestBeirDocumentBase(unittest.TestCase):
    def setUp(self):
        self.document = BeirDocument(DOCUMENT_ID, DOCUMENT_BODY_INPUT)

    def test_document_id(self):
        self.assertEqual(DOCUMENT_ID, self.document.document_id)

    def test_document_body(self):
        self.assertEqual(DOCUMENT_BODY_OUTPUT, self.document.body)
