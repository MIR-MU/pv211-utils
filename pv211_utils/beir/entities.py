from typing import Any, Tuple, Optional, List, Set

from pv211_utils.entities import DocumentBase, QueryBase


class BeirDocumentBase(DocumentBase):
    """A Generic document with just an id and a body.

    Parameters
    ----------
    document_id : str
        A unique identifier of the document.
    body : Any
        The text of the document.

    """
    def __init__(self, document_id: str, body: Any):
        super().__init__(document_id, body)


class BeirQueryBase(QueryBase):
    """A Generic query with just an id and a body

    Parameters
    ----------
    query_id : int
        A unique identifier of the query.
    body : Any
        The text of the query.

    """
    def __init__(self, query_id: int, body: Any):
        super().__init__(query_id, body)


class RawBeirDataset:
    """A generic BIER dataset with options

    Parameters
    ----------
    name : str
        A unique identifier of the dataset, select one name from the list of available datasets.
    train : bool
        A bool value that dictates if a train subset should be prepared.
    dev : bool
        A bool value that dictates if a dev subset should be prepared.
    test : bool
        A bool value that dictates if a test subset should be prepared.
    train_alternative : str
        An alternative in case the given dataset does not come with an available training subset.
    dev_alternative : str
        An alternative in case the given dataset does not come with an available dev subset.
    test_alternative : str
        An alternative in case the given dataset does not come with an available test subset.

    """
    def __init__(self, name: str,
                 train: bool = False, dev: bool = False, test: bool = False,
                 train_alternative: Optional[str] = None, dev_alternative: Optional[str] = None,
                 test_alternative: Optional[str] = None):
        self.name = name
        self.train = train
        self.dev = dev
        self.test = test
        self.train_alternative = train_alternative
        self.dev_alternative = dev_alternative
        self.test_alternative = test_alternative


class RawBeirDatasets:
    """A list of RawBeirDataset that will be loaded, prepared and merged into one for use in IR systems.

    Parameters
    ----------
    download_location : str
        A address where all the datasets will be downloaded. Access availability is required.
    datasets : List[RawBeirDataset]
        A list of RawBeirDataset values.
    """
    def __init__(self, datasets: List[RawBeirDataset], download_location: str):
        self.download_location = download_location
        self.datasets = datasets


BeirJudgementBase = Tuple[BeirQueryBase, BeirDocumentBase]
BeirJudgementsBase = Set[BeirJudgementBase]
