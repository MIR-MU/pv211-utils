from collections import OrderedDict
import gzip
import json
from typing import Optional, Set, Tuple, Union
from pathlib import Path
import pkg_resources

from gdown import cached_download

from .entities import TrecQueryBase, TrecDocumentBase


TrecJudgements = Set[Tuple[TrecQueryBase, TrecDocumentBase]]


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


def load_documents(document_class=TrecDocumentBase,
                   cache_download: Optional[Union[str, Path, bool]] = None) -> OrderedDict:
    if isinstance(cache_download, Path) or isinstance(cache_download, str):
        download_path = Path(cache_download)
        if not download_path.parent.exists():  # If the download path contains a non-existent directory, ignore it
            download_path = None
    else:
        download_path = None

    with open(pkg_resources.resource_filename('pv211_utils', 'data/trec_documents_manifest.json'), 'rt') as f:
        manifest = json.load(f)
        filename = cached_download(
            url='https://drive.google.com/uc?id={}'.format(manifest['id']),
            md5=manifest['md5'],
            path=download_path,
        )
        filename = Path(filename)

    documents = OrderedDict()

    with gzip.open(filename, 'rt') as f:
        for raw_document in json.load(f):
            document = document_class(
                document_id=str(raw_document['document_id']),
                body=raw_document['text']
            )
            documents[document.document_id] = document

    if isinstance(cache_download, bool) and cache_download is False:  # If caching is disabled, remove downloaded file
        filename.unlink()

    return documents


def load_judgements(queries: OrderedDict, documents: OrderedDict, subset: str = 'validation') -> TrecJudgements:
    relevant = set()

    filename = 'data/trec_judgements_{}.json'.format(subset)
    with open(pkg_resources.resource_filename('pv211_utils', filename), 'rt') as f:
        for query_id, document_id in json.load(f):
            query = queries[query_id]
            document = documents[document_id]
            relevance = (query, document)
            relevant.add(relevance)
    return relevant
