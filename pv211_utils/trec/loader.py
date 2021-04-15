from collections import OrderedDict
import gzip
import json
import pkg_resources
from typing import Set

from .entities import TrecQueryBase, TrecDocumentBase, TrecJudgementBase
from ..util import google_drive_download


TrecJudgements = Set[TrecJudgementBase]


def load_queries(query_class=TrecQueryBase, subset: str = 'validation') -> OrderedDict:
    queries = OrderedDict()

    filename = 'data/trec_queries_{}.json'.format(subset)
    with open(pkg_resources.resource_filename('pv211_utils', filename), 'rt') as f:
        for raw_query in json.load(f):
            query = query_class(
                query_id=raw_query['query_id'],
                title=raw_query['title'],
                body=raw_query['description'],
                narrative=raw_query['narrative'],
            )
            queries[query.query_id] = query
    return queries


def load_documents(document_class=TrecDocumentBase, **kwargs) -> OrderedDict:
    documents = OrderedDict()

    manifest_filename = 'data/trec_documents_manifest.json'
    with google_drive_download(manifest_filename, **kwargs) as filename:
        with gzip.open(filename, 'rt') as f:
            for raw_document in json.load(f):
                document = document_class(
                    document_id=str(raw_document['document_id']),
                    body=raw_document['text']
                )
                documents[document.document_id] = document

    return documents


def load_judgements(queries: OrderedDict, documents: OrderedDict, subset: str = 'validation') -> TrecJudgements:
    relevant = set()

    filename = 'data/trec_judgements_{}.json'.format(subset)
    with open(pkg_resources.resource_filename('pv211_utils', filename), 'rt') as f:
        for query_id, document_id in json.load(f):
            query: TrecQueryBase = queries[query_id]
            document: TrecDocumentBase = documents[document_id]
            relevance = (query, document)
            relevant.add(relevance)
    return relevant
