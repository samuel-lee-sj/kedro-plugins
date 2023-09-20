import importlib
from pathlib import Path, PurePosixPath
from time import sleep

import pandas as pd
import pytest
from adlfs import AzureBlobFileSystem
from fsspec.implementations.http import HTTPFileSystem
from fsspec.implementations.local import LocalFileSystem
from gcsfs import GCSFileSystem
from kedro.io import Version
from kedro.io.core import PROTOCOL_DELIMITER, generate_timestamp
from pandas._testing import assert_frame_equal
from s3fs import S3FileSystem

from kedro_datasets._io import DatasetError
from kedro_datasets.pandas import GenericDataset
from kedro_datasets.pandas.generic_dataset import _DEPRECATED_CLASSES


@pytest.fixture
def filepath_sas(tmp_path):
    return tmp_path / "test.sas7bdat"


@pytest.fixture
def filepath_csv(tmp_path):
    return tmp_path / "test.csv"


@pytest.fixture
def filepath_html(tmp_path):
    return tmp_path / "test.html"


# pylint: disable=line-too-long
@pytest.fixture()
def sas_binary():
    return b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc2\xea\x81`\xb3\x14\x11\xcf\xbd\x92\x08\x00\t\xc71\x8c\x18\x1f\x10\x11""\x002"\x01\x022\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x18\x1f\x10\x11""\x002"\x01\x022\x042\x01""\x00\x00\x00\x00\x10\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00SAS FILEAIRLINE                                                         DATA    \x00\x00\xc0\x95j\xbe\xd6A\x00\x00\xc0\x95j\xbe\xd6A\x00\x00\x00\x00\x00 \xbc@\x00\x00\x00\x00\x00 \xbc@\x00\x04\x00\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x009.0000M0WIN\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00WIN\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x95LN\xaf\xf0LN\xaf\xf0LN\xaf\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00jIW-\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00kIW-\x00\x00\x00\x00\x00\x00\x00\x00<\x04\x00\x00\x00\x02-\x00\r\x00\x00\x00 \x0e\x00\x00\xe0\x01\x00\x00\x00\x00\x00\x00\x14\x0e\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\xe4\x0c\x00\x000\x01\x00\x00\x00\x00\x00\x00H\x0c\x00\x00\x9c\x00\x00\x00\x00\x01\x00\x00\x04\x0c\x00\x00D\x00\x00\x00\x00\x01\x00\x00\xa8\x0b\x00\x00\\\x00\x00\x00\x00\x01\x00\x00t\x0b\x00\x004\x00\x00\x00\x00\x00\x00\x00@\x0b\x00\x004\x00\x00\x00\x00\x00\x00\x00\x0c\x0b\x00\x004\x00\x00\x00\x00\x00\x00\x00\xd8\n\x00\x004\x00\x00\x00\x00\x00\x00\x00\xa4\n\x00\x004\x00\x00\x00\x00\x00\x00\x00p\n\x00\x004\x00\x00\x00\x00\x00\x00\x00p\n\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00p\x9e@\x00\x00\x00@\x8bl\xf3?\x00\x00\x00\xc0\x9f\x1a\xcf?\x00\x00\x00\xa0w\x9c\xc2?\x00\x00\x00\x00\xd7\xa3\xf6?\x00\x00\x00\x00\x81\x95\xe3?\x00t\x9e@\x00\x00\x00\xe0\xfb\xa9\xf5?\x00\x00\x00\x00\xd7\xa3\xd0?\x00\x00\x00`\xb3\xea\xcb?\x00\x00\x00 \xdd$\xf6?\x00\x00\x00\x00T\xe3\xe1?\x00x\x9e@\x00\x00\x00\xc0\x9f\x1a\xf9?\x00\x00\x00\x80\xc0\xca\xd1?\x00\x00\x00\xc0m4\xd4?\x00\x00\x00\x80?5\xf6?\x00\x00\x00 \x04V\xe2?\x00|\x9e@\x00\x00\x00\x00\x02+\xff?\x00\x00\x00@\x0c\x02\xd3?\x00\x00\x00\xc0K7\xd9?\x00\x00\x00\xc0\xcc\xcc\xf8?\x00\x00\x00\xc0I\x0c\xe2?\x00\x80\x9e@\x00\x00\x00`\xb8\x1e\x02@\x00\x00\x00@\n\xd7\xd3?\x00\x00\x00\xc0\x10\xc7\xd6?\x00\x00\x00\x00\xfe\xd4\xfc?\x00\x00\x00@5^\xe2?\x00\x84\x9e@\x00\x00\x00\x80\x16\xd9\x05@\x00\x00\x00\xe0\xa5\x9b\xd4?\x00\x00\x00`\xc5\xfe\xd6?\x00\x00\x00`\xe5\xd0\xfe?\x00\x00\x00 \x83\xc0\xe6?\x00\x88\x9e@\x00\x00\x00@33\x08@\x00\x00\x00\xe0\xa3p\xd5?\x00\x00\x00`\x8f\xc2\xd9?\x00\x00\x00@\x8bl\xff?\x00\x00\x00\x00\xfe\xd4\xe8?\x00\x8c\x9e@\x00\x00\x00\xe0\xf9~\x0c@\x00\x00\x00`ff\xd6?\x00\x00\x00\xe0\xb3Y\xd9?\x00\x00\x00`\x91\xed\x00@\x00\x00\x00\xc0\xc8v\xea?\x00\x90\x9e@\x00\x00\x00\x00\xfe\xd4\x0f@\x00\x00\x00\xc0\x9f\x1a\xd7?\x00\x00\x00\x00\xf7u\xd8?\x00\x00\x00@\xe1z\x03@\x00\x00\x00\xa0\x99\x99\xe9?\x00\x94\x9e@\x00\x00\x00\x80\x14\xae\x11@\x00\x00\x00@\x89A\xd8?\x00\x00\x00\xa0\xed|\xd3?\x00\x00\x00\xa0\xef\xa7\x05@\x00\x00\x00\x00\xd5x\xed?\x00\x98\x9e@\x00\x00\x00 \x83@\x12@\x00\x00\x00\xe0$\x06\xd9?\x00\x00\x00`\x81\x04\xd5?\x00\x00\x00`\xe3\xa5\x05@\x00\x00\x00\xa0n\x12\xf1?\x00\x9c\x9e@\x00\x00\x00\x80=\x8a\x15@\x00\x00\x00\x80\x95C\xdb?\x00\x00\x00\xa0\xab\xad\xd8?\x00\x00\x00\xa0\x9b\xc4\x06@\x00\x00\x00\xc0\xf7S\xf1?\x00\xa0\x9e@\x00\x00\x00\xc0K7\x16@\x00\x00\x00 X9\xdc?\x00\x00\x00@io\xd4?\x00\x00\x00\xa0E\xb6\x08@\x00\x00\x00\x00-\xb2\xf7?\x00\xa4\x9e@\x00\x00\x00\x00)\xdc\x15@\x00\x00\x00\xe0\xa3p\xdd?\x00\x00\x00@\xa2\xb4\xd3?\x00\x00\x00 \xdb\xf9\x08@\x00\x00\x00\xe0\xa7\xc6\xfb?\x00\xa8\x9e@\x00\x00\x00\xc0\xccL\x17@\x00\x00\x00\x80=\n\xdf?\x00\x00\x00@\x116\xd8?\x00\x00\x00\x00\xd5x\t@\x00\x00\x00`\xe5\xd0\xfe?\x00\xac\x9e@\x00\x00\x00 \x06\x81\x1b@\x00\x00\x00\xe0&1\xe0?\x00\x00\x00 \x83\xc0\xda?\x00\x00\x00\xc0\x9f\x1a\n@\x00\x00\x00\xc0\xf7S\x00@\x00\xb0\x9e@\x00\x00\x00\x80\xc0J\x1f@\x00\x00\x00\xc0K7\xe1?\x00\x00\x00\xa0\x87\x85\xe0?\x00\x00\x00\xa0\xc6K\x0b@\x00\x00\x00@\xb6\xf3\xff?\x00\xb4\x9e@\x00\x00\x00\xa0p="@\x00\x00\x00\xc0I\x0c\xe2?\x00\x00\x00\xa0\x13\xd0\xe2?\x00\x00\x00`\xe7\xfb\x0c@\x00\x00\x00\x00V\x0e\x02@\x00\xb8\x9e@\x00\x00\x00\xe0$\x06%@\x00\x00\x00 \x83\xc0\xe2?\x00\x00\x00\xe0H.\xe1?\x00\x00\x00\xa0\xc6K\x10@\x00\x00\x00\xc0\x9d\xef\x05@\x00\xbc\x9e@\x00\x00\x00\x80=\n*@\x00\x00\x00\x80l\xe7\xe3?\x00\x00\x00@io\xdc?\x00\x00\x00@\n\xd7\x12@\x00\x00\x00`\x12\x83\x0c@\x00\xc0\x9e@\x00\x00\x00\xc0\xa1\x85.@\x00\x00\x00@\xdfO\xe5?\x00\x00\x00\xa0e\x88\xd3?\x00\x00\x00@5\xde\x14@\x00\x00\x00\x80h\x11\x13@\x00\xc4\x9e@\x00\x00\x00\xc0 P0@\x00\x00\x00 Zd\xe7?\x00\x00\x00`\x7f\xd9\xcd?\x00\x00\x00\xe0\xa7F\x16@\x00\x00\x00\xa0C\x0b\x1a@\x00\xc8\x9e@\x00\x00\x00 \x83\x000@\x00\x00\x00@\x8d\x97\xea?\x00\x00\x00\xe06\x1a\xc8?\x00\x00\x00@\xe1\xfa\x15@\x00\x00\x00@\x0c\x82\x1e@\x00\xcc\x9e@\x00\x00\x00 \x83\xc0/@\x00\x00\x00\xc0\xf3\xfd\xec?\x00\x00\x00`\xf7\xe4\xc9?\x00\x00\x00 \x04V\x15@\x00\x00\x00\x80\x93X!@\x00\xd0\x9e@\x00\x00\x00\xe0x\xa90@\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\xa0\xd4\t\xd0?\x00\x00\x00\xa0Ga\x15@\x00\x00\x00\xe0x\xa9 @\x00\xd4\x9e@\x00\x00\x00\x80\x95\x031@\x00\x00\x00@`\xe5\xf0?\x00\x00\x00@@\x13\xd1?\x00\x00\x00`\xe3\xa5\x16@\x00\x00\x00 /\x1d!@\x00\xd8\x9e@\x00\x00\x00\x80\x14N3@\x00\x00\x00\x80\x93\x18\xf2?\x00\x00\x00\xa0\xb2\x0c\xd1?\x00\x00\x00\x00\x7f\xea\x16@\x00\x00\x00\xa0\x18\x04#@\x00\xdc\x9e@\x00\x00\x00\x80\x93\xb82@\x00\x00\x00@\xb6\xf3\xf3?\x00\x00\x00\xc0\xeas\xcd?\x00\x00\x00\x00T\xe3\x16@\x00\x00\x00\x80\xbe\x1f"@\x00\xe0\x9e@\x00\x00\x00\x00\x00@3@\x00\x00\x00\x00\x00\x00\xf6?\x00\x00\x00\xc0\xc1\x17\xd6?\x00\x00\x00\xc0I\x0c\x17@\x00\x00\x00\xe0$\x86 @\x00\xe4\x9e@\x00\x00\x00\xc0\xa1\xa54@\x00\x00\x00`9\xb4\xf8?\x00\x00\x00@\xe8\xd9\xdc?\x00\x00\x00@\x0c\x82\x17@\x00\x00\x00@`\xe5\x1d@\x00\xe8\x9e@\x00\x00\x00 \xdb\xb96@\x00\x00\x00\xe0|?\xfb?\x00\x00\x00@p\xce\xe2?\x00\x00\x00\x80\x97n\x18@\x00\x00\x00\x00\x7fj\x1c@\x00\xec\x9e@\x00\x00\x00\xc0v\x9e7@\x00\x00\x00\xc0\xc8v\xfc?\x00\x00\x00\x80q\x1b\xe1?\x00\x00\x00\xc0rh\x1b@\x00\x00\x00\xe0\xf9~\x1b@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xfb\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x00\r\x00\x00\x00\x00\x00\x00\x00\xfe\xfb\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x0b\x00\x00\x00\x00\x00\x00\x00\xfe\xfb\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00L\x00\r\x00\x00\x00\x00\x00\x00\x00\xfe\xfb\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\x00\t\x00\x00\x00\x00\x00\x00\x00\xfe\xfb\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00(\x00\x0f\x00\x00\x00\x00\x00\x00\x00\xfe\xfb\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x04\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xffP\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x04\x01\x00\x04\x00\x00\x00\x08\x00\x00\x00\x00\x04\x01\x00\x0c\x00\x00\x00\x08\x00\x00\x00\x00\x04\x01\x00\x14\x00\x00\x00\x08\x00\x00\x00\x00\x04\x01\x00\x1c\x00\x00\x00\x08\x00\x00\x00\x00\x04\x01\x00$\x00\x00\x00\x08\x00\x00\x00\x00\x04\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x04\x00\x00\x00\x00\x00$\x00\x01\x00\x00\x00\x00\x008\x00\x01\x00\x00\x00\x00\x00H\x00\x01\x00\x00\x00\x00\x00\\\x00\x01\x00\x00\x00\x00\x00l\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x90\x00\x10\x00\x80\x00\x00\x00\x00\x00\x00\x00Written by SAS\x00\x00YEARyearY\x00\x00\x00level of output\x00W\x00\x00\x00wage rate\x00\x00\x00R\x00\x00\x00interest rate\x00\x00\x00L\x00\x00\x00labor input\x00K\x00\x00\x00capital input\x00\x00\x00\x01\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff0\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x07\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\x01\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00\xfd\xff\xff\xff\x01\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\xfe\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfb\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfa\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf9\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf6\xf6\xf6\xf6\x06\x00\x00\x00\x00\x00\x00\x00\xf7\xf7\xf7\xf7\xcd\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x110\x02\x00,\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00.\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00 \x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00kIW-\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x00\x0e\x00\x00\x00\x01\x00\x00\x00-\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x0c\x00\x10\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x08\x00\x00\x00\x1c\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


@pytest.fixture
def sas_dataset(filepath_sas, fs_args):
    return GenericDataset(
        filepath=filepath_sas.as_posix(),
        file_format="sas",
        load_args={"format": "sas7bdat"},
        fs_args=fs_args,
    )


@pytest.fixture
def html_dataset(filepath_html, fs_args):
    return GenericDataset(
        filepath=filepath_html.as_posix(),
        file_format="html",
        fs_args=fs_args,
        save_args={"index": False},
    )


@pytest.fixture
def sas_dataset_bad_config(filepath_sas, fs_args):
    return GenericDataset(
        filepath=filepath_sas.as_posix(),
        file_format="sas",
        load_args={},  # SAS reader requires a type param
        fs_args=fs_args,
    )


@pytest.fixture
def versioned_csv_dataset(filepath_csv, load_version, save_version):
    return GenericDataset(
        filepath=filepath_csv.as_posix(),
        file_format="csv",
        version=Version(load_version, save_version),
        save_args={"index": False},
    )


@pytest.fixture
def csv_dataset(filepath_csv):
    return GenericDataset(
        filepath=filepath_csv.as_posix(),
        file_format="csv",
        save_args={"index": False},
    )


@pytest.fixture
def dummy_dataframe():
    return pd.DataFrame({"col1": [1, 2], "col2": [4, 5], "col3": [5, 6]})


@pytest.mark.parametrize(
    "module_name", ["kedro_datasets.pandas", "kedro_datasets.pandas.generic_dataset"]
)
@pytest.mark.parametrize("class_name", _DEPRECATED_CLASSES)
def test_deprecation(module_name, class_name):
    with pytest.warns(DeprecationWarning, match=f"{repr(class_name)} has been renamed"):
        getattr(importlib.import_module(module_name), class_name)


class TestGenericSASDataset:
    def test_load(self, sas_binary, sas_dataset, filepath_sas):
        filepath_sas.write_bytes(sas_binary)
        df = sas_dataset.load()
        assert df.shape == (32, 6)

    def test_save_fail(self, sas_dataset, dummy_dataframe):
        pattern = (
            "Unable to retrieve 'pandas.DataFrame.to_sas' method, please ensure that your "
            "'file_format' parameter has been defined correctly as per the Pandas API "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html"
        )
        with pytest.raises(DatasetError, match=pattern):
            sas_dataset.save(dummy_dataframe)
        # Pandas does not implement a SAS writer

    def test_bad_load(self, sas_dataset_bad_config, sas_binary, filepath_sas):
        # SAS reader requires a format param e.g. sas7bdat
        filepath_sas.write_bytes(sas_binary)
        pattern = "you must specify a format string"
        with pytest.raises(DatasetError, match=pattern):
            sas_dataset_bad_config.load()

    @pytest.mark.parametrize(
        "filepath,instance_type,credentials",
        [
            ("s3://bucket/file.sas7bdat", S3FileSystem, {}),
            ("file:///tmp/test.sas7bdat", LocalFileSystem, {}),
            ("/tmp/test.sas7bdat", LocalFileSystem, {}),
            ("gcs://bucket/file.sas7bdat", GCSFileSystem, {}),
            ("https://example.com/file.sas7bdat", HTTPFileSystem, {}),
            (
                "abfs://bucket/file.sas7bdat",
                AzureBlobFileSystem,
                {"account_name": "test", "account_key": "test"},
            ),
        ],
    )
    def test_protocol_usage(self, filepath, instance_type, credentials):
        dataset = GenericDataset(
            filepath=filepath, file_format="sas", credentials=credentials
        )
        assert isinstance(dataset._fs, instance_type)

        path = filepath.split(PROTOCOL_DELIMITER, 1)[-1]

        assert str(dataset._filepath) == path
        assert isinstance(dataset._filepath, PurePosixPath)

    def test_catalog_release(self, mocker):
        fs_mock = mocker.patch("fsspec.filesystem").return_value
        filepath = "test.csv"
        dataset = GenericDataset(filepath=filepath, file_format="sas")
        assert dataset._version_cache.currsize == 0  # no cache if unversioned
        dataset.release()
        fs_mock.invalidate_cache.assert_called_once_with(filepath)
        assert dataset._version_cache.currsize == 0


class TestGenericCSVDatasetVersioned:
    def test_version_str_repr(self, filepath_csv, load_version, save_version):
        """Test that version is in string representation of the class instance
        when applicable."""
        filepath = filepath_csv.as_posix()
        ds = GenericDataset(filepath=filepath, file_format="csv")
        ds_versioned = GenericDataset(
            filepath=filepath,
            file_format="csv",
            version=Version(load_version, save_version),
        )
        assert filepath in str(ds)
        assert filepath in str(ds_versioned)
        ver_str = f"version=Version(load={load_version}, save='{save_version}')"
        assert ver_str in str(ds_versioned)
        assert "GenericDataset" in str(ds_versioned)
        assert "GenericDataset" in str(ds)
        assert "protocol" in str(ds_versioned)
        assert "protocol" in str(ds)

    def test_save_and_load(self, versioned_csv_dataset, dummy_dataframe):
        """Test that saved and reloaded data matches the original one for
        the versioned data set."""
        versioned_csv_dataset.save(dummy_dataframe)
        reloaded_df = versioned_csv_dataset.load()
        assert_frame_equal(dummy_dataframe, reloaded_df)

    def test_multiple_loads(self, versioned_csv_dataset, dummy_dataframe, filepath_csv):
        """Test that if a new version is created mid-run, by an
        external system, it won't be loaded in the current run."""
        versioned_csv_dataset.save(dummy_dataframe)
        versioned_csv_dataset.load()
        v1 = versioned_csv_dataset.resolve_load_version()

        sleep(0.5)
        # force-drop a newer version into the same location
        v_new = generate_timestamp()
        GenericDataset(
            filepath=filepath_csv.as_posix(),
            file_format="csv",
            version=Version(v_new, v_new),
        ).save(dummy_dataframe)

        versioned_csv_dataset.load()
        v2 = versioned_csv_dataset.resolve_load_version()

        assert v2 == v1  # v2 should not be v_new!
        ds_new = GenericDataset(
            filepath=filepath_csv.as_posix(),
            file_format="csv",
            version=Version(None, None),
        )
        assert (
            ds_new.resolve_load_version() == v_new
        )  # new version is discoverable by a new instance

    def test_multiple_saves(self, dummy_dataframe, filepath_csv):
        """Test multiple cycles of save followed by load for the same dataset"""
        ds_versioned = GenericDataset(
            filepath=filepath_csv.as_posix(),
            file_format="csv",
            version=Version(None, None),
        )

        # first save
        ds_versioned.save(dummy_dataframe)
        first_save_version = ds_versioned.resolve_save_version()
        first_load_version = ds_versioned.resolve_load_version()
        assert first_load_version == first_save_version

        # second save
        sleep(0.5)
        ds_versioned.save(dummy_dataframe)
        second_save_version = ds_versioned.resolve_save_version()
        second_load_version = ds_versioned.resolve_load_version()
        assert second_load_version == second_save_version
        assert second_load_version > first_load_version

        # another dataset
        ds_new = GenericDataset(
            filepath=filepath_csv.as_posix(),
            file_format="csv",
            version=Version(None, None),
        )
        assert ds_new.resolve_load_version() == second_load_version

    def test_release_instance_cache(self, dummy_dataframe, filepath_csv):
        """Test that cache invalidation does not affect other instances"""
        ds_a = GenericDataset(
            filepath=filepath_csv.as_posix(),
            file_format="csv",
            version=Version(None, None),
        )
        assert ds_a._version_cache.currsize == 0
        ds_a.save(dummy_dataframe)  # create a version
        assert ds_a._version_cache.currsize == 2

        ds_b = GenericDataset(
            filepath=filepath_csv.as_posix(),
            file_format="csv",
            version=Version(None, None),
        )
        assert ds_b._version_cache.currsize == 0
        ds_b.resolve_save_version()
        assert ds_b._version_cache.currsize == 1
        ds_b.resolve_load_version()
        assert ds_b._version_cache.currsize == 2

        ds_a.release()

        # dataset A cache is cleared
        assert ds_a._version_cache.currsize == 0

        # dataset B cache is unaffected
        assert ds_b._version_cache.currsize == 2

    def test_no_versions(self, versioned_csv_dataset):
        """Check the error if no versions are available for load."""
        pattern = r"Did not find any versions for GenericDataset\(.+\)"
        with pytest.raises(DatasetError, match=pattern):
            versioned_csv_dataset.load()

    def test_exists(self, versioned_csv_dataset, dummy_dataframe):
        """Test `exists` method invocation for versioned data set."""
        assert not versioned_csv_dataset.exists()
        versioned_csv_dataset.save(dummy_dataframe)
        assert versioned_csv_dataset.exists()

    def test_prevent_overwrite(self, versioned_csv_dataset, dummy_dataframe):
        """Check the error when attempting to override the data set if the
        corresponding Generic (csv) file for a given save version already exists."""
        versioned_csv_dataset.save(dummy_dataframe)
        pattern = (
            r"Save path \'.+\' for GenericDataset\(.+\) must "
            r"not exist if versioning is enabled\."
        )
        with pytest.raises(DatasetError, match=pattern):
            versioned_csv_dataset.save(dummy_dataframe)

    @pytest.mark.parametrize(
        "load_version", ["2019-01-01T23.59.59.999Z"], indirect=True
    )
    @pytest.mark.parametrize(
        "save_version", ["2019-01-02T00.00.00.000Z"], indirect=True
    )
    def test_save_version_warning(
        self, versioned_csv_dataset, load_version, save_version, dummy_dataframe
    ):
        """Check the warning when saving to the path that differs from
        the subsequent load path."""
        pattern = (
            rf"Save version '{save_version}' did not match load version "
            rf"'{load_version}' for GenericDataset\(.+\)"
        )
        with pytest.warns(UserWarning, match=pattern):
            versioned_csv_dataset.save(dummy_dataframe)

    def test_versioning_existing_dataset(
        self, csv_dataset, versioned_csv_dataset, dummy_dataframe
    ):
        """Check the error when attempting to save a versioned dataset on top of an
        already existing (non-versioned) dataset."""
        csv_dataset.save(dummy_dataframe)
        assert csv_dataset.exists()
        assert csv_dataset._filepath == versioned_csv_dataset._filepath
        pattern = (
            f"(?=.*file with the same name already exists in the directory)"
            f"(?=.*{versioned_csv_dataset._filepath.parent.as_posix()})"
        )
        with pytest.raises(DatasetError, match=pattern):
            versioned_csv_dataset.save(dummy_dataframe)

        # Remove non-versioned dataset and try again
        Path(csv_dataset._filepath.as_posix()).unlink()
        versioned_csv_dataset.save(dummy_dataframe)
        assert versioned_csv_dataset.exists()


class TestGenericHTMLDataset:
    def test_save_and_load(self, dummy_dataframe, html_dataset):
        html_dataset.save(dummy_dataframe)
        df = html_dataset.load()
        assert_frame_equal(dummy_dataframe, df[0])


class TestBadGenericDataset:
    def test_bad_file_format_argument(self):
        ds = GenericDataset(filepath="test.kedro", file_format="kedro")

        pattern = (
            "Unable to retrieve 'pandas.read_kedro' method, please ensure that your 'file_format' "
            "parameter has been defined correctly as per the Pandas API "
            "https://pandas.pydata.org/docs/reference/io.html"
        )

        with pytest.raises(DatasetError, match=pattern):
            _ = ds.load()

        pattern2 = (
            "Unable to retrieve 'pandas.DataFrame.to_kedro' method, please ensure that your 'file_format' "
            "parameter has been defined correctly as per the Pandas API "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html"
        )
        with pytest.raises(DatasetError, match=pattern2):
            ds.save(pd.DataFrame([1]))

    @pytest.mark.parametrize(
        "file_format",
        [
            "clipboard",
            "sql_table",
            "sql",
            "numpy",
            "records",
        ],
    )
    def test_generic_no_filepaths(self, file_format):
        error = (
            "Cannot create a dataset of file_format "
            f"'{file_format}' as it does not support a filepath target/source"
        )

        with pytest.raises(DatasetError, match=error):
            _ = GenericDataset(
                filepath="/file/thing.file", file_format=file_format
            ).load()
        with pytest.raises(DatasetError, match=error):
            GenericDataset(filepath="/file/thing.file", file_format=file_format).save(
                pd.DataFrame([1])
            )
