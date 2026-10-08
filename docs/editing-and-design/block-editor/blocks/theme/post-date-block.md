---
title: Post Date block
slug: post-date-block
position: 29
original_url: https://wordpress.org/documentation/article/post-date-block/
wp_id: 15480868
legacy_categories:
- customization
- theme-blocks
date: '2022-03-21T22:08:10'
modified: '2026-07-27T17:38:05'
migration:
  status: warnings
  warnings:
  - contained VideoPress embed (now a bare oEmbed URL; verify it auto-embeds after import)
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: videopress
    guid: lGL1k8QW
    url: https://videopress.com/v/lGL1k8QW
    original: https://videos.files.wordpress.com/lGL1k8QW/post-date-post-kapture-2026-07-03-at-08.37.57.mp4
    poster: https://videos.files.wordpress.com/lGL1k8QW/post-date-post-kapture-2026-07-03-at-08.37.57_mp4_hd_1080p.original.jpg
    media_id: 16369313
  - type: videopress
    guid: WvGLmeK3
    url: https://videopress.com/v/WvGLmeK3
    original: https://videos.files.wordpress.com/WvGLmeK3/post-date-template-kapture-2026-07-03-at-08.29.15.mp4
    poster: https://videos.files.wordpress.com/WvGLmeK3/post-date-template-kapture-2026-07-03-at-08.29.15_mp4_hd_1080p.original.jpg
    media_id: 16369337
  counts:
    callouts: 8
    callouts_info: 8
    images: 11
    images_missing_alt: 1
    internal_links_rewritten: 18
    videopress: 2
  nav_link_removed: true
---

# Post Date block

Use the Post Date block to display the publication date of a post or page. You can add this block directly to a page template in the [Site Editor](../../../site-editor/README.md), such as the Single Post or Page template, to ensure a consistent layout across your site. You can also add it inside a [Query Loop block](query-loop-block.md) to customize the appearance and layout of your post feeds.

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/lGL1k8QW -->

https://videopress.com/v/lGL1k8QW

*Adding a Post Date block to a single post*

## Add a Post Date block

To add the Post Date block, click the **+ Block Inserter** button in the top-left corner of the editor. Search for the Post Date block and click on the block to add it to the page.

You can also quickly add the Post Date block by typing `/post date` and pressing **Enter**.

![Insert a Post date block with /post date command](../../../../assets/images/2022/03/post-date-insert-Screenshot-2026-07-03-at-8.53.10-AM.png)

> [!NOTE]
> [Detailed instructions on adding blocks.](../../working-with-blocks/adding-a-new-block.md)

### Add to a template

The Post Date block can be added to a template in the [Site Editor](../../../site-editor/README.md) to easily reflect the published date of a page or post across your website.

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/WvGLmeK3 -->

https://videopress.com/v/WvGLmeK3

## Block toolbar

![Post Date block toolbar](../../../../assets/images/2022/03/post-date-block-toolbar-Screenshot-2026-07-03-at-8.45.22-AM.png)

To view the block toolbar, click on the block and the toolbar will be displayed.

### Transform

![Post Date Block transform options](../../../../assets/images/2022/03/post-date-block-transforms-Screenshot-2026-07-03-at-8.49.01-AM.png)

Click on the **Transform** button to convert the Post Date block into a Modified Date, Group, Columns or Details block.

You will also see a “This block is connected” message indicating that the block has a binding to the Post’s published date.

### Block moving tools

![Post Date block moving tooks](../../../../assets/images/2022/03/post-date-move-tools-block-toolbar.png)

The block-moving tools allow you to move the block in the editor. Use the **six dots icon** to drag and drop the block and place it anywhere on the page. Alternatively, click on the **up and down arrows** to move the block up or down.

> [!NOTE]
> [Get more information about moving a block within the editor.](../../working-with-blocks/moving-blocks.md)

### Change text alignment

![Post Date block toolbar change text alignment](../../../../assets/images/2022/03/post-date-move-tools-block-toolbar-text-align.png)

Click the **Change alignment** button in the Block toolbar to display the alignment drop-down. You can align the block text to the left, make it center-aligned or align it to the right.

### Change date

![Post Date block toolbar Change Date button and modal](../../../../assets/images/2022/03/post-date-edit-date.png)

Click the **Change date** button in the Block toolbar to display a modal with date settings.

You can select the publishing date and time through the input fields and options or select the date from the calendar. You can use the arrow buttons or drop down box to select a different month.

Click anywhere outside the modal, press the <kbd>Escape</kbd> key, or click on the button with the X to close the modal.

### More options

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../../working-with-blocks/more-options.md)

## Block settings

![Block settings button](../../../../assets/images/2022/03/block-settings-button-7-0.png)

Every block has specific options in the editor sidebar in addition to the options found in the block toolbar. If you do not see the sidebar, click on the **Settings** button next to the Save/Publish button.

### Transform to variation button

![](../../../../assets/images/2022/03/Screenshot-2026-07-05-at-9.29.49-AM.png)

The Post Date block can be easily transformed into a [Modified Date](post-modified-date-block.md) block either by choosing the Transform button on the block toolbar or the Transform to variation button from the block settings.

The Post Date block settings panel is divided into two tabs – **Settings**, and **Styles**.

### Settings

![Post Date Block Settings tab](../../../../assets/images/2022/03/block-settings-tab.png)

#### Default format

This option is toggled on when you first add a Post Date block. Your site’s Default format can be changed in the site settings area, see [customize default date and time format](../../../../using-wordpress/writing-and-publishing/organizing-your-site/customize-date-and-time-format.md) to learn how.

To change the Post Date block to use a different format from your site’s default format, toggle off the **Default format** settings.

You can choose a format from a list of predefined selections under **Choose a format**.

![Settings custom format dropdown options.](../../../../assets/images/2022/03/Screenshot-2026-07-05-at-9.09.22-AM.png)

Or you can choose **Custom** from the drop down and enter a new format string in the input box that appears.

![Settings custom format dropdown options with Custom selected](../../../../assets/images/2022/03/Screenshot-2026-07-05-at-9.11.05-AM.png)

#### Link to Post

Toggle on the **Link to post** option to link the post date to the URL of the post. In a Query Loop block, this enables the website visitor to go to the post by clicking on the Post Date.

#### Advanced

The following Advanced settings options are available: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings.](../../working-with-blocks/block-settings/advanced-settings-overview.md)

### Styles

#### Color

The Post Date block provides Color settings options to change the text and background colors.

> [!NOTE]
> [See this guide for more information about changing colors.](../../working-with-blocks/block-settings/colors-settings-overview.md)

#### Typography

The Post Date block provides typography settings to change the font family, size, appearance, line height, letter case, letter spacing, and decoration.

> [!NOTE]
> [Get more details about changing typography settings.](../../working-with-blocks/block-settings/typography-settings-overview.md)

#### Dimensions

The Post Date block provides dimension settings options to change padding and margin size.

> [!NOTE]
> [Learn more about dimension controls.](../../working-with-blocks/block-settings/dimension-controls-overview.md)

#### Border

The Post Date block provides border settings options to add border color, width, and radius.

> [!NOTE]
> [Learn more about border settings.](../../working-with-blocks/block-settings/border-settings-overview.md)

## Changelog

-   Updated 2026-07-05 (props to @awetz583 @clk87 @poena @benazeer @atachibana)
    -   Updated text, screenshots and videos for 7.0
-   Updated 2026-06-29
    -   Linked to advanced settings
-   Updated on 2023-07-28
    -   Update the block toolbar screenshots and added relevant content for change date and updated screenshot for More option.
    -   Update the Block settings sidebar screenshots and relevant content for preview icon.
    -   Included the “Post date block variation for post modified date” content as a note under “Last modified date” in the Block settings sidebar.
-   Updated on 2023-07-23
    -   Corrected the headings for Block toolbar
-   Updated on 2023-07-16
    -   Added the Post Date block variation for Post Modified Date, as mentioned here [49111](https://github.com/WordPress/gutenberg/pull/49111)
    -   Added the video for only display the modified post date if the post has been modified, as mentioned here [46839](https://github.com/WordPress/gutenberg/pull/46839)
-   Updated on 2023-07-11
    -   Updated the video to show how to add post date block because it was shows “Post Categories” which now has been changed into “Categories block”
    -   Added option to display as the last modified date as suggested here [42312](https://github.com/WordPress/gutenberg/pull/42312) and also added the text under block settings
    -   Added information for typography support, as mentioned here [43340](https://github.com/WordPress/gutenberg/pull/43340)
    -   Added option for spacing support, as mentioned here [43406](https://github.com/WordPress/gutenberg/pull/43406)
    -   Made sure all the images have alt tag
    -   Made sure the headings are in sentence case
    -   Made sure the screenshots are updated and videos are relevant to the latest version 6.2.2
-   Created 2022-03-21
