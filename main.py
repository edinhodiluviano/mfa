#!/usr/bin/env python3


import os
from pathlib import Path


def _read_lines(filename: str = '.env') -> list[str]:
    file = os.path.dirname(os.path.realpath(__file__))
    file = Path(file) / filename
    text = file.read_text()
    lines = text.split('\n')
    lines = [li for li in lines if li != '']
    return lines


def _load(line_reader_func: callable = _read_lines) -> dict:
    """Loads 2fa codes from file to a dict"""
    lines = line_reader_func()
    lines = [i.split('=') for i in lines if i != '']
    d = {i[0]: i[1] for i in lines}
    return d
