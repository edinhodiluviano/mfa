import os
from unittest.mock import patch
import textwrap

import pyotp
import pyperclip
import pytest

import main


@pytest.fixture
def mock_file(tmp_path):
    tmp_file_dir = tmp_path / 'test_dir'
    tmp_file_dir.mkdir()
    tmp_file = tmp_file_dir / 'test_env'
    contents = textwrap.dedent("""
        a=66666666666666666666666666666666
        b=CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
        c_raw=abc
    """)
    with open(tmp_file, 'w') as f:
        f.write(contents)
    yield str(tmp_file)


@pytest.fixture(autouse=True)
def mock_load(mock_file):
    original_load = main._load
    with patch('main._load') as m:
        m.return_value = original_load(mock_file)
        yield


def test_read_lines_return_list_with_correct_content():
    r = main._read_lines(filename='env_template')
    expected = [
        'github=55555555555555555555555555555555',
        'google=55555555555555555555555555555555',
    ]
    assert r == expected


def test_load_return_dict():
    r = main._load()
    assert type(r) == dict


def test_load_return_dict_with_code_a():
    r = main._load()
    assert 'a' in r


def test_load_return_dict_with_len_2():
    r = main._load()
    assert len(r) == 3


def test_get_code_returns_string():
    given = main.get_code('a')
    assert type(given) == str


def test_get_code_returns_expected_result_for_raw():
    given = main.get_code('c_raw')
    assert given == 'abc'


def test_get_code_returns_expected_result_for_a():
    given = main.get_code('a')
    expected = pyotp.TOTP('66666666666666666666666666666666').now()
    assert given == expected


def test_get_code_put_result_in_clipboard_for_a():
    expected = main.get_code('a')
    given = pyperclip.paste()
    assert given == expected


def test_gen_scripts_returns_none(tmp_path):
    r = main.gen_scripts(dest=tmp_path)
    assert r is None


def test_gen_scripts_create_3_files(tmp_path):
    tmp_dest = tmp_path / 'destination'
    tmp_dest.mkdir()
    main.gen_scripts(dest=tmp_dest)
    files = os.listdir(tmp_dest)
    assert set(files) == {'mfa_a', 'mfa_b', 'mfa_c_raw'}
