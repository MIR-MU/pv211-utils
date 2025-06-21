import unittest

from pv211_utils.beir.loader import (load_queries,
                                     load_documents,
                                     load_judgements,
                                     load_beir_datasets)
from pv211_utils.beir.entities import RawBeirDataset, RawBeirDatasets


NUM_QUERIES = 699
NUM_DOCUMENTS = 22998
NUM_JUDGEMENTS = 1696

NUM_COMBINED_DOCUMENTS = 457188
NUM_COMBINED_TEST_QUERIES = 11831
NUM_COMBINED_TRAIN_QUERIES = 657
NUM_COMBINED_DEV_QUERIES = 657
NUM_COMBINED_TEST_JUDGEMENTS = 1254
NUM_COMBINED_TRAIN_JUDGEMENTS = 111
NUM_COMBINED_DEV_JUDGEMENTS = 81


class TestLoadQueries(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([android], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.queries = load_queries(raw_test_data[1])
        self.query = self.queries["1"]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES, len(self.queries))

    def test_query_body(self):
        self.assertEqual('problem in installing apps in karbonn A5i',
                         self.query.body)


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([android], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.documents = load_documents(raw_test_data[0])
        self.document = self.documents['1']

    def test_number_of_documents(self):
        self.assertEqual(NUM_DOCUMENTS, len(self.documents))

    def test_document_body(self):
        body_begining_str = "I am playing around with my brand new Motorola Defy" \
                            " and trying to find a way to manage my contacts."
        self.assertTrue(self.document.body.startswith(body_begining_str))
        self.assertTrue(self.document.body.endswith("Does anyone have a solution for me ?"))


class TestLoadJudgements(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([android], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        queries = load_queries(raw_test_data[1])
        documents = load_documents(raw_test_data[0])

        self.judgements = load_judgements(queries, documents, raw_test_data[2])
        self.query = queries["2"]
        self.relevant_document = documents['27']
        self.irrelevant_document = documents['1']

    def test_number_of_judgements(self):
        self.assertEqual(NUM_JUDGEMENTS, len(self.judgements))

    def test_relevant_document(self):
        self.assertIn((self.query, self.relevant_document), self.judgements)

    def test_irrelevant_document(self):
        self.assertNotIn((self.query, self.irrelevant_document), self.judgements)
