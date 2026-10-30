"""Add one class to every <p> tag and optionally remove another, then write the tree to a file.

Usage:
    python3 task7.py <input.html|input.xml> [class_attribute1] [class_attribute2] [-o output]

Task 7: give every <p> tag the class `class_attribute1` (default `test`),
keeping any other classes it already has. If `class_attribute2` names a
class, remove that class from every <p> tag first. If `class_attribute2`
is `*`, clear every class on every <p> tag before adding
`class_attribute1`. The modified tree is then written back to disk.

Unlike the Milestone 1 version, the changes are made *during* parsing by
passing a `bs4.SoupReplacer` to the `BeautifulSoup` constructor as the
`replacer` argument. The replacer is configured with an `xformer` function
that edits every `<p>` tag in place as it is parsed, instead of editing
every <p> tag after the full tree is built.

Examples:
    task7.py input.html               -> <p class="liquid"> becomes
                                          <p class="liquid test">
    task7.py input.html money          -> <p class="liquid"> becomes
                                          <p class="liquid money">
    task7.py input.html money liquid   -> <p class="liquid"> becomes
                                          <p class="money">
    task7.py input.html world "*"      -> <p class="liquid money"> becomes
                                          <p class="world">
"""

import argparse
import os
import typing

import bs4


def main() -> None:
    """Run the class-updating task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Add a class to every <p> tag, optionally removing another.')
    parser.add_argument('input', help='HTML or XML file to parse')
    parser.add_argument('class_attribute1', nargs='?', default='test',
                        help='Class to add to every <p> tag (default: test)')
    parser.add_argument('class_attribute2', nargs='?', default=None,
                        help='Class to remove from every <p> tag; "*" clears '
                             'all classes')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file path')
    args: argparse.Namespace = parser.parse_args()

    def transform_p_tag(tag: bs4.Tag) -> None:
        """Add class_attribute1 to a <p> tag, removing class_attribute2 first."""
        if tag.name != 'p':
            return

        value = tag.get('class')
        if value is None:
            classes: list[str] = []
        elif isinstance(value, str):
            classes = value.split()
        else:
            classes = list(value)

        if args.class_attribute2 == '*':
            classes = []
        elif args.class_attribute2 is not None:
            classes = [cls for cls in classes if cls != args.class_attribute2]

        if args.class_attribute1 not in classes:
            classes.append(args.class_attribute1)

        if classes:
            tag['class'] = classes
        elif 'class' in tag.attrs:
            del tag.attrs['class']

    input_handle: typing.TextIO
    with open(args.input, encoding='utf-8') as input_handle:
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
            input_handle.read(), 'xml' if args.input.endswith('.xml') else 'lxml',
            replacer=bs4.SoupReplacer(xformer=transform_p_tag))

    paragraphs: bs4.ResultSet = soup.find_all('p')

    output_path: str
    if args.output is None:
        stem: str
        extension: str
        stem, extension = os.path.splitext(args.input)
        output_path = f'{stem}_task7{extension}'
    else:
        output_path = args.output
    output_handle: typing.TextIO
    with open(output_path, 'w', encoding='utf-8') as output_handle:
        output_handle.write(str(soup))

    print(f'Added class "{args.class_attribute1}" '
          f'to {len(paragraphs)} <p> tag(s).')
    if args.class_attribute2 == '*':
        print('Cleared all existing classes on every <p> tag.')
    elif args.class_attribute2 is not None:
        print(f'Removed class "{args.class_attribute2}" '
              f'from every <p> tag.')
    print(f'Wrote modified tree to {output_path}')


if __name__ == '__main__':
    main()
