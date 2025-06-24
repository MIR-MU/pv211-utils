from typing import Iterable, OrderedDict

from rank_bm25 import BM25Plus

from ..entities import DocumentBase, QueryBase
from ..irsystem import IRSystemBase
from ..preprocessing import DocPreprocessingBase


class BM25PlusSystem(IRSystemBase):
    """
    Class for BM25+ ranking system. BM25+ is extension of BM25 - bag-of-words retrieval function that ranks a set of
    documents based on the query terms appearing in each document, regardless of their proximity within the document.

    Parameters
    ----------
    documents: OrderedDict
        Input documents
    k1: float
        BM25 k1 parameter. k1 is a variable which helps determine term frequency saturation characteristics.
    b: float
        BM25 b parameter. With bigger b, the effects of the length of the document compared to the average
        length are more amplified.
    d: float
        BM25 d parameter. Delta parameter for BM25+.

    Attributes
    ----------
    bm25: BM25PlusCore
        Ranking model
    index: dict of (int, Document)
        A mapping from indexed document numbers to documents.

    """

    def __init__(
        self,
        documents: OrderedDict[str, DocumentBase],
        preprocessing: DocPreprocessingBase,
        k1: float = 1.25,
        b: float = 0.75,
        d: float = 1,
    ):
        self.preprocessing = preprocessing

        docs_values = documents.values()

        corpus = [self.preprocessing(str(document)) for document in docs_values]

        self.bm25 = BM25Plus(corpus, k1=k1, b=b, delta=d)
        self.index = dict(enumerate(docs_values))

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """
        yield best docs by relevace

        Parameters
        ----------
        query: QueryBase
        """
        query = self.preprocessing(str(query))

        # score and rank docs by their relevance
        docs = self.bm25.get_scores(query).argsort()[::-1]

        for doc in docs:
            yield self.index[doc]
