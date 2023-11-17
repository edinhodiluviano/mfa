import pyotp
import pyperclip

import main


def mock_read_lines():
    return [
        'a=66666666666666666666666666666666',
        'b=CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
        'c_raw=abc',
    ]


def mock_load():
    return main._load(mock_read_lines)


def test_read_lines_return_list_with_correct_content():
    r = main._read_lines(filename='.env_sample')
    expected = [
        'github=55555555555555555555555555555555',
        'google=55555555555555555555555555555555',
    ]
    assert r == expected


def test_load_return_dict():
    r = main._load(mock_read_lines)
    assert type(r) == dict


def test_load_return_dict_with_code_a():
    r = main._load(mock_read_lines)
    assert 'a' in r


def test_load_return_dict_with_len_2():
    r = main._load(mock_read_lines)
    assert len(r) == 3


def test_get_code_returns_string():
    given = main.get_code('a', mock_load)
    assert type(given) == str


def test_get_code_returns_expected_result_for_raw():
    given = main.get_code('c_raw', mock_load)
    assert given == 'abc'


def test_get_code_returns_expected_result_for_a():
    given = main.get_code('a', mock_load)
    expected = pyotp.TOTP('66666666666666666666666666666666').now()
    assert given == expected


def test_get_code_put_result_in_clipboard_for_a():
    expected = main.get_code('a', mock_load)
    given = pyperclip.paste()
    assert given == expected
