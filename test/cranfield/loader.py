import unittest

from pv211_utils.cranfield.loader import load_queries, load_documents, load_judgements


NUM_QUERIES = 225
NUM_DOCUMENTS = 1400
NUM_JUDGEMENTS = 1837


class TestLoadQueries(unittest.TestCase):
    def setUp(self):
        self.queries = load_queries()
        self.query = self.queries[14]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES, len(self.queries))

    def test_query_body(self):
        self.assertEqual('papers on shock-sound wave interaction .', self.query.body)


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        self.documents = load_documents()
        self.document = self.documents[14]

    def test_number_of_documents(self):
        self.assertEqual(NUM_DOCUMENTS, len(self.documents))

    def test_document_authors(self):
        self.assertEqual('ashley,h. and zartarian,g.', self.document.authors)

    def test_document_bibliography(self):
        self.assertEqual('j. ae. scs. 23, 1956, 1109.', self.document.bibliography)

    def test_document_title(self):
        self.assertEqual('piston theory - a new aerodynamic tool for the aeroelastician .', self.document.title)

    def test_document_body(self):
        self.assertTrue(self.document.body.startswith('piston theory - a new aerodynamic tool for the aeroelastician '))
        self.assertTrue(self.document.body.endswith('when analyzing aerodynamic- thermoelastic interaction problems .'))


class TestLoadJudgements(unittest.TestCase):
    def setUp(self):
        queries = load_queries()
        documents = load_documents()
        self.judgements = load_judgements(queries, documents)
        self.query = queries[1]
        self.relevant_document = documents[486]
        self.irrelevant_document = documents[487]

    def test_number_of_judgements(self):
        self.assertEqual(NUM_JUDGEMENTS, len(self.judgements))

    def test_relevant_document(self):
        self.assertIn((self.query, self.relevant_document), self.judgements)

    def test_irrelevant_document(self):
        self.assertNotIn((self.query, self.irrelevant_document), self.judgements)
