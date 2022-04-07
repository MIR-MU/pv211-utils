from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import pkg_resources
from typing import Union, Callable, Dict, Optional
from urllib.request import urlretrieve


def assert_md5sum(filename: Path, md5: str, quiet: bool = False, blocksize: int = 65536):
    if not (isinstance(md5, str) and len(md5) == 32):
        raise ValueError('MD5 must be 32 chars: {}'.format(md5))

    if not quiet:
        print('Computing MD5: {}'.format(filename))

    digest = hashlib.md5()
    with filename.open('rb') as f:
        for block in iter(lambda: f.read(blocksize), b''):
            digest.update(block)
    md5_actual = digest.hexdigest()

    if md5_actual == md5:
        if not quiet:
            print('MD5 matches: {}'.format(filename))
        return True

    raise AssertionError("MD5 doesn't match:\nactual: {}\nexpected: {}".format(md5_actual, md5))


@contextmanager
def google_drive_download(**kwargs):
    def download_function(manifest: Dict, download_path: Optional[Path]) -> Path:
        from gdown import cached_download

        url = 'https://drive.google.com/uc?id={}'.format(manifest['google_drive_id'])

        try:
            filename = cached_download(url=url, md5=manifest['md5'], path=download_path)
        except AssertionError as e:
            if 'md5_also_ok' in manifest:
                filename = cached_download(url=url, md5=manifest['md5_also_ok'], path=download_path)
            else:
                raise e
        return Path(filename)

    return _cached_download(download_function, **kwargs)


@contextmanager
def http_download(*args, **kwargs):
    def download_function(manifest: Dict, download_path: Optional[Path]) -> Path:
        url = manifest['http_url']
        if download_path is None:
            download_path = Path.home() / '.cache' / 'pv211-utils' / manifest['md5']
            download_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if not download_path.exists():
                urlretrieve(url, download_path)
            try:
                assert_md5sum(download_path, manifest['md5'])
            except AssertionError as e:
                if 'md5_also_ok' in manifest:
                    assert_md5sum(download_path, manifest['md5_also_ok'])
                else:
                    raise e
        except Exception as e:
            download_path.unlink()
            raise e
        return download_path

    return _cached_download(download_function, *args, **kwargs)


def _cached_download(download_function: Callable[[Dict, Optional[Path]], Path],
                     manifest_filename: str, cache_download: Union[str, Path, bool] = True):
    if isinstance(cache_download, Path) or isinstance(cache_download, str):
        download_path = Path(cache_download)
        if not download_path.parent.exists():  # If the download path contains a non-existent directory, ignore it
            download_path = None
    else:
        download_path = None

    with open(pkg_resources.resource_filename('pv211_utils', manifest_filename), 'rt') as f:
        manifest = json.load(f)
        filename = download_function(manifest, download_path)

    try:
        yield filename
    finally:
        if isinstance(cache_download, bool) and cache_download is False:  # If caching is disabled, remove file
            filename.unlink()
