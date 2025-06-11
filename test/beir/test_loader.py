import unittest

from pv211_utils.beir.loader import (
    load_queries,
    load_documents,
    load_judgements,
    load_beir_datasets,
    split_beir_dataset,
)
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


class TestCombineAndSplit(unittest.TestCase):
    def setUp(self):
        android = RawBeirDataset("android", test=True)
        english = RawBeirDataset("english", test=True)
        gaming = RawBeirDataset("gaming", test=True)
        gis = RawBeirDataset("gis", test=True)
        mathematica = RawBeirDataset("mathematica", test=True)
        physics = RawBeirDataset("physics", test=True)
        programmers = RawBeirDataset("programmers", test=True)
        stats = RawBeirDataset("stats", test=True)
        tex = RawBeirDataset("tex", test=True)
        unix = RawBeirDataset("unix", test=True)
        webmasters = RawBeirDataset("webmasters", test=True)
        wordpress = RawBeirDataset("wordpress", test=True)
        download_location = "datasets"

        # Test loading and combining multiple datasets
        desired_datasets = RawBeirDatasets(
            datasets=[
                android,
                english,
                gaming,
                gis,
                mathematica,
                physics,
                programmers,
                stats,
                tex,
                unix,
                webmasters,
                wordpress,
            ],
            download_location=download_location,
        )
        _, _, raw_test_data = load_beir_datasets(desired_datasets)

        # Test splitting the dataset
        # Leave 90% for training and 10% for validation and testing
        raw_train_data, raw_test_data = split_beir_dataset(
            raw_test_data, split_factor=0.9
        )
        # Subsequently split this into 5% for validation and 5% for testing
        raw_dev_data, raw_train_data = split_beir_dataset(
            raw_train_data, split_factor=0.5
        )

        raw_corpus_test = list(raw_test_data)[0]
        raw_queries_test = list(raw_test_data)[1]
        raw_qrels_test = list(raw_test_data)[2]

        raw_queries_train = list(raw_train_data)[1]
        raw_qrels_train = list(raw_train_data)[2]

        raw_queries_dev = list(raw_dev_data)[1]
        raw_qrels_dev = list(raw_dev_data)[2]

        self.documents = load_documents(raw_corpus_test)
        self.test_queries = load_queries(raw_queries_test)
        self.test_judgements = load_judgements(
            self.test_queries, self.documents, raw_qrels_test
        )

        self.train_queries = load_queries(raw_queries_train)
        self.train_judgements = load_judgements(
            self.train_queries, self.documents, raw_qrels_train
        )

        self.dev_queries = load_queries(raw_queries_dev)
        self.dev_judgements = load_judgements(
            self.dev_queries, self.documents, raw_qrels_dev
        )

        self.document = self.documents["1"]

    def test_number_of_documents(self):
        self.assertEqual(NUM_COMBINED_DOCUMENTS, len(self.documents))

    def test_document_body(self):
        body_begining_str = (
            "I am playing around with my brand new Motorola Defy"
            " and trying to find a way to manage my contacts."
        )
        self.assertTrue(self.document.body.startswith(body_begining_str))
        self.assertTrue(
            self.document.body.endswith("Does anyone have a solution for me ?")
        )

    def test_split_size(self):
        self.assertTrue(NUM_COMBINED_TEST_QUERIES, len(self.test_queries))
        self.assertTrue(NUM_COMBINED_TRAIN_QUERIES, len(self.train_queries))
        self.assertTrue(NUM_COMBINED_DEV_QUERIES, len(self.dev_queries))

        self.assertTrue(NUM_COMBINED_TEST_JUDGEMENTS, len(self.test_judgements))
        self.assertTrue(NUM_COMBINED_TRAIN_JUDGEMENTS, len(self.train_judgements))
        self.assertTrue(NUM_COMBINED_DEV_JUDGEMENTS, len(self.dev_judgements))
