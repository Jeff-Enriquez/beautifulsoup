"""Shared helpers for the milestone 2 task unit tests."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import bs4

ROOT = Path(__file__).resolve().parents[3]
APPS_DIR = ROOT / 'apps' / 'm3'
TESTS_DIR = ROOT / 'bs4' / 'tests'

LARGE_INPUTS = (
    'giga.html',
    'enwiki-20151002-pages-meta-current23.xml',
)

INPUT_FILES = (
    'small1.html',
    'small2.xml',
    'medium1.html',
    'medium2.xml',
    'large1.html',
    'large2.html',
    'very_large.html',
    'nested.html',
)

SMALL_INPUTS = (
    'small1.html',
    'small2.xml',
    'medium1.html',
    'medium2.xml',
    'nested.html',
)

MEM_LIMIT_GIB = 50
MEM_LIMIT_BYTES = MEM_LIMIT_GIB * 1024 ** 3

# Wrapper that sets the address-space limit, runs the task in a child
# process, and reports the wall-clock time and peak RSS of that child.
# The task's stdout is discarded (it is enormous for these inputs); its
# stderr is forwarded so failures can be diagnosed.
_WRAPPER = r'''
import resource
import subprocess
import sys
import time

task, input_path = sys.argv[1:3]
limit = int(sys.argv[3])
resource.setrlimit(resource.RLIMIT_AS, (limit, limit))

start = time.perf_counter()
proc = subprocess.run([sys.executable, task, input_path],
                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                      text=True)
elapsed = time.perf_counter() - start
peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print(f'ELAPSED_SECONDS={elapsed:.3f}')
print(f'PEAK_RSS_KIB={peak}')
if proc.stderr:
    sys.stderr.write(proc.stderr)
sys.exit(proc.returncode)
'''

_ELAPSED_RE = re.compile(r'ELAPSED_SECONDS=([0-9.]+)')
_PEAK_RE = re.compile(r'PEAK_RSS_KIB=(\d+)')


def run_task(script, input_name):
    """Run a task script against a corpus input under the memory limit.

    Returns a (returncode, elapsed_seconds, peak_rss_kib, stderr) tuple.
    """
    proc = subprocess.run(
        [sys.executable, '-c', _WRAPPER,
         str(APPS_DIR / script), str(TESTS_DIR / input_name),
         str(MEM_LIMIT_BYTES)],
        capture_output=True, text=True)
    elapsed = _ELAPSED_RE.search(proc.stdout)
    peak = _PEAK_RE.search(proc.stdout)
    seconds = float(elapsed.group(1)) if elapsed else None
    peak_kib = int(peak.group(1)) if peak else None
    return proc.returncode, seconds, peak_kib, proc.stderr


def copy_input(input_name, dest_dir):
    """Copy a corpus input file into dest_dir and return the new path."""
    destination = Path(dest_dir) / input_name
    shutil.copy2(TESTS_DIR / input_name, destination)
    return destination


def run_task_on_copy(script, input_name, dest_dir, *extra_args):
    """Run a task script against a copy of an input file in dest_dir."""
    copied = copy_input(input_name, dest_dir)
    command = [sys.executable, str(APPS_DIR / script), str(copied), *extra_args]
    return subprocess.run(command, capture_output=True, text=True)


def read_input(input_name):
    """Return the contents of a corpus input file as a string."""
    return (TESTS_DIR / input_name).read_text(encoding='utf-8')


def build_soup(markup, input_name):
    """Parse markup with the same parser the task scripts select."""
    parser = 'xml' if input_name.endswith('.xml') else 'lxml'
    return bs4.BeautifulSoup(markup, parser)
