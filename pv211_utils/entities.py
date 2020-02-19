from functools import total_ordering


@total_ordering
class DocumentBase(object):
    """
    A Cranfield collection document.

    Parameters
    ----------
    document_id : int
        A unique identifier of the document.
    authors : list of str
        A unique identifiers of the authors of the document.
    bibliography : str
        The bibliographical entry for the document.
    title : str
        The title of the document.
    body : str
        The abstract of the document.

    Attributes
    ----------
    document_id : int
        A unique identifier of the document.
    authors : list of str
        A unique identifiers of the authors of the document.
    bibliography : str
        The bibliographical entry for the document.
    title : str
        The title of the document.
    body : str
        The abstract of the document.

    """
    document_id = None
    authors = None
    bibliography = None
    title = None
    body = None

    def __init__(self, document_id, authors, bibliography, title, body):
        self.document_id = document_id
        self.authors = authors
        self.bibliography = bibliography
        self.title = title
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
        return f'<Document {self.document_id} titled “{self.title}”>'


@total_ordering
class QueryBase(object):
    """
    A Cranfield collection query.

    Parameters
    ----------
    query_id : int
        A unique identifier of the query.
    body : str
        The text of the query.

    Attributes
    ----------
    query_id : int
        A unique identifier of the query.
    body : str
        The text of the query.

    """
    def __init__(self, query_id: int, body: str):
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
