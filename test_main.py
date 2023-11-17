import main


def mock_read_lines():
    return [
        'a=66666666666666666666666666666666',
        'b=CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
    ]


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
    assert len(r) == 2
