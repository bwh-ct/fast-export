## Fudge user ids filter

This plugin automatically fixes committer (Mercurial user) and author
ids that `git fast-import` considers invalid, e.g. `name
<email@example.com` or `name> email@example.com`.

This can be useful in automated conversions where configuring
`hg-fast-export` for a specific repository is not practical.  Normally
you should use an author map to fix invalid ids instead.

To use the plugin, add `--plugin fudge_author_ids`.
