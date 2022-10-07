from multiprocessing import get_context
from typing import Iterable, Union, List, Tuple, OrderedDict

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity
from gensim.utils import simple_preprocess
from tqdm import tqdm

from pv211_utils.entities import QueryBase, DocumentBase
from pv211_utils.irsystem import IRSystemBase


class TfidfSystem(IRSystemBase):
    """
    A system that returns documents ordered by decreasing cosine similarity.

    Attributes
    ----------
    dictionary: Dictionary
        The dictionary of the system.
    tfidf_model: TfidfModel
        The TF-IDF model of the system.
    index: MatrixSimilarity
        The indexed TF-IDF documents.
    index_to_document: dict of (int, Document)
        A mapping from indexed document numbers to documents.

    """
    DICTIONARY: Dictionary
    TFIDF_MODEL: TfidfModel

    def __init__(self, documents: OrderedDict[str, DocumentBase]):
        with get_context('fork').Pool(None) as pool:
            document_bodies = pool.imap(self.__class__._document_to_tokens, documents.values())
            document_bodies = tqdm(document_bodies, desc='Building the dictionary', total=len(documents))
            self.dictionary = Dictionary(document_bodies)
            self.__class__.DICTIONARY = self.dictionary

        with get_context('fork').Pool(None) as pool:
            document_vectors = pool.imap(self.__class__._document_to_bag_of_words, documents.values())
            document_vectors = tqdm(document_vectors, desc='Building the TF-IDF model', total=len(documents))
            self.tfidf_model = TfidfModel(document_vectors)
            self.__class__.TFIDF_MODEL = self.tfidf_model

        with get_context('fork').Pool(None) as pool:
            document_vectors = pool.imap(self.__class__._document_to_tfidf_vector, documents.values())
            document_vectors = tqdm(document_vectors, desc='Building the TF-IDF index', total=len(documents))
            self.index = SparseMatrixSimilarity(document_vectors, num_docs=len(
                documents), num_terms=len(self.dictionary))

        del self.__class__.DICTIONARY
        del self.__class__.TFIDF_MODEL

        self.index_to_document = dict(enumerate(documents.values()))

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """The ranked retrieval results for a query.

        Parameters
        ----------
        query : QueryBase
            A query.

        Returns
        -------
        iterable of Document
            The ranked retrieval results for a query.

        """
        self.__class__.DICTIONARY = self.dictionary
        self.__class__.TFIDF_MODEL = self.tfidf_model

        query_vector = self.__class__._document_to_tfidf_vector(query)
        similarities = enumerate(self.index[query_vector])
        similarities = sorted(similarities, key=lambda item: item[1], reverse=True)
        for document_number, _ in similarities:
            document = self.index_to_document[document_number]
            yield document

        del self.__class__.DICTIONARY
        del self.__class__.TFIDF_MODEL

    @classmethod
    def _document_to_tokens(cls, document: Union[QueryBase, DocumentBase]) -> List[str]:
        return simple_preprocess(document.body)

    @classmethod
    def _document_to_bag_of_words(cls, document: Union[QueryBase, DocumentBase]) -> List[Tuple[int, int]]:
        return cls.DICTIONARY.doc2bow(cls._document_to_tokens(document))

    @classmethod
    def _document_to_tfidf_vector(cls, document: Union[QueryBase, DocumentBase]) -> List[Tuple[int, float]]:
        return cls.TFIDF_MODEL[cls._document_to_bag_of_words(document)]
