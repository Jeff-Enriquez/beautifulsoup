# Beautiful Soup 4 Project

[TOC]

## Milestone 1

A suite of eight command-line programs, under `apps/m1/`, that exercise the
[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) HTML/XML
parsing library. Each program takes an HTML or XML file as a command-line
argument, builds a parse tree, performs one task, and (for tasks 1, 6, and 7)
writes the modified tree back to disk. Task 8 edits the given document.

### Environment

*   Python 3.14
*   [Beautiful Soup 4.13.0](https://www.crummy.com/software/BeautifulSoup/) (regular installation from PyPI)
*   lxml 6.1.3

### Setup

From the repository root, create a virtual environment and install the
required dependencies explicitly.

#### Linux / macOS

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install beautifulsoup4==4.13.0 lxml==6.1.3
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install beautifulsoup4==4.13.0 lxml==6.1.3
```

#### Windows (Command Prompt)

```bat
py -m venv .venv
.venv\Scripts\activate.bat
pip install beautifulsoup4==4.13.0 lxml==6.1.3
```

### How to run

The scripts live in `apps/m1/` and take an input file from the test corpus
(`bs4/tests/`) as their first argument. Run them from the repository root.

```shell
python3 apps/m1/task1.py bs4/tests/small1.html [output]
python3 apps/m1/task2.py bs4/tests/small1.html
python3 apps/m1/task3.py bs4/tests/small1.html
python3 apps/m1/task4.py bs4/tests/small1.html
python3 apps/m1/task5.py bs4/tests/small1.html
python3 apps/m1/task6.py bs4/tests/small1.html [output]
python3 apps/m1/task7.py bs4/tests/small1.html [class_attribute1] [class_attribute2] [-o output]
python3 apps/m1/task8.py bs4/tests/small1.html signed_by
```

Every script accepts `.xml` files too; the XML parser is selected
automatically. When no output path is given, tasks 1, 6, and 7 write next to
the input file with a `_pretty`, `_task6`, or `_task7` suffix; task 8 signs
the input file in place.

`task7.py` takes two optional class parameters:

*   `class_attribute1` (optional, defaults to `test`) is added to every
    `<p>` tag, keeping existing classes.
*   `class_attribute2` (optional) is removed from every `<p>` tag first; the
    special value `*` clears all existing classes instead.
*   The modified tree is written to `-o output` if given, otherwise next to
    the input file with a `_task7` suffix.

```shell
python3 apps/m1/task7.py input.html             # <p class="liquid"> -> <p class="liquid test">
python3 apps/m1/task7.py input.html money        # <p class="liquid"> -> <p class="liquid money">
python3 apps/m1/task7.py input.html money liquid # <p class="liquid"> -> <p class="money">
python3 apps/m1/task7.py input.html world "*"    # <p class="liquid money"> -> <p class="world">
```

`task8.py` signs the document in place:

*   First signing: inserts
    `<!-- Created by <signed_by>. At <timestamp> -->` at the top of the
    document (right after the DOCTYPE for HTML, after the XML declaration on
    the second line for XML, or at the very top when the document has no
    DOCTYPE).
*   Later signings: appends
    `<!-- Modified by <signed_by>. At <timestamp> -->` on the line after the
    previous signature.

### The eight tasks

| File | Task | Main API used |
| --- | --- | --- |
| `task1.py` | Read a file into a tree and write the tree back to disk as a prettified file. | `BeautifulSoup(...)`, `soup.prettify()` |
| `task2.py` | Print all hyperlinks, with `href` and link text. | `soup.find_all('a')` |
| `task3.py` | Print all tags in the document (and a count summary). | `soup.find_all()` |
| `task4.py` | Print all tags that have an `id` attribute, in a single API call. | `soup.find_all(id=True)` |
| `task5.py` | Use `find_parent()` meaningfully: immediate parent, full ancestor chain, nearest enclosing `<section>`, nearest ancestor with an `id`. | `tag.find_parent()`, `tag.find_parent('section')`, `tag.find_parent(id=True)` |
| `task6.py` | Change all `<b>` tags to `<blockquote>` and write the tree to a file. | `soup.find_all('b')`, `tag.name = 'blockquote'` |
| `task7.py` | Add a class to every `<p>` tag (optionally removing another class, or clearing all classes with `*`, first) and write the tree to a file. | `soup.find_all('p')`, `tag.get('class')`, `tag['class']` |
| `task8.py` | Sign the document: insert a `Created by` (or `Modified by`) comment after the XML declaration or DOCTYPE and write the signed tree back to the file. | `bs4.Comment`, `soup.find(...)`, `soup.insert()` |

### Test corpus

`bs4/tests/` holds a corpus of 10 HTML/XML files used to exercise every task:
eight regular inputs (small, medium, large, very large, and deeply nested
documents) plus the two GB-scale experiment inputs:

| File | Kind | Size (KiB) |
| --- | --- | --- |
| `bs4/tests/small1.html` | small HTML | 0.46 |
| `bs4/tests/small2.xml` | small XML | 0.42 |
| `bs4/tests/medium1.html` | medium HTML | 282 |
| `bs4/tests/medium2.xml` | medium XML | 414 |
| `bs4/tests/large1.html` | large HTML | 2,801 |
| `bs4/tests/large2.html` | large HTML | 6,985 |
| `bs4/tests/very_large.html` | very large HTML | 70,297 |
| `bs4/tests/nested.html` | very nested HTML | 27 (1,000 nested `<div>` levels) |
| `bs4/tests/giga.html` | GB-scale experiment (synthetic HTML) | 1,049,806 |
| `bs4/tests/enwiki-20151002-pages-meta-current23.xml` | GB-scale experiment (real Wikipedia dump) | 6,078,948 |

The Wikipedia dump, `bs4/tests/enwiki-20151002-pages-meta-current23.xml`,
can be downloaded from [Internet Archive][enwiki-dump].

[enwiki-dump]: https://archive.org/download/enwiki-20151002/enwiki-20151002-pages-meta-current23.xml-p018225001p020925000.bz2

### Tests

Unit tests live under `bs4/tests/m1/`. There is one test module per task
(`test_task1.py` through `test_task8.py`), plus `test_large_files.py` for
the timing/memory experiments below.

Each `test_taskN.py` runs the corresponding `apps/m1/taskN.py` against
copies of the corpus inputs in a temporary directory and checks the exit
code, printed output, and any files written back to disk.

```shell
python3 bs4/tests/m1/test_task1.py
python3 bs4/tests/m1/test_task2.py
python3 bs4/tests/m1/test_task3.py
python3 bs4/tests/m1/test_task4.py
python3 bs4/tests/m1/test_task5.py
python3 bs4/tests/m1/test_task6.py
python3 bs4/tests/m1/test_task7.py
python3 bs4/tests/m1/test_task8.py
```

`test_large_files.py` runs `task1.py` against the five largest inputs under
a 50 GiB address-space limit and reports wall-clock time and peak RSS. It
is intentionally slow (minutes for the largest files) and writes
multi-gigabyte prettified output to a temporary directory, so it is kept
separate and run explicitly:

```shell
python3 bs4/tests/m1/test_large_files.py
```

### Very large file experiment

The five largest inputs were run through `apps/m1/task1.py` under `/usr/bin/time`
to record wall-clock time and peak resident memory (RSS). Peak RSS grows
roughly linearly with input size, at roughly 17-27x the file size:

| Input | Size (KiB) | Peak RSS (KiB) | RSS / size | Time (s) |
| --- | --- | --- | --- | --- |
| `bs4/tests/large1.html` | 2,801 | 75,824 | 27.1x | 0.54 |
| `bs4/tests/large2.html` | 6,985 | 153,584 | 22.0x | 1.32 |
| `bs4/tests/very_large.html` | 70,297 | 1,255,348 | 17.9x | 14.45 |
| `bs4/tests/giga.html` | 1,049,806 | 18,346,856 | 17.5x | 228.68 |
| `bs4/tests/enwiki-20151002-pages-meta-current23.xml` | 6,078,948 | 56,724,436 | n/a | 150.32 |

The `enwiki` run was killed by the OS out-of-memory killer (signal 9)
after 150.32 s, when RSS reached 56,724,436 KiB (~54 GiB).

#### Why peak memory is far larger than the file

`task1.py` is a whole-document tool, and several full copies of the
document coexist in memory at peak:

1.  Raw markup: the entire file is read into a single Python `str` that
    stays alive (the tree's text nodes are slices into it).
2.  lxml tree: the lxml parser builds its own C-backed tree of Python
    objects, which remains as the backing store for the soup tree.
3.  BeautifulSoup tree: every element, text node, comment, and attribute
    becomes a `bs4.element.Tag` or `NavigableString` object with dicts
    and parent/sibling pointers. The hundreds of bytes of per-node
    overhead dwarf the source text, so a dump with tens of millions of
    nodes dominates RSS.
4.  Prettified output: `soup.prettify()` materializes the entire
    reformatted document as a new string, ~20% larger than the input
    (1.07 GB in, 1.29 GB out for `giga.html`).

#### Why the enwiki run failed

Extrapolating the 17-27x scaling, the 6.2 GB Wikipedia dump would need on
the order of 100+ GB of RAM. The machine ran out of memory at ~54 GiB,
and the OS killed the process before parsing finished.

#### Do the task1 results apply to the other tasks?

Yes, with one caveat. All eight tasks share the identical bottleneck: the
entire file is read into one `str` and a full parse tree is built, which
costs 17-27x the file size and dominates peak RSS in every task. The
enwiki failure happened during parsing, before `prettify()` even ran, and
the parse phase is byte-for-byte identical across all tasks. Any file
that runs out of memory while `task1.py` parses will therefore fail every
other task at the same point.

The caveat is that `prettify()` adds one extra ~1.2x copy of the document
that tasks 2-5 never make, while `task3.py`'s bare `soup.find_all()`
materializes a list of every tag. A file that fails only at the very last
prettify step might barely work in `task2.py`, `task4.py`, or `task5.py`.
Because the parse tree dwarfs these extras (17-27x versus ~1.2x), a
`task1.py` failure is a strong indicator that the other tasks will fail
too, but strictly confirming it means running `task3.py` against the same
file and checking that it dies at the same stage.

## Milestone 2

A suite of command-line programs that exercise a
[fork](https://github.com/UCI-MSWE-Program/beautifulsoup4) of [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) HTML/XML
parsing library. These scripts reimplement the corresponding Milestone 1
tasks using the fork's parsing hooks — `SoupStrainer` (`parse_only`) and
`SoupReplacer` (`replacer`) — so the work happens *during* parsing instead
of after the full tree is built.

### What's here

| File | Task | Parsing hook |
| --- | --- | --- |
| `task2.py` | Print every hyperlink, with `href` and link text. | `parse_only=bs4.SoupStrainer('a')` |
| `task3.py` | Print every tag in document order, with a count summary. | `parse_only=bs4.SoupStrainer(True)` |
| `task4.py` | Print every tag that carries an `id` attribute. | `parse_only=bs4.SoupStrainer(id=True)` |
| `task6.py` | Rename every `<b>` tag to `<blockquote>` and write the tree to a file. | `replacer=bs4.SoupReplacer('b', 'blockquote')` |
| `task7.py` | Add a class to every `<p>` tag (optionally removing another class, or clearing all classes with `*`) and write the tree to a file. | `replacer=bs4.SoupReplacer('p', class_attribute1, class_attribute2)` |

`task2.py` and `task4.py` parse a strict subset of the document, so they use
far less memory than their whole-document Milestone 1 counterparts.
`task3.py` must see every tag, so `SoupStrainer(True)` matches every tag
while still skipping non-tag strings.

### Environment

*   Python 3.14
*   Fork of [Beautiful Soup 4.13.0](https://github.com/UCI-MSWE-Program/beautifulsoup4) (editable installation from the `bs4/beautifulsoup4/` git submodule)
*   lxml 6.1.3

### Cloning

Milestone 2 depends on a fork of Beautiful Soup 4 vendored as a git
submodule under `bs4/beautifulsoup4/`. Clone the repository with its submodules
included:

```shell
git clone --recurse-submodules https://github.com/UCI-MSWE-Program/uci-swe-262-project.git
```

If the repository was already cloned without the submodule, fetch it with:

```shell
git submodule update --init --recursive
```

### Setup

From the repository root, create a virtual environment and install the
dependencies listed in `requirements.txt` (the forked Beautiful Soup 4
submodule and lxml).

#### Linux / macOS

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -e ./bs4/beautifulsoup4 lxml==6.1.3
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ./bs4/beautifulsoup4 lxml==6.1.3
```

#### Windows (Command Prompt)

```bat
py -m venv .venv
.venv\Scripts\activate.bat
pip install -e ./bs4/beautifulsoup4 lxml==6.1.3
```

### How to run

The scripts live in `apps/m2/` and take an input file from the test corpus
(`bs4/tests/`) as their first argument. Run them from the repository root
with the virtual environment activated.

#### Linux / macOS

```shell
python3 apps/m2/task2.py bs4/tests/small1.html
python3 apps/m2/task3.py bs4/tests/small1.html
python3 apps/m2/task4.py bs4/tests/small1.html
python3 apps/m2/task6.py bs4/tests/small1.html
python3 apps/m2/task7.py bs4/tests/small1.html
```

#### Windows (PowerShell / Command Prompt)

```powershell
python apps\m2\task2.py bs4\tests\small1.html
python apps\m2\task3.py bs4\tests\small1.html
python apps\m2\task4.py bs4\tests\small1.html
python apps\m2\task6.py bs4\tests\small1.html
python apps\m2\task7.py bs4\tests\small1.html
```

Every script accepts `.xml` files too; the XML parser is selected
automatically. `task6.py` writes the modified tree next to the input file
with a `_task6` suffix, unless you pass an output path as a second
argument:

```shell
python3 apps/m2/task6.py bs4/tests/small1.html output.html
```

`task7.py` takes the same optional class arguments as its Milestone 1
counterpart: the class to add (default `test`) and an optional class to
remove, where `*` clears every existing class first. It writes next to the
input file with a `_task7` suffix unless you pass `-o output`:

```shell
python3 apps/m2/task7.py bs4/tests/small1.html           # add "test"
python3 apps/m2/task7.py bs4/tests/small1.html money      # add "money"
python3 apps/m2/task7.py bs4/tests/small1.html money liquid  # remove "liquid", add "money"
python3 apps/m2/task7.py bs4/tests/small1.html world "*"  # clear all classes, add "world"
```

### Tests

The unit tests under `bs4/tests/m2/` run each script against the corpus
under a 50 GiB address-space limit and report wall-clock time and peak RSS.
`test_task2.py` through `test_task6.py` each exercise both `giga.html` and
`medium1.html`. `test_task7.py` mirrors its Milestone 1 counterpart and
runs `task7.py` against the smaller corpus inputs, checking the classes
written back to disk.

#### Linux / macOS

```shell
python3 bs4/tests/m2/test_task2.py
python3 bs4/tests/m2/test_task3.py
python3 bs4/tests/m2/test_task4.py
python3 bs4/tests/m2/test_task6.py
python3 bs4/tests/m2/test_task7.py
```

#### Windows

```powershell
python bs4\tests\m2\test_task2.py
python bs4\tests\m2\test_task3.py
python bs4\tests\m2\test_task4.py
python bs4\tests\m2\test_task6.py
python bs4\tests\m2\test_task7.py
```

## Milestone 3

> For instructions on environment, cloning, or setup, please refer to 
[Milestone 2](#milestone-2).

A third suite under `apps/m3/` that reimplements the same two editing tasks
as Milestone 2 (`task6.py` and `task7.py`) using the *transformer-function*
forms of the fork's `SoupReplacer` hook, instead of the convenience
`og_tag`/`alt_tag` and `add_classes`/`remove_classes` arguments.

### What's here

| File | Task | Parsing hook |
| --- | --- | --- |
| `task6.py` | Rename every `<b>` tag to `<blockquote>` and write the tree to a file. | `replacer=bs4.SoupReplacer(name_xformer=...)` |
| `task7.py` | Add a class to every `<p>` tag (optionally removing another class, or clearing all classes with `*`) and write the tree to a file. | `replacer=bs4.SoupReplacer(xformer=...)` |

Both scripts accept `.xml` files too and share the command-line interface
of their Milestone 2 counterparts:

```shell
python3 apps/m3/task6.py bs4/tests/small1.html [output]
python3 apps/m3/task7.py bs4/tests/small1.html [class_attribute1] [class_attribute2] [-o output]
```

### Tests

Unit tests live under `bs4/tests/m3/`. `test_task6.py` runs `task6.py`
against `giga.html`, `medium1.html`, and `large1.html` under a 50 GiB
address-space limit; `test_task7.py` runs `task7.py` against the non-GB
corpus inputs and checks the classes written back to disk. Both also
unit-test the `name_xformer`/`xformer` behavior directly.

```shell
python3 bs4/tests/m3/test_task6.py
python3 bs4/tests/m3/test_task7.py
```

## See also

* [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
