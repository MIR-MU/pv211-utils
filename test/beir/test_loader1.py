import unittest

from pv211_utils.beir.loader import (
    load_queries,
    load_documents,
    load_judgements,
    load_beir_datasets,
    split_beir_dataset,
)
from pv211_utils.beir.entities import RawBeirDataset, RawBeirDatasets

# Constants for the 'android' dataset
NUM_QUERIES = 699
NUM_DOCUMENTS = 22998
NUM_JUDGEMENTS = 1696

# TODO: Adjust these constants for the first half of the datasets (android, english, gaming, gis, mathematica, physics)
NUM_COMBINED_DOCUMENTS = 0  # UPDATE THIS
NUM_COMBINED_TEST_QUERIES = 0  # UPDATE THIS
NUM_COMBINED_TRAIN_QUERIES = 0  # UPDATE THIS
NUM_COMBINED_DEV_QUERIES = 0  # UPDATE THIS
NUM_COMBINED_TEST_JUDGEMENTS = 0  # UPDATE THIS
NUM_COMBINED_TRAIN_JUDGEMENTS = 0  # UPDATE THIS
NUM_COMBINED_DEV_JUDGEMENTS = 0  # UPDATE THIS


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
        self.assertEqual("problem in installing apps in karbonn A5i", self.query.body)


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([android], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.documents = load_documents(raw_test_data[0])
        self.document = self.documents["1"]

    def test_number_of_documents(self):
        self.assertEqual(NUM_DOCUMENTS, len(self.documents))

    def test_document_body(self):
        body_begining_str = (
            "I am playing around with my brand new Motorola Defy"
            " and trying to find a way to manage my contacts."
        )
        self.assertTrue(self.document.body.startswith(body_begining_str))
        self.assertTrue(
            self.document.body.endswith("Does anyone have a solution for me ?")
        )


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
        self.relevant_document = documents["27"]
        self.irrelevant_document = documents["1"]

    def test_number_of_judgements(self):
        self.assertEqual(NUM_JUDGEMENTS, len(self.judgements))

    def test_relevant_document(self):
        self.assertIn((self.query, self.relevant_document), self.judgements)

    def test_irrelevant_document(self):
        self.assertNotIn((self.query, self.irrelevant_document), self.judgements)


class TestCombineAndSplitPart1(unittest.TestCase):
    def setUp(self):
        # Datasets for the first half
        android = RawBeirDataset("android", test=True)
        english = RawBeirDataset("english", test=True)
        gaming = RawBeirDataset("gaming", test=True)
        gis = RawBeirDataset("gis", test=True)
        mathematica = RawBeirDataset("mathematica", test=True)
        physics = RawBeirDataset("physics", test=True)
        download_location = "datasets"

        desired_datasets = RawBeirDatasets(
            datasets=[
                android,
                english,
                gaming,
                gis,
                mathematica,
                physics,
            ],
            download_location=download_location,
        )
        _, _, raw_test_data = load_beir_datasets(desired_datasets)

        # Split the dataset
        raw_train_data, raw_test_data = split_beir_dataset(raw_test_data, split_factor=0.9)
        raw_dev_data, raw_train_data = split_beir_dataset(raw_train_data, split_factor=0.5)

        raw_corpus_test, raw_queries_test, raw_qrels_test = list(raw_test_data)
        _, raw_queries_train, raw_qrels_train = list(raw_train_data)
        _, raw_queries_dev, raw_qrels_dev = list(raw_dev_data)

        self.documents = load_documents(raw_corpus_test)
        self.test_queries = load_queries(raw_queries_test)
        self.test_judgements = load_judgements(self.test_queries, self.documents, raw_qrels_test)

        self.train_queries = load_queries(raw_queries_train)
        self.train_judgements = load_judgements(self.train_queries, self.documents, raw_qrels_train)

        self.dev_queries = load_queries(raw_queries_dev)
        self.dev_judgements = load_judgements(self.dev_queries, self.documents, raw_qrels_dev)

    def test_number_of_documents(self):
        self.assertEqual(NUM_COMBINED_DOCUMENTS, len(self.documents))

    def test_split_size(self):
        print(NUM_COMBINED_TEST_QUERIES, NUM_COMBINED_TRAIN_QUERIES, NUM_COMBINED_DEV_QUERIES, 
              NUM_COMBINED_TEST_JUDGEMENTS, NUM_COMBINED_TRAIN_JUDGEMENTS, NUM_COMBINED_DEV_JUDGEMENTS)
        self.assertEqual(NUM_COMBINED_TEST_QUERIES, len(self.test_queries))
        self.assertEqual(NUM_COMBINED_TRAIN_QUERIES, len(self.train_queries))
        self.assertEqual(NUM_COMBINED_DEV_QUERIES, len(self.dev_queries))

        self.assertEqual(NUM_COMBINED_TEST_JUDGEMENTS, len(self.test_judgements))
        self.assertEqual(NUM_COMBINED_TRAIN_JUDGEMENTS, len(self.train_judgements))
        self.assertEqual(NUM_COMBINED_DEV_JUDGEMENTS, len(self.dev_judgements))