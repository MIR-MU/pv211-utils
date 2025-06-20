import pytest
from collections import OrderedDict
from typing import List

# Minimal mocks for required base classes
class DummyDocument:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class DummyQuery:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class DummyPreprocessor:
    def __call__(self, text: str) -> List[str]:
        return text.lower().split()


from pv211_utils.systems.bow import BoWSystem 


@pytest.fixture
def sample_documents():
    return OrderedDict({
        "1": DummyDocument("the cat sat on the mat"),
        "2": DummyDocument("the dog sat on the mat"),
        "3": DummyDocument("the cat chased the mouse"),
    })


def test_bow_initialization(sample_documents):
    preprocessor = DummyPreprocessor()
    system = BoWSystem(sample_documents, preprocessor)

    # Test dictionary
    assert "cat" in system.dictionary.token2id
    assert len(system.index_to_document) == 3


def test_bow_search_ranking(sample_documents):
    preprocessor = DummyPreprocessor()
    system = BoWSystem(sample_documents, preprocessor)

    query = DummyQuery("cat mat")
    results = list(system.search(query))

    # First document should be most similar to query
    assert isinstance(results[0], DummyDocument)
    assert str(results[0]) == "the cat sat on the mat"

    # All docs should be returned in sorted order
    assert len(results) == 3
