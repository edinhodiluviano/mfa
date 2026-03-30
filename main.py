#!/usr/bin/env python3

import datetime as dt
import os
import stat
import sys
from pathlib import Path

import fire
import pyotp
import pyperclip


def _load(filename: str = '.env') -> dict:
    """Loads 2fa codes from file to a dict"""
    if not os.path.isabs(filename):
        filename = os.path.dirname(os.path.realpath(__file__)) + '/' + filename

    file = Path(filename)
    with open(file) as f:
        d = {
            line.split('=')[0]: line.split('=')[1].strip('\n')
            for line in f
            if line.strip('\n') != ''
        }
    return d


def get_code(name: str):
    """Print the OTP code to screen and put it into memory."""

    tokens = _load()

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


def gen_scripts(dest: Path = Path('.')):
    python_path = sys.executable
    this_file = os.path.realpath(__file__)
    this_folder = os.path.dirname(this_file)
    this_file = Path(this_folder) / this_file
    token = _load()
    for key in token.keys():
        filename = dest / f'mfa_{key}'
        contents = f'{python_path} {this_file} get_code {key}'
        with open(filename, 'w') as f:
            f.write(contents)
        os.chmod(filename, 0o700)


if __name__ == '__main__':
    fire.Fire({
        'gen_scripts': gen_scripts,
        'get_code': get_code,
    })
