from pathlib import Path
from os import umask
from sys import argv


if len(argv) > 1 and argv[1] == 'all':
    from pv211_utils.arqmath.loader import TEXT_FORMATS

    BASE_TEXT_FORMATS = TEXT_FORMATS
else:
    BASE_TEXT_FORMATS = ['text']


def download_trec(root_directory: Path) -> None:
    from pv211_utils.trec.loader import load_documents

    pathname = str(root_directory / 'trec_documents.json.gz')
    load_documents(cache_download=pathname)


def download_arqmath(root_directory: Path) -> None:
    from pv211_utils.arqmath.loader import load_questions, load_answers, TEXT_FORMATS

    text_formats = set(TEXT_FORMATS) & set(BASE_TEXT_FORMATS)
    for text_format in text_formats:
        answers_pathname = str(root_directory / f'arqmath2020_answers_{text_format}.json.gz')
        answers = load_answers(text_format, cache_download=answers_pathname)
        questions_pathname = str(root_directory / f'arqmath2020_questions_{text_format}.json.gz')
        load_questions(text_format, answers, cache_download=questions_pathname)


def main() -> None:
    umask(0o000)
    root_directory = Path('/var') / 'tmp' / 'pv211'
    root_directory.mkdir(parents=True, exist_ok=True, mode=0o777)
    download_trec(root_directory)
    download_arqmath(root_directory)


if __name__ == '__main__':
    main()
