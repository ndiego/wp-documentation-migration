---
title: List view
slug: list-view
original_url: https://wordpress.org/documentation/article/list-view/
wp_id: 14641368
categories:
- customization
- block-editor
date: '2021-07-08T23:00:09'
modified: '2026-09-09T20:28:08'
migration:
  status: warnings
  warnings:
  - contained VideoPress embed (now a bare oEmbed URL; verify it auto-embeds after import)
  videos:
  - type: videopress
    guid: 5Ns9rJJH
    url: https://videopress.com/v/5Ns9rJJH
    original: https://videos.files.wordpress.com/5Ns9rJJH/list-view-7-1.mov
    poster: https://videos.files.wordpress.com/5Ns9rJJH/list-view-7-1_mov_vp9_1440p.original.jpg
    media_id: 16370347
  counts:
    callouts: 1
    callouts_info: 1
    images: 9
    images_missing_alt: 1
    internal_links_rewritten: 5
    preserved_heading_anchors: 2
    videopress: 1
---

# List view

List view is a navigation tool that displays all the blocks in your post or page in a structured outline. It makes it easy to move between nested blocks, select specific content, and understand how your content is organized. Whether you’re looking for a single Paragraph block buried deep within a long post or a Columns block containing multiple items, List view helps you quickly find and edit exactly what you need.

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/5Ns9rJJH -->

https://videopress.com/v/5Ns9rJJH

## How to use List view

![Document overview button location](../../assets/images/2021/07/Screenshot-2026-09-04-at-3.59.41-PM.png)

Click on the Document Overview button in the top left of the editor to open the List view panel.

This will cause the view to open and stay open until you close it once more. You can close List View by either selecting the “x” or by selecting the Document Overview icon once more.

List view will show image previews for [Image](../media-blocks/image-block.md) and [Gallery](../media-blocks/gallery-block.md) blocks. It will also display blocks the names of HTML anchors given to blocks.

![List view close button](../../assets/images/2021/07/Screenshot-2026-09-04-at-4.18.46-PM.png)

### How to select blocks

List view allows you to both see all of your content at once and select any block you’d like. To select a block and bring it into focus, click on the name of the block in List view. This will select the block for you to then customize in the editor. Press the escape key to deselect all blocks.

### How to select multiple blocks

You can select multiple blocks at once in List view by holding down the Shift key and clicking them

### How to drag and drop blocks

After opening List view, select the block or section of blocks you want to drag and drop. After selecting, you can then drag and drop the content wherever you’d like within the List view sidebar. You are not able to drag and drop within the Editor itself.

### How to make changes to individual blocks

Each block within List view has a three-dot menu that you can click on to take further action on the block itself. List view block controls include: Copy, Cut, Duplicate, Add before, Add after, Add note, Copy styles, Paste styles, Group, Ungroup, Lock, Unlock, Rename, Hide, Create Pattern, and Delete.

![Expand block options in list view](../../assets/images/2021/07/Screenshot-2026-09-04-at-4.26.07-PM.png)

### How to collapse sections

Next to each section of blocks, you’ll see an arrow icon that you can click to collapse or expand sections of blocks. This is helpful if you’re trying to navigate between complex content in order to more readily focus on different sections.

![The arrow icon next to each block to collapse or expand block](../../assets/images/2021/12/Screen-Shot-2021-12-21-at-3.45.27-PM.png)

### How to display an HTML anchor

If a block has an HTML Anchor set, it’s displayed in List view so it’s easier to distinguish between other blocks and reference as you want. Here’s an example with a `my-anchor-2` anchor.

![HTML anchor example](../../assets/images/2021/07/Screenshot-2026-09-04-at-4.30.32-PM.png)

> [!NOTE]
> [Learn more about HTML Anchors in the Page Jumps documentation.](page-jumps.md)

## Locked Blocks

If a block has been [locked](more-options.md#lock), a small icon will show next to its name in the List view.

![Locked blocks example](../../assets/images/2021/07/Screenshot-2026-09-04-at-4.36.02-PM.png)

## Hidden Blocks

If a block has been hidden, a small eye icon will show next to its name in the List view.

![](../../assets/images/2021/07/list-view-1-7.0.jpg)

*Screenshot*

<a id="demonstration-of-list-view"></a>

## Synced Patterns

[Synced patterns](reusable-blocks.md) are highlighted in purple to distinguish them from regular blocks. When you select a Synced pattern from the List view, you will see additional options in the editor.

![Example of a synced pattern in List view with the name My synched pattern. There is an Edit original button on the pattern and in the block settings sidebar.](../../assets/images/2021/07/Screenshot-2026-09-09-at-3.26.35-PM.png)

<a id="demonstration-of-list-view-2"></a>

## Outline

![Outline tab](../../assets/images/2021/07/Screenshot-2026-09-04-at-4.42.16-PM.png)

Choose the Outline tab to display the following post information:

-   Number of characters
-   Number of words
-   Time to read
-   Heading structure

## Resources

-   [Improve your workflow with List view](https://make.wordpress.org/core/2021/06/09/core-editor-improvement-improve-your-workflow-with-list-view/)

## Changelog

-   2026-09-04 (props @awetz583 @CalolanC @leonnugraha @iammehedi1 @donalirl @ekamran @simonwheatley @anujrathore24 @omarbadawy1)
    -   Updated video and screenshots to 7.1
-   2026-05-05
    -   Updated hidden blocks
-   2024-04-16
    -   Updated a screenshot and alt texts
-   2024-01-25
    -   Add media previews to list view for gallery and image blocks
-   2023-08-08
    -   WordPress 6.3 renamed Reusable Block to Patterns
-   2023-07-17
    -   WordPress 6.3 renamed Reusable Block to (Synced) Patterns
-   2023-06-14 Updated to reflect how the “info” section is now inside the list view.
-   2021-07-09 Created
