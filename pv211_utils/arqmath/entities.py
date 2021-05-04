from typing import Any, List, Tuple

from ..entities import DocumentBase, QueryBase


class ArqmathAnswerBase(DocumentBase):
    """An answer from the ARQMath collection.

    Parameters
    ----------
    document_id : str
        A unique identifier of the answer among all questions and answers.
    body : Any
        The text of the answer, including mathematical formulae.
    upvotes : int
        The number of upvotes for the answer.
    is_accepted : bool
        If the answer has been accepted by the poster of the question.

    Attributes
    ----------
    upvotes : int
        The number of upvotes for the answer.
    is_accepted : bool
        If the answer has been accepted by the poster of the question.

    """
    def __init__(self, document_id: str, body: Any, upvotes: int, is_accepted: bool):
        super().__init__(document_id, body)
        self.upvotes = upvotes
        self.is_accepted = is_accepted


class ArqmathQuestionBase(DocumentBase):
    """A question from the ARQMath collection.

    Parameters
    ----------
    document_id : str
        A unique identifier of the question among all questions and answers.
    title : Any
        The title of the question, including mathematical formulae.
    body : Any
        The text of the question, including mathematical formulae.
    tags : list of str
        Tags describing the topics of the question.
    upvotes : int
        The number of upvotes for the question.
    views : int
        The number of views for the question.
    answers : list of ArqmathAnswerBase
        The answers for the question.

    Attributes
    ----------
    title : Any
        The title of the question, including mathematical formulae.
    tags : list of str
        Tags describing the topics of the question.
    upvotes : int
        The number of upvotes for the question.
    views : int
        The number of views for the question.
    answers : list of ArqmathAnswerBase
        The answers for the question.

    """
    def __init__(self, document_id: str, title: Any, body: Any, tags: List[str],
                 upvotes: int, views: int, answers: List[ArqmathAnswerBase]):
        super().__init__(document_id, body)
        self.title = title
        self.tags = tags
        self.upvotes = upvotes
        self.views = views
        self.answers = answers


class ArqmathQueryBase(QueryBase):
    """A query from the answer retrieval task of ARQMath.

    Parameters
    ----------
    query_id : int
        A unique identifier of the query.
    title : Any
        The title of the query, including mathematical formulae.
    body : Any
        The text of the query, including mathematical formulae.
    tags : list of str
        Tags describing the topics of the query.

    Attributes
    ----------
    title : Any
        The title of the query, including mathematical formulae.
    tags : list of str
        Tags describing the topics of the query.

    """
    def __init__(self, query_id: int, title: Any, body: Any, tags: List[str]):
        super().__init__(query_id, body)
        self.title = title
        self.tags = tags


ArqmathJudgementBase = Tuple[ArqmathQueryBase, ArqmathAnswerBase]
