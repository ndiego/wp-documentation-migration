# Suites

A suite is a separate site for shots that cannot share the default one: the Classic Editor and classic widgets, a
classic default theme, a "broken plugin" site for recovery mode, a static front page, and so on.

- One folder per suite: `suites/<name>/blueprint.json`. A shot selects it with `suite: <name>`; the default suite
  is `../blueprint.json`.
- Same contract as the default suite (see `../README.md`): Blueprint v1, versions pinned in `preferredVersions`, a
  `login` step for `admin` / `password`, the mu-plugin installed from a bundled file, and no run-time network.
- Bundled paths are relative to the suite's own `blueprint.json`, so a suite either keeps its own copies of the
  files it needs or is generated from the default blueprint by a script. Do not use `../` in bundled paths.
- Give each suite a short `README.md` listing what it changes and any slugs it promises beyond (or instead of) the
  default content pack.

There are no suites yet.
