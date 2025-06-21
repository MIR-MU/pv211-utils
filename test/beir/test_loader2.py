import unittest

from pv211_utils.beir.loader import (
    load_queries,
    load_documents,
    load_judgements,
    load_beir_datasets,
    split_beir_dataset,
)
from pv211_utils.beir.entities import RawBeirDataset, RawBeirDatasets

# TODO: Adjust these constants for a single dataset from the second half, e.g., 'programmers'
NUM_QUERIES = 0  # UPDATE THIS
NUM_DOCUMENTS = 0  # UPDATE THIS
NUM_JUDGEMENTS = 0  # UPDATE THIS

# TODO: Update these example IDs and bodies for the chosen single dataset
SINGLE_TEST_QUERY_ID = "some_query_id"  # UPDATE THIS
SINGLE_TEST_QUERY_BODY = "some query body"  # UPDATE THIS
SINGLE_TEST_DOC_ID = "some_doc_id"  # UPDATE THIS
SINGLE_TEST_DOC_BODY_START = "some doc body start"  # UPDATE THIS
SINGLE_TEST_DOC_BODY_END = "some doc body end"  # UPDATE THIS
SINGLE_JUDGEMENT_QUERY_ID = "some_query_id_for_judgement"  # UPDATE THIS
SINGLE_JUDGEMENT_RELEVANT_DOC_ID = "relevant_doc_id"  # UPDATE THIS
SINGLE_JUDGEMENT_IRRELEVANT_DOC_ID = "irrelevant_doc_id"  # UPDATE THIS

# TODO: Adjust these constants for the second half of the datasets (programmers, stats, tex, unix, webmasters, wordpress)
NUM_COMBINED_DOCUMENTS = 0  # UPDATE THIS
NUM_COMBINED_TEST_QUERIES = 0  # UPDATE THIS
NUM_COMBINED_TRAIN_QUERIES = 0  # UPDATE THIS
NUM_COMBINED_DEV_QUERIES = 0  # UPDATE THIS
NUM_COMBINED_TEST_JUDGEMENTS = 0  # UPDATE THIS
NUM_COMBINED_TRAIN_JUDGEMENTS = 0  # UPDATE THIS
NUM_COMBINED_DEV_JUDGEMENTS = 0  # UPDATE THIS


class TestLoadQueries(unittest.TestCase):
    def setUp(self):
        programmers = RawBeirDataset("programmers", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([programmers], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.queries = load_queries(raw_test_data[1])
        if SINGLE_TEST_QUERY_ID in self.queries:
            self.query = self.queries[SINGLE_TEST_QUERY_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES, len(self.queries))

    def test_query_body(self):
        if not hasattr(self, 'query'):
            self.skipTest(f"Query with ID '{SINGLE_TEST_QUERY_ID}' not found.")
        self.assertEqual(SINGLE_TEST_QUERY_BODY, self.query.body)


class TestLoadDocuments(unittest.TestCase):
    def setUp(self):
        programmers = RawBeirDataset("programmers", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([programmers], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.documents = load_documents(raw_test_data[0])
        if SINGLE_TEST_DOC_ID in self.documents:
            self.document = self.documents[SINGLE_TEST_DOC_ID]

    def test_number_of_documents(self):
        self.assertEqual(NUM_DOCUMENTS, len(self.documents))

    def test_document_body(self):
        if not hasattr(self, 'document'):
            self.skipTest(f"Document with ID '{SINGLE_TEST_DOC_ID}' not found.")
        self.assertTrue(self.document.body.startswith(SINGLE_TEST_DOC_BODY_START))
        self.assertTrue(self.document.body.endswith(SINGLE_TEST_DOC_BODY_END))


class TestLoadJudgements(unittest.TestCase):
    def setUp(self):
        programmers = RawBeirDataset("programmers", test=True)
        download_location = "datasets"
        desired_datasets = RawBeirDatasets([programmers], download_location)
        _, _, raw_test_data = load_beir_datasets(desired_datasets)
        self.queries = load_queries(raw_test_data[1])
        self.documents = load_documents(raw_test_data[0])
        self.judgements = load_judgements(self.queries, self.documents, raw_test_data[2])

        if (SINGLE_JUDGEMENT_QUERY_ID in self.queries and
                SINGLE_JUDGEMENT_RELEVANT_DOC_ID in self.documents and
                SINGLE_JUDGEMENT_IRRELEVANT_DOC_ID in self.documents):
            self.query = self.queries[SINGLE_JUDGEMENT_QUERY_ID]
            self.relevant_document = self.documents[SINGLE_JUDGEMENT_RELEVANT_DOC_ID]
            self.irrelevant_document = self.documents[SINGLE_JUDGEMENT_IRRELEVANT_DOC_ID]

    def test_number_of_judgements(self):
        self.assertEqual(NUM_JUDGEMENTS, len(self.judgements))

    def test_judgement_documents(self):
        if not hasattr(self, 'query'):
            self.skipTest("Required queries or documents for judgement test not found.")
        self.assertIn((self.query, self.relevant_document), self.judgements)
        self.assertNotIn((self.query, self.irrelevant_document), self.judgements)


class TestCombineAndSplitPart2(unittest.TestCase):
    def setUp(self):
        # Datasets for the second half
        programmers = RawBeirDataset("programmers", test=True)
        stats = RawBeirDataset("stats", test=True)
        tex = RawBeirDataset("tex", test=True)
        unix = RawBeirDataset("unix", test=True)
        webmasters = RawBeirDataset("webmasters", test=True)
        wordpress = RawBeirDataset("wordpress", test=True)
        download_location = "datasets"

        desired_datasets = RawBeirDatasets(
            datasets=[
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
        self.assertEqual(NUM_COMBINED_TEST_QUERIES, len(self.test_queries))
        self.assertEqual(NUM_COMBINED_TRAIN_QUERIES, len(self.train_queries))
        self.assertEqual(NUM_COMBINED_DEV_QUERIES, len(self.dev_queries))

        self.assertEqual(NUM_COMBINED_TEST_JUDGEMENTS, len(self.test_judgements))
        self.assertEqual(NUM_COMBINED_TRAIN_JUDGEMENTS, len(self.train_judgements))
        self.assertEqual(NUM_COMBINED_DEV_JUDGEMENTS, len(self.dev_judgements))