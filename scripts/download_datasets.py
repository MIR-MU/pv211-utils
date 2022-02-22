from pathlib import Path

from pv211_utils.trec.loader import load_documents as trec_load_documents


if __name__ == '__main__':
    root_directory = Path('/var') / 'tmp' / 'pv211'
    root_directory.mkdir(parents=True, exist_ok=True)
    trec_load_documents(Document, cache_download=str(root_directory/'trec_documents.json.gz'))
