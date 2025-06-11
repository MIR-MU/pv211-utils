import unittest

from pv211_utils.cranfield.entities import CranfieldQueryBase, CranfieldDocumentBase


QUERY_ID = 123
QUERY_BODY_INPUT = "some body  text"
QUERY_BODY_OUTPUT = ["some", "body", "text"]

DOCUMENT_ID = "123"
DOCUMENT_AUTHORS_INPUT = "ashley,h. and zartarian,g."
DOCUMENT_AUTHORS_OUTPUT = ["ashley,h.", "zartarian,g."]
DOCUMENT_BIBLIOGRAPHY_INPUT = "j. ae. scs. 23, 1956, 1109."
DOCUMENT_BIBLIOGRAPHY_OUTPUT = ["j. ae. scs. 23", "1956", "1109."]
DOCUMENT_TITLE_INPUT = "some title"
DOCUMENT_TITLE_OUTPUT = ["some", "title"]
DOCUMENT_BODY_INPUT = "some  body text"
DOCUMENT_BODY_OUTPUT = ["some", "body", "text"]


class CranfieldQuery(CranfieldQueryBase):
    def __init__(self, query_id: int, body: str):
        body = body.split()
        super().__init__(query_id, body)


class CranfieldDocument(CranfieldDocumentBase):
    def __init__(
        self, document_id: str, authors: str, bibliography: str, title: str, body: str
    ):
        authors = authors.split(" and ")
        bibliography = bibliography.split(", ")
        title = title.split()
        body = body.split()
        super().__init__(document_id, authors, bibliography, title, body)


class TestCranfieldQueryBase(unittest.TestCase):
    def setUp(self):
        self.query = CranfieldQuery(QUERY_ID, QUERY_BODY_INPUT)

    def test_query_id(self):
        self.assertEqual(QUERY_ID, self.query.query_id)

    def test_query_body(self):
        self.assertEqual(QUERY_BODY_OUTPUT, self.query.body)


class TestCranfieldDocumentBase(unittest.TestCase):
    def setUp(self):
        self.document = CranfieldDocument(
            DOCUMENT_ID,
            DOCUMENT_AUTHORS_INPUT,
            DOCUMENT_BIBLIOGRAPHY_INPUT,
            DOCUMENT_TITLE_INPUT,
            DOCUMENT_BODY_INPUT,
        )

    def test_document_id(self):
        self.assertEqual(DOCUMENT_ID, self.document.document_id)

    def test_document_authors(self):
        self.assertEqual(DOCUMENT_AUTHORS_OUTPUT, self.document.authors)

    def test_document_bibliography(self):
        self.assertEqual(DOCUMENT_BIBLIOGRAPHY_OUTPUT, self.document.bibliography)

    def test_document_title(self):
        self.assertEqual(DOCUMENT_TITLE_OUTPUT, self.document.title)

    def test_document_body(self):
        self.assertEqual(DOCUMENT_BODY_OUTPUT, self.document.body)
