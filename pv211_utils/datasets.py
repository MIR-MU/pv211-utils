"""The dataset module provides interfaces for loading
and splitting Arqmath, Cranfield, Trec, and Beir datasets.

Classes:
-------
ArqmathDataset
    Interface for Arqmath dataset.
CranfieldDataset
    Interface for Cranfield dataset.
TrecDataset
    Interface for Trec dataset.
BeirDataset
    Interface for Beir dataset.
"""
from .arqmath import loader as arqmath_loader
from .arqmath.loader import ArqmathJudgements
from .cranfield import loader as cranfield_loader
from .cranfield.loader import CranfieldJudgements
from .trec.loader import TrecJudgements
from .trec import loader as trec_loader
from .beir import loader as beir_loader
from .beir.loader import BeirJudgementsBase
from .query_ordering import ARQMATH_QUERIES, CRANFIELD_QUERIES

from beir.datasets.data_loader import GenericDataLoader
from collections import OrderedDict
from pathlib import Path
from functools import reduce
from enum import Enum


def _check_split_size_interval(split_size: float) -> None:
    if not 0 <= split_size <= 1:
        raise ValueError(
            "split proportion has to be between 0 and 1")


def _check_year(year: int) -> None:
    if year not in {2020, 2021, 2022}:
        raise ValueError("year has to be either 2020, 2021, or 2022")


def _check_beir_dataset_path(path: Path, name: str) -> bool:
    path = path / name
    all_paths = [
        path / "corpus.jsonl",
        path / "queries.jsonl",
        path / "qrels" / "test.tsv",
    ]

    if name in beir_loader.HAVE_TRAIN:
        all_paths.append(path / "qrels" / "train.tsv")
    if name in beir_loader.HAVE_DEV:
        if name == "msmarco-v2":
            all_paths.append(path / "qrels" / "dev1.tsv")
            all_paths.append(path / "qrels" / "dev2.tsv")
        else:
            all_paths.append(path / "qrels" / "dev.tsv")

    # True iff every needed file exists
    return reduce(lambda a, b: a and b.exists(), all_paths, True)


def _check_beir_datatset_name(name: str) -> None:
    if name not in beir_loader.AVAILABLE_DATASETS:
        raise ValueError("dataset with given name is not available")


class Split(Enum):
    train = 0
    validation = 1
    test = 2


class ArqmathDataset():
    """Class to provide interface to load and split Arqmath dataset.

    Attributes:
    ----------
    year : int
        Year from which the queries and judgements for testing are loaded.
    text_format : str
        Format of the text in queries, answers, and questions.
    validation_split_size : float
        Proportion of the train dataset to include in the validation split.
    """

    def __init__(
            self,
            year: int,
            text_format: str,
            validation_split_size: float = 0.2) -> None:
        """Check if arguments have legal values and construct attributes
        for ArqmathDataset object.

        Args:
        ----
        year : int
            Year from which the queries and judgements for testing
            are loaded.
        text_format : str
            Format of the text in queries, answers, and questions.
        validation_split_size : float, optional
            Proportion of the train dataset to include in the validation
            split. Defaults to 0.2.
        """
        _check_year(year)
        arqmath_loader._check_text_format(text_format)
        _check_split_size_interval(validation_split_size)

        self.year = year
        self.text_format = text_format
        self.validatoin_split_size = validation_split_size

    def _get_split(self, year: int, split: Split) -> OrderedDict:
        queries = arqmath_loader.load_queries(
            text_format=self.text_format,
            year=year)
        queries_partition = []
        validation_size = int(self.validatoin_split_size * len(queries))

        if split == Split.train:
            split_interval = range(validation_size, len(queries))
        else:  # split = Split.validation
            split_interval = range(validation_size)

        for i in split_interval:
            ith_query_id = ARQMATH_QUERIES[year][i]
            queries_partition.append((ith_query_id, queries[ith_query_id]))

        return OrderedDict(queries_partition)

    def _load_judgements(self, year: int) -> ArqmathJudgements:
        return arqmath_loader.load_judgements(
            queries=arqmath_loader.load_queries(
                text_format=self.text_format,
                year=year),
            answers=self.load_answers(),
            year=year)

    def set_year(self, new_year: int) -> None:
        """Change the year attribute ArqmathDataset object.

        Args:
        ----
        new_year : int
            A new value of the year attribute.
        """
        self.year = new_year

    def set_text_format(self, new_text_format: str) -> None:
        """Change the text_format attribute ArqmathDataset object.

        Args:
        ----
        new_text_format : str
            A new value of the text_format attribute.
        """
        arqmath_loader._check_text_format(new_text_format)
        self.text_format = new_text_format

    def set_validation_split_size(self, new_proportion: float) -> None:
        """Change the validation_split_size attribute ArqmathDataset object.

        Args:
        ----
        validation_split_size : float
            A new value of the validation_split_size attribute.
        """
        _check_split_size_interval(new_proportion)
        self.validatoin_split_size = new_proportion

    def load_test_queries(self) -> OrderedDict:
        """Load the test split of queries,
        i.e. queries from the year specified as the attribute.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return arqmath_loader.load_queries(
            text_format=self.text_format,
            year=self.year)

    def load_train_queries(self) -> OrderedDict:
        """Load the train split of queries, i.e. all the queries from
        all the years beside the one specified as the atribute, excluding
        validation split.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        year1, year2 = {2020, 2021, 2022} - {self.year}

        return OrderedDict(
            self._get_split(year1, Split.train),
            **self._get_split(year2, Split.train))

    def load_validation_queries(self) -> OrderedDict:
        """Load the validation split of queries, i.e. all the queries from
        all the years beside the one specifiet as the atribute, excluding
        train split.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        year1, year2 = {2020, 2021, 2022} - {self.year}

        return OrderedDict(
            self._get_split(year1, Split.validation),
            **self._get_split(year2, Split.validation))

    def load_test_judgements(self) -> ArqmathJudgements:
        """Load judgements for test queries.

        Returns:
        -------
        ArqmathJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        return self._load_judgements(self.year)

    def load_train_judgements(self) -> ArqmathJudgements:
        """Load judgements for train queries.

        Returns:
        -------
        ArqmathJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        year1, year2 = {2020, 2021, 2022} - {self.year}
        return {(q, a)
                for q, a in self._load_judgements(year1).union(
                    self._load_judgements(year2))
                if q.query_id in self.load_train_queries().keys()}

    def load_validation_judgements(self) -> ArqmathJudgements:
        """Load judgements for validation queries.

        Returns:
        -------
        ArqmathJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        year1, year2 = {2020, 2021, 2022} - {self.year}
        return {(q, a)
                for q, a in self._load_judgements(year1).union(
                    self._load_judgements(year2))
                if q.query_id in self.load_validation_queries().keys()}

    def load_answers(self) -> OrderedDict:
        """Load answers.

        Returns:
        -------
        OrderedDict
            Dictionary of (document_id: Answer) form.
        """
        return arqmath_loader.load_answers(text_format=self.text_format)

    def load_questions(self) -> OrderedDict:
        """Load questions.

        Returns:
        -------
        OrderedDict
            Dictionary of (document_id: Question) form.
        """
        return arqmath_loader.load_questions(
            text_format=self.text_format,
            answers=self.load_answers())


class CranfieldDataset():
    """Class to provide interface to load and split Arqmath dataset.

    Attributes:
    ----------
    test_split_size : float
        Proportion of the dataset to include in the test split.
    validation_split_size : float
        Proportion of the train dataset to include in the validation split.
    """

    def __init__(self, test_split_size: float = 1,
                 validation_split_size: float = 0) -> None:
        """Check if arguments have legal values and construct attributes
        for CranfieldDataset object.

        Args:
        ----
        test_split_size : float, optional
            Proportion of the dataset to include in the test split.
            Defaults to 1.
        validation_split_size : float, optional
            Proportion of the train dataset to include in the validation
            split. Defaults to 0.
        """
        _check_split_size_interval(test_split_size)
        _check_split_size_interval(validation_split_size)
        self.test_split_size = test_split_size
        self.validation_split_size = validation_split_size

    def _get_split(self, split: Split) -> OrderedDict:
        queries = cranfield_loader.load_queries()
        queries_partition = []
        test_size = int(self.test_split_size * len(queries))
        validation_size = int(self.validation_split_size
                              * (len(queries) - test_size))

        if split == Split.test:
            split_interval = range(test_size)
        elif split == Split.validation:
            split_interval = range(test_size, test_size + validation_size)
        else:  # split = Split.train
            split_interval = range(test_size + validation_size, len(queries))

        for i in split_interval:
            ith_query_id = CRANFIELD_QUERIES[i]
            queries_partition.append((ith_query_id, queries[ith_query_id]))

        return OrderedDict(queries_partition)

    def _load_judgements(self) -> CranfieldJudgements:
        return cranfield_loader.load_judgements(
            cranfield_loader.load_queries(),
            cranfield_loader.load_documents()
        )

    def set_test_split_size(self, new_size: float) -> None:
        """Change the test_split_size attribute CranfieldDataset object.

        Args:
        ----
        validation_split_size : float
            A new value of the test_split_size attribute.
        """
        self.test_split_size = new_size

    def set_validation_split_size(self, new_size: float) -> None:
        """Change the validation_split_size attribute CranfieldDataset
        object.

        Args:
        ----
        validation_split_size : float
            A new value of the validation_split_size attribute.
        """
        self.validation_split_size = new_size

    def load_test_queries(self) -> OrderedDict:
        """Load the test split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return self._get_split(Split.test)

    def load_train_queries(self) -> OrderedDict:
        """Load the train split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return self._get_split(Split.train)

    def load_validation_queries(self) -> OrderedDict:
        """Load the validation split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return self._get_split(Split.validation)

    def load_test_judgements(self) -> CranfieldJudgements:
        """Load judgements for test queries.

        Returns:
        -------
        CranfieldJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        return {(q, a)
                for q, a in self._load_judgements()
                if q.query_id in self.load_test_queries().keys()}

    def load_train_judgements(self) -> CranfieldJudgements:
        """Load judgements for train queries.

        Returns:
        -------
        CranfieldJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        return {(q, a)
                for q, a in self._load_judgements()
                if q.query_id in self.load_train_queries().keys()}

    def load_validation_judgements(self) -> CranfieldJudgements:
        """Load judgements for validaiton queries.

        Returns:
        -------
        CranfieldJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        return {(q, a)
                for q, a in self._load_judgements()
                if q.query_id in self.load_validation_queries().keys()}

    def load_documents(self) -> OrderedDict:
        """Load documents.

        Returns:
        -------
        OrderedDict
            Dictionary of (document_id: Document) form.
        """
        return cranfield_loader.load_documents()


class TrecDataset():
    """Class to provide interface to load and split Trec dataset.

    Attributes:
    ----------
    validation_split_size : float
        Proportion of the train dataset to include in the validation split.
    """

    def __init__(self, validation_split_size: float = 0.2) -> None:
        """Check if arguments have legal values and construct attributes
        for TrecDataset object.

        Args:
        ----
        validation_split_size : float, optional
            Proportion of the train dataset to include in the validation
            split. Defaults to 0.2.
        """
        _check_split_size_interval(validation_split_size)
        self.validation_split_size = validation_split_size

    def _get_train_validation_queries(self) -> list:
        return (
            list(trec_loader.load_queries(subset="train").items())
            + list(trec_loader.load_queries(subset="validation").items())
        )

    def set_validation_split_size(self, new_size: float) -> None:
        """Change the validation_split_size attribute TrecDataset object.

        Args:
        ----
        validation_split_size : float
            A new value of the validation_split_size attribute.
        """
        _check_split_size_interval(new_size)
        self.validation_split_size = new_size

    def load_test_queries(self) -> OrderedDict:
        """Load the test split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return trec_loader.load_queries(subset="test")

    def load_train_queries(self) -> OrderedDict:
        """Load the train split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        test_validate_queries = self._get_train_validation_queries()
        return OrderedDict(
            test_validate_queries[:int(len(test_validate_queries)
                                       * (1 - self.validation_split_size))]
        )

    def load_validation_queries(self) -> OrderedDict:
        """Load the validation split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        test_validate_queries = self._get_train_validation_queries()
        return OrderedDict(
            test_validate_queries[int(len(test_validate_queries)
                                      * (1 - self.validation_split_size)):]
        )

    def load_test_judgements(self) -> TrecJudgements:
        """Load judgements for test queries.

        Returns:
        -------
        TrecJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        return trec_loader.load_judgements(self.load_test_queries(),
                                           self.load_documents(),
                                           subset="test")

    def load_train_judgements(self) -> TrecJudgements:
        """Load judgements for train queries.

        Returns:
        -------
        TrecJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        documents = self.load_documents()
        return {(q, a)
                for q, a in trec_loader.load_judgements(self.load_train_queries(),
                                                        documents,
                                                        subset="train").union(
                    trec_loader.load_judgements(self.load_validation_queries(),
                                                documents,
                                                subset="validation"))
                if q.query_id in self.load_train_queries().keys()}

    def load_validation_judgements(self) -> TrecJudgements:
        """Load judgements for validation queries.

        Returns:
        -------
        TrecJudgements
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        documents = self.load_documents()
        return {(q, a)
                for q, a in trec_loader.load_judgements(self.load_train_queries(),
                                                        documents,
                                                        subset="train").union(
                    trec_loader.load_judgements(self.load_validation_queries(),
                                                documents,
                                                subset="validation"))
                if q.query_id in self.load_validation_queries().keys()}

    def load_documents(self) -> OrderedDict:
        """Load documents.

        Returns:
        -------
        OrderedDict
            Dictionary of (document_id: Document) form.
        """
        return trec_loader.load_documents()


class BeirDataset():
    """Class to provide interface to load and split Beir datasets.
    Possible options - "msmarco", "msmarco-v2", "trec-covid",
                       "nfcorpus", "nq", "hotpotqa", "fiqa", "arguana",
                       "webis-touche2020", "quora", "dbpedia-entity",
                       "scidocs", "fever", "climate-fever", "scifact"

    Attributes:
    ----------
    dataset_name : str
        Name of the dataset to be loaded.
    """

    _download_path = Path.home() / '.cache' / 'pv211-utils'

    def __init__(self, dataset_name: str) -> None:
        """Check if arguments have legal values and construct attributes
        for BeirDataset object.

        Args:
        ----
        dataset_name : str
            Name of the dataset to be loaded.
        """
        _check_beir_datatset_name(dataset_name)
        self.dataset_name = dataset_name
        if not _check_beir_dataset_path(self._download_path,
                                        self.dataset_name):
            self._download_path = Path(
                beir_loader.download_beir_dataset(self.dataset_name,
                                                  str(self._download_path)))
        else:
            self._download_path = self._download_path / self.dataset_name

    def set_dataset_name(self, new_dataset_name: str) -> None:
        """Choose a different dataset to be loaded.

        Args:
        ----
        new_dataset_name : str
            Name of the new dataset to be loaded.
        """
        _check_beir_datatset_name(new_dataset_name)
        self.dataset_name = new_dataset_name
        if not _check_beir_dataset_path(self._download_path,
                                        self.dataset_name):
            self._download_path = Path(
                beir_loader.download_beir_dataset(self.dataset_name,
                                                  str(self._download_path)))
        else:
            self._download_path = Path.home() / '.cache' / 'pv211-utils' / self.dataset_name

    def load_test_queries(self) -> OrderedDict:
        """Load the test split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return beir_loader.load_queries(
            beir_loader.load_beir_test_set(self.dataset_name,
                                           str(self._download_path))[1]
        )

    def load_train_queries(self) -> OrderedDict:
        """Load the train split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return beir_loader.load_queries(
            beir_loader.load_beir_train_set(self.dataset_name,
                                            str(self._download_path))[1]
        )

    def load_validation_queries(self) -> OrderedDict:
        """Load the validation split of queries.

        Returns:
        -------
        OrderedDict
            Dictionary of test queries in (query_id: Query) form.
        """
        return beir_loader.load_queries(
            beir_loader.load_beir_dev_set(self.dataset_name,
                                          str(self._download_path))[1]
        )

    def load_test_judgements(self) -> BeirJudgementsBase:
        """Load judgements for test queries.

        Returns:
        -------
        BeirJudgementsBase
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        documents, queries, judgements = beir_loader.load_beir_test_set(
            self.dataset_name, str(self._download_path))
        return beir_loader.load_judgements(beir_loader.load_queries(queries),
                                           beir_loader.load_documents(documents),
                                           judgements)

    def load_train_judgements(self) -> BeirJudgementsBase:
        """Load judgements for train queries.

        Returns:
        -------
        BeirJudgementsBase
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        documents, queries, judgements = beir_loader.load_beir_train_set(
            self.dataset_name, str(self._download_path))
        return beir_loader.load_judgements(beir_loader.load_queries(queries),
                                           beir_loader.load_documents(documents),
                                           judgements)

    def load_validation_judgements(self) -> BeirJudgementsBase:
        """Load judgements for validation queries.

        Returns:
        -------
        BeirJudgementsBase
            Set of (Query, Answer) pairs, where Anwser is judged
            as relevant to the Query.
        """
        documents, queries, judgements = beir_loader.load_beir_dev_set(
            self.dataset_name, str(self._download_path))
        return beir_loader.load_judgements(beir_loader.load_queries(queries),
                                           beir_loader.load_documents(documents),
                                           judgements)

    def load_documents(self) -> OrderedDict:
        """Load documents.

        Returns:
        -------
        OrderedDict
            Dictionary of (document_id: Document) form.
        """
        return beir_loader.load_documents(
            GenericDataLoader(data_folder=self._download_path).load_corpus()
        )