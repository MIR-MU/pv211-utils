import math
from typing import Iterable, Dict, OrderedDict

import numpy as np

from pv211_utils.entities import QueryBase, DocumentBase
from pv211_utils.irsystem import IRSystemBase


class BM25():
    """
    Class for ranking function
    """

    def __init__(self, corpus: list):
        """
        Parameters
        ----------
        corpus: list
            list of documents
        """
        self.k1 = 1.25
        self.b = 0.75
        self.d = 0.5

        self.corpus = corpus
        self.corpus_len = len(corpus)

        self.doc_lens = [len(d) for d in corpus]
        self.avgdl = sum(self.doc_lens) / len(self.doc_lens)
        self.dfs = self.compute_dfs()

    def compute_dfs(self) -> Dict[str, int]:
        """
        Compute df for every word in corpus

        Returns
        -------
            dictionary where each word has number of documents it occurs in.
        """
        dfs: Dict[str, int] = {}

        for doc in self.corpus:
            doc_set = set(doc)  # remove duplicates in doc
            for word in doc_set:
                if word in dfs:
                    dfs[word] += 1
                else:
                    dfs[word] = 1
        return dfs

    def get_idfs(self, doc: list) -> list:
        """
        get idf for each word in doc

        Parameters
        ----------
        doc: list
            document as list of words
        """
        idfs = []

        for w in doc:
            if w not in self.dfs:
                idfs.append(0)
                continue

            df = self.dfs[w]
            idfs.append(math.log((self.corpus_len - df + .5)/(df + .5) + self.d))
        return idfs

    def __call__(self, query: list) -> np.ndarray:
        """
        Score documents in corpus for a query

        Parameters
        ----------
        query: list
            Preprocessed tokens

        Returns
        -------
            Score for each document in corpus
        """
        scores = np.zeros(self.corpus_len)
        idfs = self.get_idfs(query)

        for i, doc in enumerate(self.corpus):
            L = self.doc_lens[i] / self.avgdl
            # skip empty docs
            if L == 0:
                continue

            # calculate
            K = self.k1 * (1 - self.b + self.b * L)
            for j, qword in enumerate(query):
                tf = doc.count(qword)
                # skip the word that not appear in the doc
                if tf > 0:
                    scores[i] += (tf / (tf + K)) * idfs[j]

        return scores


class BM25System(IRSystemBase):
    """
    A system that returns documents ordered by decreasing cosine similarity.

    Attributes
    ----------
    bm25: BM25
        Ranking model
    index: dict of (int, Document)
        A mapping from indexed document numbers to documents.

    """

    def __init__(self, documents: OrderedDict):
        docs_values = documents.values()

        # preprocess the docs
        corpus = [doc.body.split(" ") for doc in docs_values]

        self.bm25 = BM25(corpus)
        self.index = dict(enumerate(docs_values))

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """
        yield best docs by relevace

        Parameters
        ----------
        query: QueryBase
        """
        query = query.body.split(" ")

        # score and rank docs by their relevance
        docs = self.bm25(query).argsort()[::-1]

        for doc in docs:
            yield self.index[doc]
