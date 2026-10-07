---
title: Title block
slug: title-block
original_url: https://wordpress.org/documentation/article/title-block/
wp_id: 16365943
categories:
- customization
- theme-blocks
date: '2025-08-02T06:07:44'
modified: '2026-06-29T20:21:19'
migration:
  status: clean
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  counts:
    callouts: 2
    callouts_info: 2
    code_links_swapped: 1
    images: 2
    images_missing_alt: 1
    internal_links_rewritten: 4
  first_paragraph_is_nav_link: true
---

# Title block

[Go to the List of Blocks](../block-editor/blocks-list.md)

Title block (formerly known as Post Title block) displays the title of a post or page. This block is primarily nested inside a [query loop](query-loop-block.md) block and helps to customize the appearance of the query loop.

![Title block in the Query Loop block.](../../assets/images/2025/08/title-6.8-1.jpg)

> [!NOTE]
> See [here](../block-editor/work-with-blocks.md) for a description of how to use blocks in general and each component such as toolbars, settings panel, etc.

## Block settings

![](../../assets/images/2025/08/title-settings-6.8.jpg)

*Screenshot*

### Settings

#### Make title a link

It links the title to the URL of the post or page. This enables the website visitor to go to the page by clicking on the Title.

#### Open in new tab

It opens the linked page in a separate browser tab.

#### Link Rel

It controls the page link’s [`rel`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel) attribute (the relationship between the current document and the linked document), for adding nofollow amongst other things.

#### Advanced

The following Advanced settings options are available: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings.](../block-editor/advanced-settings-overview.md)

## Changelog

-   Updated 2026-06-29
    -   Linked to advanced settings
-   2025-08-02
    -   Renamed to Title block from Post Title block
-   2023-07-25
    -   Fix broken images URLs
-   2022-12-12
    -   Updated screenshots for 6.1
-   Created 2022-03-17
