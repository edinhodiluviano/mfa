#!/usr/bin/env python3

import datetime as dt
import os
from pathlib import Path

import pyotp
import pyperclip


def _read_lines(filename: str = '.env') -> list[str]:
    file = os.path.dirname(os.path.realpath(__file__))
    file = Path(file) / filename
    text = file.read_text()
    lines = text.split('\n')
    lines = [li for li in lines if li != '']
    return lines


def _load(_line_reader_func: callable = _read_lines) -> dict:
    """Loads 2fa codes from file to a dict"""
    lines = _line_reader_func()
    lines = [i.split('=') for i in lines if i != '']
    d = {i[0]: i[1] for i in lines}
    return d


def get_code(
    name: str,
    _load_func: callable = _load,
):
    """Print the OTP code to screen and put it into memory."""

    tokens = _load_func()

    if name.endswith('_raw'):
        code = tokens[name]
        print(f'{code=}')
    else:
        name = name.lower()
        key = tokens[name]
        t = pyotp.TOTP(key)
        code = t.now()

        time = dt.datetime.now().second
        time = time % 30
        time = 30 - time
        print(f'{code=} for {time} seconds')

    pyperclip.copy(code)
    return code
