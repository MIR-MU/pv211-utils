
import random

from collections import OrderedDict
from typing import Optional
from beir import util
from beir.datasets.data_loader import GenericDataLoader
from sklearn.model_selection import train_test_split

from .entities import BeirQueryBase, BeirDocumentBase, BeirJudgementsBase, RawBeirDatasets

AVAILABLE_DATASETS = {"msmarco", "msmarco-v2", "trec-covid", "nfcorpus", "nq", "hotpotqa", "fiqa", "arguana",
                      "webis-touche2020", "quora", "dbpedia-entity", "scidocs", "fever", "climate-fever", "scifact"}

CQADUPSTACK = {"android", "english", "gaming", "gis", "mathematica", "physics", "programmers", "stats", "tex", "unix",
               "webmasters", "wordpress"}
HAVE_TRAIN = {"msmarco", "msmarco-v2", "nfcorpus", "nq", "hotpotqa", "fiqa", "fever", "scifact"}
HAVE_TEST = {"msmarco", "trec-covid", "nfcorpus", "nq", "hotpotqa", "fiqa", "arguana", "webis-touche2020", "quora",
             "dbpedia-entity", "scidocs", "fever", "climate-fever", "scifact", "android", "english", "gaming", "gis",
             "mathematica", "physics", "programmers", "stats", "tex", "unix", "webmasters", "wordpress"}
HAVE_DEV = {"msmarco", "msmarco-v2", "nfcorpus", "hotpotqa", "fiqa", "quora", "dbpedia-entity", "fever"}

DEFAULT_DOWNLOAD_LOCATION = "datasets/cqadupstack"


def download_beir_dataset(dataset_name: str, file_location: str) -> str:
    """A Generic BEIR dataset downloader.

        Parameters
        ----------
        dataset_name : str
            A string with the name of a BEIR dataset - should be one of the names from the lists above.
        file_location : str
            Location of the folder where data is to be stored.
    """
    # cqadupstack is a specific case where the dataset is split into multiple subsets with specific topic
    if dataset_name in CQADUPSTACK:
        url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/cqadupstack.zip"
        data_path = util.download_and_unzip(url, file_location)
        data_path = data_path + "/" + dataset_name
    else:
        url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset_name)
        data_path = util.download_and_unzip(url, file_location)
    # nq train set is in a separate file
    if dataset_name == "nq":
        url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nq-train.zip"
        util.download_and_unzip(url, file_location)
    return data_path


def load_beir_test_set(dataset_name: str, data_path: str, alternative: Optional[str] = None):
    if dataset_name not in HAVE_TEST:  # currently only dataset that does not include test is msmarco-v2
        print("Your chosen dataset ", dataset_name, " does not have a test subset.")
        if alternative is None:
            print(
                "You may select a alternative subset, such as the dev2 for msmarco-v2, or split some other subset "
                "into your desired parts using the split_BEIR_dataset.")
            return None, None, None
        if alternative in ["train"]:
            print("You have chosen the training set for testing, please reconsider or at least split it with "
                  "split_BEIR_dataset.")
            return load_beir_train_set(dataset_name, data_path)
        elif alternative in ["dev", "dev1", "dev2"]:
            print("You have chosen ", alternative, "as your alternative, split it with split_BEIR_dataset if you want "
                                                   "to have both ",
                  alternative, " and test set.")
            return load_beir_dev_set(dataset_name, data_path)
        else:
            print("The selected alternative ", alternative, " is not viable, please use train, dev, dev1, dev2")
            return None, None, None
    else:
        return GenericDataLoader(data_folder=data_path).load(split="test")


def load_beir_train_set(dataset_name: str, data_path: str, alternative: Optional[str] = None):
    if dataset_name not in HAVE_TRAIN:
        print("Your chosen dataset ", dataset_name, " does not have a train subset.")
        if alternative is None:
            print(
                "You may select a alternative subset, such as the dev for dbpedia-entity, or split some other subset "
                "into your desired parts using the split_BEIR_dataset.")
            return None, None, None
        if alternative in ["test"]:
            print("You have chosen the testing set for training, please reconsider or at least split it with "
                  "split_BEIR_dataset.")
            return load_beir_test_set(dataset_name, data_path)
        elif alternative in ["dev", "dev1", "dev2"]:
            print("You have chosen ", alternative, "as your alternative, split it with split_BEIR_dataset if you want "
                                                   "to have both ",
                  alternative, " and train set.")
            return load_beir_dev_set(dataset_name, data_path)
        else:
            print("The selected alternative ", alternative, " is not viable, please use test, dev, dev1, dev2")
            return None, None, None
    elif dataset_name == "nq":
        return GenericDataLoader(data_folder=data_path + "-train").load(split="train")
    else:
        return GenericDataLoader(data_folder=data_path).load(split="train")


def load_beir_dev_set(dataset_name: str, data_path: str, alternative: Optional[str] = None):
    if dataset_name not in HAVE_DEV:
        print("Your chosen dataset ", dataset_name, " does not have a dev subset.")
        if alternative is None:
            print(
                "You may select a alternative subset, or split some other subset into your desired parts using the "
                "split_BEIR_dataset.")
            return None, None, None
        if alternative in ["test"]:
            print("You have chosen the dev set for training, please reconsider or at least split it with "
                  "split_BEIR_dataset.")
            return load_beir_test_set(dataset_name, data_path)
        elif alternative in ["train"]:
            print("You have chosen ", alternative, "as your alternative, split it with split_BEIR_dataset if you want "
                                                   "to have both ",
                  alternative, " and train set.")
            return load_beir_dev_set(dataset_name, data_path)
        else:
            print("The selected alternative ", alternative, " is not viable, please use test, dev, dev1, dev2")
            return None, None, None
    if dataset_name == "msmarco-v2":
        if alternative is None:
            print(
                "The selected dataset, msmarco-v2, has two dev subsets. By default the dev1 subset is used, "
                "you can choose the dev2 by setting the alternative parameter.")
            return GenericDataLoader(data_folder=data_path).load(split="dev1")
        elif alternative == "dev1":
            return GenericDataLoader(data_folder=data_path).load(split="dev1")
        elif alternative == "dev2":
            print("The selected dataset, msmarco-v2, has two dev subsets. You have selected the dev2 subset.")
            return GenericDataLoader(data_folder=data_path).load(split="dev2")
        else:
            print("With this msmarco-v2 dataset please use either None, dev1 or de2 alternative")
            return None, None, None
    else:
        return GenericDataLoader(data_folder=data_path).load(split="dev")


def combine_beir_datasets(raw_data1, raw_data2):
    """
    if raw_data1 is None or list(raw_data1)[0] is None:
        return raw_data2
    if raw_data2 is None or list(raw_data2)[0] is None:
        return raw_data1
    """
    if raw_data1 is None:
        raw_data1 = [{}, {}, {}]
    raw_data1, raw_data2 = list(raw_data1), list(raw_data2)
    corpus1, queries1, qrels1 = raw_data1
    corpus2, queries2, qrels2 = raw_data2
    # Combining dictionaries into one and adding the hash of the values to resolve collisions
    # Corpus
    corpus_collisions = {}
    combined_corpus = corpus1
    if combined_corpus:
        last_key = max(map(lambda x: int(x), list(combined_corpus.keys())))
    else:
        last_key = 0

    for i, item in enumerate(corpus2.items()):
        key = str(i + last_key)
        """
        if key in corpus1.keys():
            hashed = str(abs(hash(item[1]["text"])))
            corpus_collisions[key] = hashed
            key = hashed
        """
        corpus_collisions[item[0]] = key
        combined_corpus[key] = item[1]

    # Queries
    query_collisions = {}
    combined_queries = queries1

    if combined_queries:
        last_key = max(map(lambda x: int(x), list(combined_queries.keys())))
    else:
        last_key = 0

    for i, item in enumerate(queries2.items()):
        key = str(i + last_key)
        """
        if key in queries1.keys():
            hashed = str(abs(hash(item[1])))
            query_collisions[key] = hashed
            key = hashed
        """
        query_collisions[item[0]] = key
        combined_queries[key] = item[1]

    # Judgements
    combined_qrels = qrels1
    for item in qrels2.items():
        key = item[0]
        values_dict = item[1]
        new_values_dict = {}

        key = query_collisions[key]
        colision_resolving = []

        for value_key in values_dict.keys():
            new_key = corpus_collisions[value_key]
            colision_resolving.append((new_key, value_key))
        for new_key, old_key in colision_resolving:
            new_values_dict[new_key] = values_dict[old_key]

        combined_qrels[key] = new_values_dict

    return combined_corpus, combined_queries, combined_qrels


def split_beir_dataset(raw_data, split_factor=0.2):
    raw_data = list(raw_data)
    queries1, queries2 = train_test_split(list(raw_data[1].items()), test_size=split_factor, random_state=42)
    queries1, queries2 = OrderedDict(queries1), OrderedDict(queries2)
    raw_data1 = (raw_data[0], queries1, raw_data[2])
    raw_data2 = (raw_data[0], queries2, raw_data[2])
    return raw_data1, raw_data2


def load_beir_datasets(datasets_data: RawBeirDatasets):
    raw_train_data = None
    raw_dev_data = None
    raw_test_data = None
    datasets_data.datasets.sort(key=lambda x: x.name)
    for dataset in datasets_data.datasets:
        # in case a download location is None assume that data is already present in the folder indicated by data_path
        if datasets_data.download_location is None:
            data_path = DEFAULT_DOWNLOAD_LOCATION + "/" + dataset.name
        else:
            location = datasets_data.download_location
            data_path = download_beir_dataset(dataset.name, location)

        # now load each individual data subset
        if dataset.train:
            temp_train_data = load_beir_train_set(dataset.name, data_path, dataset.train_alternative)
            raw_train_data = combine_beir_datasets(raw_train_data, temp_train_data)
        if dataset.dev:
            temp_dev_data = load_beir_dev_set(dataset.name, data_path, dataset.dev_alternative)
            raw_dev_data = combine_beir_datasets(raw_dev_data, temp_dev_data)
        if dataset.test:
            temp_test_data = load_beir_test_set(dataset.name, data_path, dataset.test_alternative)
            raw_test_data = combine_beir_datasets(raw_test_data, temp_test_data)
    return raw_train_data, raw_dev_data, raw_test_data


def load_queries(raw_queries, max_test_queries: Optional[int] = None, query_class=BeirQueryBase) -> OrderedDict:
    queries = OrderedDict()
    if max_test_queries is None:
        max_test_queries = 99967454511  # the entire Big Smoke's order is close enough to infinity
    for que in list(raw_queries.items())[:max_test_queries]:
        que_id = que[0]
        query = query_class(
            query_id=que_id,
            body=que[1],
        )
        queries[que_id] = query
    return queries


def load_documents(raw_corpus, document_class=BeirDocumentBase) -> OrderedDict:
    from collections import OrderedDict
    documents = OrderedDict()
    for doc in raw_corpus.items():
        doc_id = doc[0]
        document = document_class(
            document_id=doc_id,
            body=doc[1]["text"]
        )
        documents[doc_id] = document
    return documents


def load_judgements(queries: OrderedDict, raw_documents: OrderedDict, raw_qrels) -> BeirJudgementsBase:
    judgements = set()
    for que_id in queries.keys():

        for doc_id in (list(raw_qrels[que_id].keys())):
            query: BeirQueryBase = queries[que_id]
            document: BeirDocumentBase = raw_documents[doc_id]
            relevance = (query, document)
            judgements.add(relevance)
    return judgements


def create_false_judgements(documents: OrderedDict, queries: OrderedDict, judgements: BeirJudgementsBase,
                            num_of_false_judgements: int = 10000) -> BeirJudgementsBase:

    false_judgements = set()
    seed = 42
    randomizer = random.Random(seed)
    random.seed(42)

    doc_ids = list(documents.keys())
    que_ids = list(queries.keys())

    for _ in range(num_of_false_judgements):
        que_id = randomizer.choice(que_ids)
        doc_id = randomizer.choice(doc_ids)
        query: BeirQueryBase = queries[que_id]
        document: BeirDocumentBase = documents[doc_id]
        relevance = (query, document)

        while relevance in judgements or relevance in false_judgements:
            que_id = randomizer.choice(que_ids)
            doc_id = randomizer.choice(doc_ids)
            query: BeirQueryBase = queries[que_id]
            document: BeirDocumentBase = documents[doc_id]
            relevance = (query, document)
        false_judgements.add(relevance)
    return false_judgements
