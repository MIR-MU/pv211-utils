import unittest

from pv211_utils.trec.loader import load_queries, load_documents, load_judgements


NUM_QUERIES = 150
NUM_DOCUMENTS = 527890
NUM_JUDGEMENTS_TRAIN = 7102
NUM_JUDGEMENTS_VALIDATION = 1858
NUM_JUDGEMENTS_TEST = 4726


class TestLoadQueries(unittest.TestCase):
    def setUp(self):
        self.queries = load_queries()
        self.query = self.queries[409]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES, len(self.queries))

    def test_query_title(self):
        self.assertEqual('legal, Pan Am, 103', self.query.title)

    def test_query_body(self):
        self.assertTrue(self.query.body.startswith('What legal actions have resulted'))

    def test_query_narrative(self):
        self.assertTrue(self.query.narrative.startswith('Documents describing any charges, claims'))


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        self.documents = load_documents()
        self.financial_times_document = self.documents['FT911-3']
        self.federal_register_document = self.documents['FR940104-0-00002']
        self.fbis_document = self.documents['FBIS3-1']
        self.la_times_document = self.documents['LA010189-0001']

    def test_number_of_documents(self):
        self.assertEqual(NUM_DOCUMENTS, len(self.documents))

    def test_financial_times_document_body(self):
        self.assertTrue(self.financial_times_document.body.startswith('CONTIGAS, the German gas group'))

    def test_federal_register_document_body(self):
        self.assertTrue(self.federal_register_document.body.startswith('DEPARTMENT OF AGRICULTURE'))

    def test_fbis_document_body(self):
        self.assertTrue(self.fbis_document.body.startswith('POLITICIANS,  PARTY PREFERENCES'))

    def test_la_times_document_body(self):
        self.assertTrue(self.la_times_document.body.startswith('The onset of the new Gorbachev policy of glasnost'))


class TestLoadJudgements(unittest.TestCase):
    def setUp(self):
        queries = load_queries()
        documents = load_documents()

        self.judgements_train = load_judgements(queries, documents, 'train')
        self.judgements_validation = load_judgements(queries, documents, 'validation')
        self.judgements_test = load_judgements(queries, documents, 'test')

        self.query_train = queries[301]
        self.query_validation = queries[400]
        self.query_test = queries[401]

        self.relevant_document_train = documents['FBIS3-10937']
        self.irrelevant_document_train = documents['FBIS3-10634']
        self.relevant_document_validation = documents['FT944-6336']
        self.irrelevant_document_validation = documents['FT944-3328']
        self.relevant_document_test = documents['LA100290-0174']
        self.irrelevant_document_test = documents['LA100490-0070']

    def test_number_of_judgements_train(self):
        self.assertEqual(NUM_JUDGEMENTS_TRAIN, len(self.judgements_train))

    def test_number_of_judgements_validation(self):
        self.assertEqual(NUM_JUDGEMENTS_VALIDATION, len(self.judgements_validation))

    def test_number_of_judgements_test(self):
        self.assertEqual(NUM_JUDGEMENTS_TEST, len(self.judgements_test))

    def test_relevant_document_train(self):
        self.assertIn((self.query_train, self.relevant_document_train), self.judgements_train)
        self.assertNotIn((self.query_train, self.relevant_document_train), self.judgements_validation)
        self.assertNotIn((self.query_train, self.relevant_document_train), self.judgements_test)

    def test_irrelevant_document_train(self):
        self.assertNotIn((self.query_train, self.irrelevant_document_train), self.judgements_train)
        self.assertNotIn((self.query_train, self.irrelevant_document_train), self.judgements_validation)
        self.assertNotIn((self.query_train, self.irrelevant_document_train), self.judgements_test)

    def test_relevant_document_validation(self):
        self.assertNotIn((self.query_validation, self.relevant_document_validation), self.judgements_train)
        self.assertIn((self.query_validation, self.relevant_document_validation), self.judgements_validation)
        self.assertNotIn((self.query_validation, self.relevant_document_validation), self.judgements_test)

    def test_irrelevant_document_validation(self):
        self.assertNotIn((self.query_validation, self.irrelevant_document_validation), self.judgements_train)
        self.assertNotIn((self.query_validation, self.irrelevant_document_validation), self.judgements_validation)
        self.assertNotIn((self.query_validation, self.irrelevant_document_validation), self.judgements_test)

    def test_relevant_document_test(self):
        self.assertNotIn((self.query_test, self.relevant_document_test), self.judgements_train)
        self.assertNotIn((self.query_test, self.relevant_document_test), self.judgements_validation)
        self.assertIn((self.query_test, self.relevant_document_test), self.judgements_test)

    def test_irrelevant_document_test(self):
        self.assertNotIn((self.query_test, self.irrelevant_document_test), self.judgements_train)
        self.assertNotIn((self.query_test, self.irrelevant_document_test), self.judgements_validation)
        self.assertNotIn((self.query_test, self.irrelevant_document_test), self.judgements_test)
