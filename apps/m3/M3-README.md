# M3-README

### Recommendation (Technical brief of SoupReplacer API)

This is a recommendation for a future refactor, not a description of the
current implementation. Today the `SoupReplacer` API has two layers — the
low-level transformer primitives added in Milestone 3, and the declarative
convenience forms from Milestone 2 — wired up as two separate code paths
in the parser.

Keep both, but make the declarative forms delegate to the transformer
primitives. Concretely:

*   Treat M3's (`name_xformer`, `attrs_xformer`, `xformer`) as the core,
    low-level API — the single mechanism the parser would invoke.
*   Treat M2's (`og_tag`, `alt_tag`) and (`tag`, `add`, `remove`) as
    thin, typed sugar that builds the equivalent transformer functions
    under the hood.

Why this shape:

*   Guidance: use the declarative forms for the 90% case
    ("rename `<b>`", "fix classes") because they're harder to misuse and
    easy to review. Reserve transformers for genuinely novel
    transformations.
*   One code path: if the convenience constructors are compiled into the
    same transformer calls the M3 path uses, there's one implementation to
    test, one place end-tag handling lives, and no drift between the two
    interfaces.
*   Room to grow: new declarative helpers can be added without touching
    the parser, while power users still get full escape-hatch control.

If we had to ship only one: ship the transformer API (M3). It is strictly
more general — the declarative forms are trivial wrappers over it, whereas
the reverse is not true. But for developer ergonomics, we should not make
our team write `lambda tag: 'blockquote' if tag.name == 'b' else tag.name`
when `SoupReplacer('b', 'blockquote')` says the same thing in one readable
line.

## See also

* [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
