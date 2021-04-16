import unittest

from pv211_utils.trec.loader import load_queries, load_documents, load_judgements


CACHE_DOWNLOAD = False

NUM_QUERIES_TRAIN = 80
NUM_QUERIES_VALIDATION = 20
NUM_QUERIES_TEST = 50
NUM_DOCUMENTS = 527890

DOCUMENT_IDS = set([
    'FT911-3',
    'FR940104-0-00002',
    'FBIS3-1',
    'LA010189-0001',
    'FBIS3-10937',
    'FBIS3-10634',
    'FT944-6336',
    'FT944-3328',
    'LA100290-0174',
    'LA100490-0070',
])
DOCUMENTS = load_documents(cache_download=CACHE_DOWNLOAD, filter_document_ids=DOCUMENT_IDS)


class TestLoadQueries(unittest.TestCase):
    def setUp(self):
        self.queries_train = load_queries(subset='train')
        self.queries_validation = load_queries(subset='validation')
        self.queries_test = load_queries(subset='test')
        self.query = self.queries_test[409]

    def test_number_of_queries_train(self):
        self.assertEqual(NUM_QUERIES_TRAIN, len(self.queries_train))

    def test_number_of_queries_validation(self):
        self.assertEqual(NUM_QUERIES_VALIDATION, len(self.queries_validation))

    def test_number_of_queries_test(self):
        self.assertEqual(NUM_QUERIES_TEST, len(self.queries_test))

    def test_query_title(self):
        self.assertEqual('legal, Pan Am, 103', self.query.title)

    def test_query_body(self):
        self.assertTrue(self.query.body.startswith('What legal actions have resulted'))

    def test_query_narrative(self):
        self.assertTrue(self.query.narrative.startswith('Documents describing any charges, claims'))


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        self.financial_times_document = DOCUMENTS['FT911-3']
        self.federal_register_document = DOCUMENTS['FR940104-0-00002']
        self.fbis_document = DOCUMENTS['FBIS3-1']
        self.la_times_document = DOCUMENTS['LA010189-0001']

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
        queries_train = load_queries(subset='train')
        queries_validation = load_queries(subset='validation')
        queries_test = load_queries(subset='test')

        self.judgements_train = load_judgements(queries_train, DOCUMENTS, 'train')
        self.judgements_validation = load_judgements(queries_validation, DOCUMENTS, 'validation')
        self.judgements_test = load_judgements(queries_test, DOCUMENTS, 'test')

        self.query_train = queries_train[301]
        self.query_validation = queries_validation[400]
        self.query_test = queries_test[401]

        self.relevant_document_train = DOCUMENTS['FBIS3-10937']
        self.irrelevant_document_train = DOCUMENTS['FBIS3-10634']
        self.relevant_document_validation = DOCUMENTS['FT944-6336']
        self.irrelevant_document_validation = DOCUMENTS['FT944-3328']
        self.relevant_document_test = DOCUMENTS['LA100290-0174']
        self.irrelevant_document_test = DOCUMENTS['LA100490-0070']

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
