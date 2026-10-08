---
title: Footnotes block
slug: footnotes-block
position: 4
original_url: https://wordpress.org/documentation/article/footnotes-block/
wp_id: 16358457
legacy_categories:
- customization
- text-blocks
date: '2023-08-08T07:28:08'
modified: '2026-06-30T03:17:00'
migration:
  status: clean
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2023/08/footnotes-demo.mp4
    local_path: docs/assets/videos/2023/08/footnotes-demo.mp4
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2023/08/footnotes-public-view.mp4
    local_path: docs/assets/videos/2023/08/footnotes-public-view.mp4
  counts:
    images: 7
    internal_links_rewritten: 5
    self_hosted_videos: 2
---

# Footnotes block

WordPress 6.3 introduces a new feature to insert and display footnotes. This option can be found on the toolbar of individual blocks under the [Rich Editing](../../working-with-blocks/more-text-editing-overview.md) option.

![Overview of how to insert Footnotes.](../../../../assets/images/2023/08/footnote-block.png)

## Adding the Footnotes Block

The Footnotes block will be added to your page or post as soon as you insert your first note using the Rich Text option. This new block works like other blocks and it can be moved around and removed.

From 6.4, the Footnotes block can be removed, a provision has been made to make re-insertion easier. Additionally, the footnotes block is now displayed in the inserter for improved discoverability. It will show even if anchors are not yet inserted into the content. This modification strеamlinеs and improvеs thе discovеrability of thе Footnotеs block, with thе wider goal of crеating a morе usеr-friеndly еxpеriеncе.

![The footnotes block can be added manually.](../../../../assets/images/2023/08/footnotes-inserter.png)

The text in the placeholder is a starting point, future refinements may include instructions on how to insert anchors.

![An empty footnotes block](../../../../assets/images/2023/08/footnotes-block-empty.png)

The user experience was enhanced in the most recent update by giving placeholder instructions for scenarios where the Footnotes block is not available for custom post types. This enhancement seeks to provide users with clearer guidance by providing instructions when the Footnotes block is missing in specified instances.

![Footnotes block placeholder when it's not available on custom post types](../../../../assets/images/2023/12/image.png)

Adding Footnote blocks to templates is also not possible at the moment but it is [being explored](https://github.com/WordPress/gutenberg/issues/52554).

Attempting to remove a Footnotes block triggers a warning regarding its removal and its impact. It advises that footnote references in the content area will continue to show if the block is removed. The user is required to confirm the deletion request before the block is deleted.

![The prompt when attempting to remove a footnotes block](../../../../assets/images/2023/12/image-3.png)

## Adding individual notes

To add new notes, highlight some text and open the “Rich Text” menu. Then select the “Footnotes” option.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2023/08/footnotes-demo.mp4"></video>

Notes are automatically linked to the original text and include a “go back” link for convenience.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2023/08/footnotes-public-view.mp4"></video>

If you move your blocks around after having added notes, the numbers and order of the notes will be automatically updated to match the changes you made.

## Removing and Deleting Footnotes

The Footnotes block in WordPress is designed to be user-friendly, but there are some nuances when it comes to removing footnotes or deleting them entirely. Here’s how you can manage footnotes effectively:

### 1. Removing the Footnotes Block

**Steps to Remove the Footnotes Block:**

1.  Select the Footnotes block at the bottom of your post or page.
2.  Click the three-dot menu (⋮) in the block toolbar.
3.  Choose Remove Block.
4.  A warning message will appear, informing you that removing the block will leave the footnote references intact. Confirm the deletion if you wish to proceed.

Note: If you reinsert the Footnotes block after removing it, all previously added footnotes will reappear.

### 2. Deleting Individual Footnotes

Currently, there is no direct way to delete individual footnotes from the Footnotes block. However, you can achieve this by removing the footnote references from the content area. Here’s how:

**Steps to Delete a Footnote:**

1.  Locate the footnote reference in your content (the superscript number linked to the footnote).
2.  Delete the reference by highlighting it and pressing the Backspace or Delete key.
3.  Once the reference is removed, the corresponding footnote in the Footnotes block will automatically disappear.

### 3. Clearing All Footnotes

If you want to remove all footnotes from your post or page, you’ll need to:

1.  Delete all footnote references in the content area (as described above).
2.  Remove the Footnotes block to ensure no residual footnotes remain.

## Customize the Footnotes Block

The Footnotes block has been improved with more design flexibility in this release. The block now has settings for [typography](../../working-with-blocks/block-settings/typography-settings-overview.md), [dimensions](../../working-with-blocks/block-settings/dimension-controls-overview.md), and [border](../../working-with-blocks/block-settings/border-settings-overview.md) control. [Color](../../working-with-blocks/block-settings/colors-settings-overview.md) support has been adjusted, with link and text now being the default, rather than background and text. These modifications attempt to give users more flexibility when it comes to modifying the Footnotes block.

![Footnote block settings options](../../../../assets/images/2023/12/image-1.png)

![Footnote block text color settings](../../../../assets/images/2023/12/image-2.png)

## Changelog

-   Updated 2026-06-30
    -   Added section on removing and deleting footnotes. Props @karthickmurugan
-   Updated 2023-12-12
    -   Updating content for WordPress 6.4
-   Created 2023-08-08
