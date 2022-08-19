import unittest

from pv211_utils.beir.loader import load_queries, load_documents, load_judgements, load_beir_datasets
from pv211_utils.beir.entities import RawBeirDataset, RawBeirDatasets


NUM_QUERIES = 699
NUM_DOCUMENTS = 22998
NUM_JUDGEMENTS = 1696
NUM_COMBINED_DOCUMENTS = 58374


class TestLoadQueries(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets(download_location, [android])
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.queries = load_queries(raw_test_data[1])
        self.query = self.queries["11546"]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES, len(self.queries))

    def test_query_body(self):
        self.assertEqual('Android chroot ubuntu - is it possible to get ubuntu to recognise usb devices',
                         self.query.body)


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets(download_location, [android])
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.documents = load_documents(raw_test_data[0])
        self.document = self.documents['51829']

    def test_number_of_documents(self):
        self.assertEqual(NUM_DOCUMENTS, len(self.documents))

    def test_document_body(self):
        self.assertTrue(self.document.body.startswith('I want to send files to android tablet with a application from'))
        self.assertTrue(self.document.body.endswith(' drive? my application that sent files written via Delphi.'))


class TestLoadJudgements(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets(download_location, [android])
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        queries = load_queries(raw_test_data[1])
        documents = load_documents(raw_test_data[0])

        self.judgements = load_judgements(queries, documents, raw_test_data[2])
        self.query = queries["66595"]
        self.relevant_document = documents['81292']
        self.irrelevant_document = documents['51829']

    def test_number_of_judgements(self):
        self.assertEqual(NUM_JUDGEMENTS, len(self.judgements))

    def test_relevant_document(self):
        self.assertIn((self.query, self.relevant_document), self.judgements)

    def test_irrelevant_document(self):
        self.assertNotIn((self.query, self.irrelevant_document), self.judgements)
