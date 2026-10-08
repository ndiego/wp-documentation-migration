---
title: Twenty Twenty-Five changelog
slug: twenty-twenty-five-changelog
position: 1
original_url: https://wordpress.org/documentation/article/twenty-twenty-five-changelog/
wp_id: 16360853
legacy_categories:
- customization
- default-themes
date: '2024-11-12T21:47:35'
modified: '2026-05-21T05:08:28'
migration:
  status: clean
  counts:
    preserved_heading_anchors: 6
    version_links_kept_absolute: 3
---

# Twenty Twenty-Five changelog

<a id="Version_1.5"></a>

## Version 1.5

May 20, 2026 with [WordPress 7.0](https://wordpress.org/documentation/wordpress-version/version-7-0/)

-   Exclude sticky posts in templates that have multiple Query blocks with offsets, to prevent repeating sticky posts in each query. ([#62975](https://core.trac.wordpress.org/ticket/62975))
-   Remove the text color setting in the ‘Written by’ pattern, and inherit color from a parent element, to avoid potential problems with very low color contrast. ([#62982](https://core.trac.wordpress.org/ticket/62982))
-   Update Fira Sans font for the theme, to resolve rendering issues with the backtick character. ([#63964](https://core.trac.wordpress.org/ticket/63964))
-   Documentation: Remove redundant comments for conditionally-defined functions. ([#64265](https://core.trac.wordpress.org/ticket/64265))

<a id="Version_1.4"></a>

## Version 1.4

Released: December 3, 2025 with [WordPress 6.9](https://wordpress.org/documentation/wordpress-version/version-6-9/)

-   Introduce minification for `style.css`. ([#63012](https://core.trac.wordpress.org/ticket/63012))
-   Add `path` data to the theme stylesheet so it can be inlined, to avoid a render-blocking external stylesheet. ([#63007](https://core.trac.wordpress.org/ticket/63007))
-   Prevent `pre` elements from overflowing their container by setting the element’s `overflow-x` to `auto`. ([#63875](https://core.trac.wordpress.org/ticket/63875))
-   Remove redundant `echo` from `esc_html_e()` in the ‘Cover with big heading’ block pattern. ([#63345](https://core.trac.wordpress.org/ticket/63345))
-   Fix typo in font credit URL protocol. ([#63747](https://core.trac.wordpress.org/ticket/63747))

<a id="Version_1.3"></a>

## Version 1.3

Released: August 5, 2025

-   Ensure editor styles are enqueued, using a relative path in `add_editor_style()` instead of a full URL. [#63399](https://core.trac.wordpress.org/ticket/63399)

<a id="Version_1.2"></a>

## Version 1.2

Released: April 15, 2025 with [WordPress 6.8](https://wordpress.org/documentation/wordpress-version/version-6-8/)

-   Improve text strings for patterns and templates. [#62482](https://core.trac.wordpress.org/ticket/62482)

<a id="Version_1.1"></a>

## Version 1.1

Released: February 11, 2025

-   Pin a `theme.json` schema version to Twenty Twenty-Five ([#62455](https://core.trac.wordpress.org/ticket/62455))

<a id="Version_1.0"></a>

## Version 1.0

Released: November 12, 2024

Initial Release.
