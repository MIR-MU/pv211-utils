from pathlib import Path


BASE_TEXT_FORMATS = ['text']


def download_trec(root_directory: Path) -> None:
    from pv211_utils.trec.loader import load_documents

    pathname = str(root_directory/'trec_documents.json.gz')
    load_documents(cache_download=pathname)


def download_arqmath(root_directory: Path) -> None:
    from pv211_utils.arqmath.loader import load_answers, TEXT_FORMATS

    text_formats = set(TEXT_FORMATS) & set(BASE_TEXT_FORMATS)
    for text_format in text_formats:
        pathname = str(root_directory/f'arqmath2020_answers_{text_format}.json.gz')
        load_answers(text_format, cache_download=pathname)


def main() -> None:
    root_directory = Path('/var') / 'tmp' / 'pv211'
    root_directory.mkdir(parents=True, exist_ok=True)
    download_trec(root_directory)
    download_arqmath(root_directory)


if __name__ == '__main__':
    main()
