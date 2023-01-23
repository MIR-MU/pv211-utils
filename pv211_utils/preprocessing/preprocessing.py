from abc import ABC, abstractmethod
from gensim.utils import simple_preprocess
from typing import List


class DocPreprocessing(ABC):
    @abstractmethod
    def __call__(self, doc: str) -> List[str]:
        raise NotImplementedError()


class NoneDocProcessing(DocPreprocessing):
    def __call__(self, doc: str) -> List[str]:
        return doc.split(" ")


class SimpleDocProcessing(DocPreprocessing):
    def __init__(self, deacc: bool = False, min_len: int = 2, max_len: int = 15):
        self.deacc = deacc
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, doc: str) -> List[str]:
        return simple_preprocess(doc, self.deacc, self.min_len, self.max_len)
