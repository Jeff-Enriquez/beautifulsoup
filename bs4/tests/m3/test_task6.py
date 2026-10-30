"""Unit tests for task6.py and the SoupReplacer API."""

import sys
import unittest
from pathlib import Path

import bs4

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import run_task  # noqa: E402


class Task6Tests(unittest.TestCase):
    def _run_and_report(self, name):
        returncode, seconds, peak_kib, stderr = run_task('task6.py', name)
        if seconds is not None and peak_kib is not None:
            print(f'{name}: {seconds:.2f}s, '
                  f'peak RSS {peak_kib / 1024 ** 2:.2f} GiB')
        else:
            print(f'{name}: did not complete')
        self.assertIsNotNone(seconds, 'missing ELAPSED_SECONDS in output')
        self.assertIsNotNone(peak_kib, 'missing PEAK_RSS_KIB in output')
        self.assertEqual(
            returncode, 0,
            f'task6.py failed on {name} (memory limit or crash):\n{stderr}')

    def test_giga_html(self):
        self._run_and_report('giga.html')

    def test_medium1_html(self):
        self._run_and_report('medium1.html')

    def test_large1_html(self):
        self._run_and_report('large1.html')


class SoupReplacerTests(unittest.TestCase):
    def test_name_xformer_renames_tag_during_parse(self):
        html = ('<html><body><p>Some <b class="bold" id="x">bold</b> '
                'text</p></body></html>')
        replacer = bs4.SoupReplacer(
            name_xformer=lambda tag: ('blockquote'
                                      if tag.name == 'b' else tag.name))
        soup = bs4.BeautifulSoup(html, 'lxml', replacer=replacer)
        self.assertIsNone(soup.find('b'))
        blockquote = soup.find('blockquote')
        self.assertIsNotNone(blockquote)
        self.assertEqual(blockquote.get('class'), ['bold'])
        self.assertEqual(blockquote.get('id'), 'x')
        self.assertEqual(blockquote.get_text(), 'bold')

    def test_name_xformer_returning_none_keeps_name(self):
        html = '<html><body><p>para</p><b>bold</b></body></html>'
        replacer = bs4.SoupReplacer(name_xformer=lambda tag: None)
        soup = bs4.BeautifulSoup(html, 'lxml', replacer=replacer)
        self.assertIsNotNone(soup.find('p'))
        self.assertIsNotNone(soup.find('b'))
        self.assertIsNone(soup.find('blockquote'))

    def test_name_xformer_leaves_nonmatching_tags_unchanged(self):
        html = ('<html><body><strong class="bold">strong</strong> '
                '<b>bold</b></body></html>')
        replacer = bs4.SoupReplacer(
            name_xformer=lambda tag: ('blockquote'
                                      if tag.name == 'b' else tag.name))
        soup = bs4.BeautifulSoup(html, 'lxml', replacer=replacer)
        self.assertIsNotNone(soup.find('strong'))
        self.assertEqual(soup.find('strong').get('class'), ['bold'])
        self.assertIsNone(soup.find('b'))
        self.assertIsNotNone(soup.find('blockquote'))
        self.assertEqual(soup.find('blockquote').get_text(), 'bold')


if __name__ == '__main__':
    unittest.main()
