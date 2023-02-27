from typing import Iterable, OrderedDict

from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
from tqdm import tqdm

from ..entities import DocumentBase, QueryBase
from ..irsystem import IRSystemBase
from ..preprocessing.preprocessing import AbsDocPreprocessing


class BoWSystem(IRSystemBase):
    """
    A bag-of-words system

    Parameters
    ----------
    documents: OrderedDict
        Input documents
    preprocessing: AbsDocPreprocessing
        Type of preprocessing

    Attributes
    ----------
    dictionary: Dictionary
        The dictionary of the system.
    index: MatrixSimilarity
        The indexed documents.
    index_to_document: dict of (int, Document)
        A mapping from indexed document numbers to documents.

    """

    def __init__(self, documents: OrderedDict[str, DocumentBase], preprocessing: AbsDocPreprocessing):
        self.preprocessing = preprocessing

        document_bodies = (self.preprocessing(document.body) for document in documents.values())
        document_bodies = tqdm(document_bodies, desc='Building the dictionary', total=len(documents))

        self.dictionary = Dictionary(document_bodies)
        document_vectors = (self._doc2bow(document.body) for document in documents.values())
        document_vectors = tqdm(document_vectors, desc='Building the index', total=len(documents))

        self.index = SparseMatrixSimilarity(document_vectors, num_docs=len(documents), num_terms=len(self.dictionary))
        self.index_to_document = dict(enumerate(documents.values()))

    def _doc2bow(self, doc: str):
        return self.dictionary.doc2bow(self.preprocessing(doc))

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """The ranked retrieval results for a query.

        Parameters
        ----------
        query : Query
            A query.

        Returns
        -------
        iterable of Document
            The ranked retrieval results for a query.

        """
        similarities = enumerate(self.index[self._doc2bow(query.body)])
        sorted_similarities = sorted(similarities, key=lambda item: item[1], reverse=True)

        for document_number, _ in sorted_similarities:
            document = self.index_to_document[document_number]
            yield document
