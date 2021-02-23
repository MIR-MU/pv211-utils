from functools import total_ordering
from typing import Any


@total_ordering
class DocumentBase:
    """A document.

    Parameters
    ----------
    document_id : str
        A unique identifier of the document.
    body : Any
        The abstract of the document.

    Attributes
    ----------
    document_id : str
        A unique identifier of the document.
    body : Any
        The abstract of the document.

    """
    SUMMARY_LENGTH = 50

    def __init__(self, document_id: str, body: Any):
        self.document_id = document_id
        self.body = body

    def __hash__(self):
        return hash(self.document_id)

    def __eq__(self, other):
        if isinstance(other, DocumentBase):
            return self.document_id == other.document_id
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DocumentBase):
            return self.document_id < other.document_id
        return NotImplemented

    def __repr__(self):
        summary = ' '.join(self.body.split())
        if len(summary) > self.SUMMARY_LENGTH:
            summary = '{} ...'.format(summary[:self.SUMMARY_LENGTH])
        return f'<Document {self.document_id} “{summary}”>'


@total_ordering
class QueryBase:
    """A query.

    Parameters
    ----------
    query_id : int
        A unique identifier of the query.
    body : Any
        The text of the query.

    Attributes
    ----------
    query_id : int
        A unique identifier of the query.
    body : Any
        The text of the query.

    """
    def __init__(self, query_id: int, body: Any):
        self.query_id = query_id
        self.body = body

    def __hash__(self):
        return hash(self.query_id)

    def __eq__(self, other):
        if isinstance(other, QueryBase):
            return self.query_id == other.query_id
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, QueryBase):
            return self.query_id < other.query_id
        return NotImplemented

    def __repr__(self):
        return f'<Query {self.query_id} “{self.body}”>'
