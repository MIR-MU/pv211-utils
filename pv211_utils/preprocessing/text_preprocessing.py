from abc import ABC, abstractmethod
from gensim.utils import simple_preprocess, deaccent
from typing import List, Optional, Callable

WordNormFunc = Optional[Callable]


class DocPreprocessingBase(ABC):
    @abstractmethod
    def __call__(self, doc: str) -> List[str]:
        raise NotImplementedError()


class NoneDocPreprocessing(DocPreprocessingBase):
    def __call__(self, doc: str) -> List[str]:
        return doc.split(" ")


class LowerDocPreprocessing(DocPreprocessingBase):
    def __call__(self, doc: str) -> List[str]:
        return doc.lower().split(" ")


class SimpleDocPreprocessing(DocPreprocessingBase):
    """Simple document preprocessing

    Attributes
    ----------
    deacc: bool
        if true, accentuation will be removed from input doc
    min_len: int
        All words shorter than min_len will be filtered out
    max_len: int
        All words longer than max_len will be filtered out
    """

    def __init__(self, deacc: bool = False, min_len: int = 2, max_len: int = 15):
        self.deacc = deacc
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, doc: str) -> List[str]:
        """Preprocess input doc

        Parameters
        ----------
        doc: str
            Input document as string

        Returns
        -------
        list of Document
            Processed, lowered and tokenized doc
        """

        return simple_preprocess(doc, self.deacc, self.min_len, self.max_len)


class DocPreprocessing(DocPreprocessingBase):
    """Document preprocessing

    Attributes
    ----------
    deacc: bool
        if true, accentuation will be removed from input doc
    lower: bool
        if true, doc will be lower-cased
    lemm: Optional[Callable[[str]]]
        lemmatize function
    stem: Optional[Callable[[str]]]
        stemming function
    stopwords: List[str]
        stopwords will be removed from doc
    min_len: int
        All words shorter than min_len will be filtered out
    max_len: int
        All words longer than max_len will be filtered out

    """

    def __init__(self, lower: bool = True, deacc: bool = True, lemm: WordNormFunc = None, stem: WordNormFunc = None,
                 stopwords: List[str] = [], min_len: int = 2, max_len: int = 15):

        self.lower = lower
        self.deacc = deacc
        self.lemm = lemm
        self.stem = stem
        self.stopwords = stopwords
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, doc: str) -> List[str]:
        """Preprocess input doc

        Parameters
        ----------
        doc: str
            Input document as string

        Returns
        -------
        list of Document
            Processed and tokenized doc

        """

        tokens = []
        for word in doc.split(" "):
            if self.min_len < len(word) < self.max_len and word not in self.stopwords:
                if self.lower:
                    word = word.lower()
                if self.deacc:
                    word = deaccent(word)
                if self.lemm:
                    word = self.lemm(word)
                if self.stem:
                    word = self.stem(word)

                tokens.append(word)
        return tokens
