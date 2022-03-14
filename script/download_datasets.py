from pathlib import Path

from pv211_utils.trec.loader import load_documents as trec_load_documents
from pv211_utils.arqmath.loader import load_answers as arqmath_load_answers, TEXT_FORMATS


if __name__ == '__main__':
    root_directory = Path('/var') / 'tmp' / 'pv211'
    root_directory.mkdir(parents=True, exist_ok=True)
    trec_load_documents(cache_download=str(root_directory/'trec_documents.json.gz'))
    for text_format in TEXT_FORMATS:
        arqmath_filename = str(root_directory/f'arqmath2020_answers_{text_format}.json.gz'
        arqmath_load_answers(text_format, cache_download=))
