from collections import OrderedDict
import json
from typing import Set, Tuple
from re import sub
import pkg_resources

from pv211_utils.entities import Query, Document


def load_queries() -> OrderedDict:
    queries = OrderedDict()

    with open(pkg_resources.resource_filename("pv211_utils", "data/cran.qry.json"), 'r') as f:
        for raw_query in json.load(f)[:-1]:
            query = Query(
                query_id=raw_query['query number'],
                body=raw_query['query'],
            )
            queries[query.query_id] = query
    return queries


def load_documents() -> OrderedDict:
    documents = OrderedDict()

    with open(pkg_resources.resource_filename("pv211_utils", 'data/cranfield_data.json'), 'r') as f:
        for raw_document in json.load(f):
            authors = [
                sub(r' et al.$', '', author)
                for author in raw_document['author'].split(' and ')
            ]
            document = Document(
                document_id=raw_document['id'],
                authors=authors,
                bibliography=raw_document['bibliography'],
                title=raw_document['title'],
                body=raw_document['body'],
            )
            documents[document.document_id] = document
    return documents


def load_judgements(queries, documents) -> Set[Tuple[int, int]]:
    relevant = set()

    with open(pkg_resources.resource_filename('data/cranqrel.json'), 'r') as f:
        for raw_relevance in json.load(f):
            query_id = queries[int(raw_relevance['query_num'])]
            document_id = documents[int(raw_relevance['id'])]
            relevance = (query_id, document_id)
            relevant.add(relevance)
    return relevant
