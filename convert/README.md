# convert

`wp_markdown.py` is the interface every handbook conversion goes through. The converter core (WordPress block-markup
pre-pass plus a markdownify subclass that GitHub and Jetpack's PHP Markdown Extra render identically) lives in
`../scripts/convert.py`, entangled with the HelpHub pipeline; this facade loads it and exposes only the generic
calls, so extracting the core later changes nothing for callers.

It lived in the documentation-toolkit repo (`toolkit/convert/`) until that repo's 0.2.0 restructure. Conversion is a
one-time migration step rather than documentation maintenance, so it moved back here with the pipeline it wraps.
Another handbook that needs to convert points `WP_MARKDOWN_CORE` at this repo's `scripts/convert.py`, or runs the
conversion from a checkout of this repo.

```python
import sys; sys.path.insert(0, "convert")
import wp_markdown as wm
md, report = wm.html_to_markdown(html, slug="getting-started", base_url="https://developer.wordpress.org")
```

`report` carries warnings, info, counts (images, missing alt, links made absolute, …) and the heading ids assigned.
Callout styles: `gfm-alert` (default, the cross-handbook convention in `toolkit/style/CONVENTIONS.md`), `gutenberg`
(raw callout divs, the Block Editor's current style), `shortcode` (`[info]`… what DevHub renders natively; the Theme
Handbook spike used it to prove byte-identical notices).

A handbook layer adds its own link rewriting, image policy and heading-id handling by patching the core the way
`notes/theme-handbook-migration/spike/scripts/convert_theme.py` does. Those patches are handbook-specific and do not
belong in the facade. Dependencies: `beautifulsoup4`, `markdownify`, `pyyaml` (the repo's `.venv`).
