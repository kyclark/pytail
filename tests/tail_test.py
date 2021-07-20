""" Tests for tail.py """

import os
import re
import string
import random
from subprocess import getstatusoutput
from typing import List

PRG = './tail.py'
BUSTLE = './tests/inputs/the-bustle.txt'
SPIDERS = './tests/inputs/spiders.txt'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_no_args() -> None:
    """ Dies on no args """

    retval, out = getstatusoutput(PRG)
    assert retval != 0
    assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_bad_file() -> None:
    """ Die on missing input """

    bad = random_filename()
    retval, out = getstatusoutput(f'{PRG} {bad}')
    assert retval == 0
    assert re.search(f'{bad} is not a file', out)


# --------------------------------------------------
def run(args: List[str], expected_file: str) -> None:
    """ Runs """

    assert os.path.isfile(expected_file)

    rv, out = getstatusoutput(f"{PRG} {' '.join(args)}")
    assert rv == 0
    assert out == open(expected_file).read().rstrip()


# --------------------------------------------------
def test_spiders_n1() -> None:
    """ Test spiders """

    run(['-n', '1', SPIDERS], 'tests/expected/spiders.txt.n1.out')


# --------------------------------------------------
def test_spiders_n3() -> None:
    """ Test spiders """

    run(['-n', '3', SPIDERS], 'tests/expected/spiders.txt.n3.out')


# --------------------------------------------------
def random_filename() -> str:
    """ Generate a random filename """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
