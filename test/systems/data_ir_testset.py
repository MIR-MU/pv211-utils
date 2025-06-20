from collections import OrderedDict
from typing import List
from pv211_utils.entities import DocumentBase, QueryBase
from pv211_utils.preprocessing import DocPreprocessingBase

class DummyDocument(DocumentBase):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text


class DummyQuery(QueryBase):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text

DOCUMENTS = OrderedDict({
    "1": DummyDocument("climate change impacts polar bears in the Arctic"),
    "2": DummyDocument("the polar region is experiencing rising temperatures"),
    "3": DummyDocument("the economy and inflation are impacting consumers"),
})

QUERY = DummyQuery("climate change arctic polar bears")
