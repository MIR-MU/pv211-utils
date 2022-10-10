from typing import Iterable, OrderedDict

from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
from gensim.utils import simple_preprocess
from tqdm import tqdm

from ..entities import DocumentBase, QueryBase
from ..irsystem import IRSystemBase


class BoWSystem(IRSystemBase):
    """
    A bag-of-words system

    Parameters
    ----------
    documents: OrderedDict
        Input documents

    Attributes
    ----------
    dictionary: Dictionary
        The dictionary of the system.
    index: MatrixSimilarity
        The indexed documents.
    index_to_document: dict of (int, Document)
        A mapping from indexed document numbers to documents.

    """

    def __init__(self, documents: OrderedDict[str, DocumentBase]):
        document_bodies = (simple_preprocess(document.body) for document in documents.values())
        document_bodies = tqdm(document_bodies, desc='Building the dictionary', total=len(documents))

        dictionary = Dictionary(document_bodies)
        document_vectors = (dictionary.doc2bow(simple_preprocess(document.body)) for document in documents.values())
        document_vectors = tqdm(document_vectors, desc='Building the index', total=len(documents))

        index = SparseMatrixSimilarity(document_vectors, num_docs=len(documents), num_terms=len(dictionary))
        index_to_document = dict(enumerate(documents.values()))

        self.dictionary = dictionary
        self.index = index
        self.index_to_document = index_to_document

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
        query_vector = self.dictionary.doc2bow(simple_preprocess(query.body))
        similarities = enumerate(self.index[query_vector])
        sorted_similarities = sorted(similarities, key=lambda item: item[1], reverse=True)

        for document_number, _ in sorted_similarities:
            document = self.index_to_document[document_number]
            yield document
