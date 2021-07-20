#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-07-20
Purpose: Python tail
"""

import argparse
import gzip
import os
import sys
from itertools import islice
from typing import Generator, List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    num_lines: int


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Python tail',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-n',
                        '--num_lines',
                        help='Number of lines',
                        metavar='int',
                        type=int,
                        default=10)

    parser.add_argument('file',
                        help='Input file(s)',
                        metavar='FILE',
                        nargs='+')

    args = parser.parse_args()

    return Args(args.file, args.num_lines)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    num_files = len(args.files)

    for file_num, filename in enumerate(args.files, start=1):
        if not os.path.isfile(filename):
            print(f'{filename} is not a file', file=sys.stderr)
            continue

        ext = os.path.splitext(filename)[1]
        try:
            fh = gzip.open(file, 'rb') if ext == '.gz' else open(
                filename, 'rb')

            if num_files > 1:
                print('{}==> {} <=='.format('\n' if file_num > 1 else '',
                                            filename))

            if lines := list(islice(read_backwards(fh), args.num_lines)):
                print('\n'.join(reversed(lines)))

        except Exception as e:
            print(e, file=sys.stderr)
            continue


# --------------------------------------------------
def read_backwards(fh: TextIO) -> Generator[str, None, None]:
    """ Read file backwards """

    buffer = bytearray()
    pos = fh.seek(0, os.SEEK_END)

    while True:
        new_pos = pos - 1
        if new_pos < 0:
            break

        pos = fh.seek(new_pos)
        byte = fh.read(1)
        if byte == b'\n':
            if buffer:
                yield buffer.decode()[::-1]
                buffer = bytearray()
        else:
            buffer.extend(byte)

    if buffer:
        yield buffer.decode()[::-1]


# --------------------------------------------------
if __name__ == '__main__':
    main()
