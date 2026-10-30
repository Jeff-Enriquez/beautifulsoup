"""Rename every <b> tag to <blockquote> and write the tree to a file.

Usage: python3 task6.py <input.html|input.xml> [output]

Task 6: a SoupReplacer is passed to the BeautifulSoup constructor as the
replacer argument. The replacer is configured with a name_xformer
function: while parsing, every tag whose name is <b> is created with the
name <blockquote> instead, keeping its attributes and children. The
modified tree is then written back to disk.
"""

import argparse
import os
import typing

import bs4


def main() -> None:
    """Run the <b>-to-<blockquote> rename from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Change <b> tags to <blockquote>.')
    parser.add_argument('input', help='HTML or XML file to parse')
    parser.add_argument('output', nargs='?', help='Output file path')
    args: argparse.Namespace = parser.parse_args()

    input_handle: typing.TextIO
    with open(args.input, encoding='utf-8') as input_handle:
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
            input_handle.read(), 'xml' if args.input.endswith('.xml') else 'lxml',
            replacer=bs4.SoupReplacer(
                name_xformer=lambda tag: ('blockquote'
                                          if tag.name == 'b' else tag.name)))

    blockquote_tags: bs4.ResultSet = soup.find_all('blockquote')

    output_path: str
    if args.output is None:
        stem: str
        extension: str
        stem, extension = os.path.splitext(args.input)
        output_path = f'{stem}_task6{extension}'
    else:
        output_path = args.output
    output_handle: typing.TextIO
    with open(output_path, 'w', encoding='utf-8') as output_handle:
        output_handle.write(str(soup))

    print(f'Renamed {len(blockquote_tags)} <b> tag(s) to <blockquote>.')
    print(f'Wrote modified tree to {output_path}')


if __name__ == '__main__':
    main()
