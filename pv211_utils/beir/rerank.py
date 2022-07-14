from typing import Iterable



from pv211_utils.rerank import ReRankBase
from .entities import BeirQueryBase, BeirDocumentBase



class GenericReRank(ReRankBase):
    """A Reranker that uses the given model and query to reorder top_k documents.

    Parameters
    ----------
    model : Any
        A trained model that can assign a relevance to a query-document pair.
    """

    def __init__(self, model):
        self.model = model

    def rerank_top_k(self, query: BeirQueryBase, retrieved_documents: Iterable[BeirDocumentBase], k: int) -> Iterable[BeirDocumentBase]:
        top_k_documents = []
        query_document_pairs = []
        for document, _ in zip(retrieved_documents,range(k)):
            top_k_documents.append(document)
            query_document_pairs.append((query.body,document.body))
        cross_similarities = enumerate(self.model.predict(query_document_pairs))
        cross_similarities = sorted(cross_similarities, key=lambda item: item[1], reverse=True)


        # Return first k documents based on re-ranked order
        for document_number,_ in cross_similarities:
            document = top_k_documents[document_number]
            yield document
