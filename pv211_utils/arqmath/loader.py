from collections import OrderedDict
import gzip
import json
import pkg_resources
import re
from typing import Optional, Set

import ijson

from .entities import ArqmathQueryBase, ArqmathQuestionBase, ArqmathAnswerBase, ArqmathJudgementBase
from ..util import google_drive_download


ArqmathJudgements = Set[ArqmathJudgementBase]
TEXT_FORMATS = (
    'text',
    'text+latex',
    'text+prefix',
    'xhtml+latex',
    'xhtml+cmml',
    'xhtml+pmml',
)


def _check_text_format(text_format: str) -> None:
    if text_format in TEXT_FORMATS:
        return
    recognized_text_formats = ', '.join(
        '"{}"'.format(text_format)
        for text_format
        in TEXT_FORMATS
    )
    message = (
        'The requested text format "{}" has not been recognized.\n'
        'The recognized text formats are {}.'
    )
    message = message.format(text_format, recognized_text_formats)
    raise ValueError(message)


def _resolve_query_id(raw_query_id: str) -> int:
    query_id_match = re.fullmatch('A.(?P<query_id>[0-9]+)', raw_query_id)
    assert query_id_match is not None
    query_id = int(query_id_match.group('query_id'))
    return query_id


def load_queries(text_format: str, query_class=ArqmathQueryBase) -> OrderedDict:
    _check_text_format(text_format)
    queries = OrderedDict()

    filename = 'data/arqmath2020_queries_{}.json'.format(text_format)
    with open(pkg_resources.resource_filename('pv211_utils', filename), 'rt') as f:
        for raw_query in json.load(f):
            query_id = _resolve_query_id(raw_query['query_id'])
            query = query_class(
                query_id=query_id,
                title=raw_query['title'],
                body=raw_query['body'],
                tags=raw_query['tags'],
            )
            queries[query.query_id] = query

    return queries


def load_questions(text_format: str, answers: OrderedDict, question_class=ArqmathQuestionBase,
                   filter_document_ids: Optional[Set] = None, **kwargs) -> OrderedDict:
    _check_text_format(text_format)
    questions = OrderedDict()

    manifest_filename = 'data/arqmath2020_questions_{}_manifest.json'
    manifest_filename = manifest_filename.format(text_format)
    with google_drive_download(manifest_filename, **kwargs) as filename:
        with gzip.open(filename, 'rt') as f:
            for raw_question in ijson.items(f, 'item'):
                document_id = raw_question['document_id']
                if filter_document_ids is not None and document_id not in filter_document_ids:
                    continue
                question_answers = [answers[document_id] for document_id in raw_question['answers']]
                question = question_class(
                    document_id=document_id,
                    title=raw_question['title'],
                    body=raw_question['body'],
                    tags=raw_question['tags'],
                    upvotes=raw_question['upvotes'],
                    views=raw_question['views'],
                    answers=question_answers,
                )
                questions[question.document_id] = question

    return questions


def load_answers(text_format: str, answer_class=ArqmathAnswerBase,
                 filter_document_ids: Optional[Set] = None, **kwargs) -> OrderedDict:
    _check_text_format(text_format)
    answers = OrderedDict()

    manifest_filename = 'data/arqmath2020_answers_{}_manifest.json'
    manifest_filename = manifest_filename.format(text_format)
    with google_drive_download(manifest_filename, **kwargs) as filename:
        with gzip.open(filename, 'rt') as f:
            for raw_answer in ijson.items(f, 'item'):
                document_id = raw_answer['document_id']
                if filter_document_ids is not None and document_id not in filter_document_ids:
                    continue
                assert raw_answer['is_accepted'] in ('True', 'False')
                is_accepted = raw_answer['is_accepted'] == 'True'
                answer = answer_class(
                    document_id=document_id,
                    body=raw_answer['body'],
                    upvotes=raw_answer['upvotes'],
                    is_accepted=is_accepted,
                )
                answers[answer.document_id] = answer

    return answers


def load_judgements(queries: OrderedDict, answers: OrderedDict,
                    filter_document_ids: Optional[Set] = None) -> ArqmathJudgements:
    relevant = set()

    filename = 'data/arqmath2020_judgements.json'
    with open(pkg_resources.resource_filename('pv211_utils', filename), 'rt') as f:
        for raw_query_id, document_id in json.load(f):
            query_id = _resolve_query_id(raw_query_id)
            if filter_document_ids is not None and document_id not in filter_document_ids:
                continue
            query: ArqmathQueryBase = queries[query_id]
            answer: ArqmathAnswerBase = answers[document_id]
            relevance = (query, answer)
            relevant.add(relevance)

    return relevant
