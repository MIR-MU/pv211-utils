from typing import Any, Tuple

from ..entities import DocumentBase, QueryBase


class TrecDocumentBase(DocumentBase):
    """A TREC collection document.

    Parameters
    ----------
    document_id : str
        A unique identifier of the document.
    body : Any
        The text of the document.

    """
    def __init__(self, document_id: str, body: Any):
        super().__init__(document_id, body)


class TrecQueryBase(QueryBase):
    """A TREC collection query.

    Parameters
    ----------
    query_id : int
        A unique identifier of the query.
    title : Any
        Up to three words that best describe the query.
    body : Any
        A one-sentence description of the topic area.
    narrative: Any
        A concise description of what makes a document relevant.

    Attributes
    ----------
    title : Any
        Up to three words that best describe the query.
    narrative: Any
        A concise description of what makes a document relevant.

    """
    def __init__(self, query_id: int, title: Any, body: Any, narrative: Any):
        super().__init__(query_id, body)
        self.title = title
        self.narrative = narrative


TrecJudgementBase = Tuple[TrecQueryBase, TrecDocumentBase]
