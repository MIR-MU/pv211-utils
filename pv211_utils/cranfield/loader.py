from collections import OrderedDict
import json
from typing import Set, Tuple
import pkg_resources

from .entities import CranfieldQueryBase, CranfieldDocumentBase


def load_queries(query_class=CranfieldQueryBase) -> OrderedDict:
    queries = OrderedDict()

    with open(pkg_resources.resource_filename("pv211_utils", "data/cran.qry.json"), 'r') as f:
        for raw_query in json.load(f)[:-1]:
            query = query_class(
                query_id=raw_query['query number'],
                body=raw_query['query'],
            )
            queries[query.query_id] = query
    return queries


def load_documents(document_class=CranfieldDocumentBase) -> OrderedDict:
    documents = OrderedDict()

    with open(pkg_resources.resource_filename("pv211_utils", 'data/cranfield_data.json'), 'r') as f:
        for raw_document in json.load(f):
            document = document_class(
                document_id=raw_document['id'],
                authors=raw_document['author'],
                bibliography=raw_document['bibliography'],
                title=raw_document['title'],
                body=raw_document['body']
            )
            documents[document.document_id] = document
    return documents


def load_judgements(queries: OrderedDict, documents: OrderedDict) -> Set[Tuple[CranfieldQueryBase, CranfieldDocumentBase]]:
    relevant = set()

    with open(pkg_resources.resource_filename("pv211_utils", 'data/cranqrel.json'), 'r') as f:
        for raw_relevance in json.load(f):
            query_id = queries[int(raw_relevance['query_num'])]
            document_id = documents[int(raw_relevance['id'])]
            relevance = (query_id, document_id)
            relevant.add(relevance)
    return relevant
