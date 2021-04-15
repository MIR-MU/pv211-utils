from contextlib import contextmanager
import json
from pathlib import Path
import pkg_resources
from typing import Union

from gdown import cached_download


@contextmanager
def google_drive_download(manifest_filename: str, cache_download: Union[str, Path, bool] = True):
    if isinstance(cache_download, Path) or isinstance(cache_download, str):
        download_path = Path(cache_download)
        if not download_path.parent.exists():  # If the download path contains a non-existent directory, ignore it
            download_path = None
    else:
        download_path = None

    with open(pkg_resources.resource_filename('pv211_utils', manifest_filename), 'rt') as f:
        manifest = json.load(f)
        filename = cached_download(
            url='https://drive.google.com/uc?id={}'.format(manifest['id']),
            md5=manifest['md5'],
            path=download_path,
        )
        filename = Path(filename)

    try:
        yield filename
    finally:
        if isinstance(cache_download, bool) and cache_download is False:  # If caching is disabled, remove file
            filename.unlink()
