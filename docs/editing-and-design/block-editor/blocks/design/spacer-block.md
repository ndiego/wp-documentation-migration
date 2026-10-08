---
title: Spacer block
slug: spacer-block
position: 10
original_url: https://wordpress.org/documentation/article/spacer-block/
wp_id: 11285893
legacy_categories:
- customization
- design-blocks
date: '2019-03-07T12:43:29'
modified: '2026-07-23T21:27:09'
migration:
  status: warnings
  warnings:
  - 'external images hotlinked from user-images.githubusercontent.com: 1 (see assets/images-manifest.json)'
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2019/03/spacer-1.mp4
    local_path: docs/assets/videos/2019/03/spacer-1.mp4
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2019/03/spacer-2.mp4
    local_path: docs/assets/videos/2019/03/spacer-2.mp4
  counts:
    callouts: 4
    callouts_info: 4
    images: 9
    internal_links_rewritten: 7
    legacy_support_links_fixed: 1
    self_hosted_videos: 2
    small_images_kept_as_html: 3
  nav_link_removed: true
---

# Spacer block

If you want to have a space between two blocks, the Spacer block is what you will use.<br>
A **vertical** spacer adds space between blocks in a column (as in a page or post).<br>
A **horizontal** spacer adds space between blocks in a row (as in a [Navigation block](../theme/navigation-block.md)).

(Note: Using a Navigation block requires a [block theme](https://wordpress.org/themes/tags/full-site-editing/) or a theme that has support for [template editing](https://wordpress.org/themes/tags/template-editing/).)

In this video, you can see how you can use the spacer block and the different settings to modify it.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2019/03/spacer-1.mp4"></video>

*Demo of inserting Spacer block into post content and modifying its settings.*

## Add a Spacer block

To add an Spacer block, click on the **Add Block** icon.

You can also type `/spacer` and hit enter in a new *paragraph block* to add one quickly.

![How to add a space block to a page or post](../../../../assets/images/external/user-images.githubusercontent.com/4da5d58417-189541348-49772276-96e3-4eac-9fde-4b08df482b83.jpeg)

*Add Spacer Block*

## Block toolbar

In order to reveal the block toolbar, you can click on the block and the toolbar will display.

Every block comes with unique toolbar icons and blocks specific user controls that allow you to manipulate the block right in the editor.

The Spacer block shows four buttons in the block toolbar:

-   Transform to
-   Move controls
-   More options

<img src="../../../../assets/images/2019/03/spacer-block-toolbar-all.png" alt="The spacer block toolbar " width="230">

*Spacer Block Toolbar*

### Transform to:

![Transform options for Spacer Block](../../../../assets/images/2019/03/spacer-transforms.png)

*Transform options for Spacer Block*

When you click on the **“Transform”** button, you can convert the **Spacer** block into **Columns**, **Separator**, **Details**, or **Group** blocks.

-   **Separator**: Changes the Spacer into a visual horizontal line that helps divide content, providing a cleaner visual break between sections.
-   **Group**: Allows you to wrap the Spacer inside a Group, enabling background color, padding, margin, and border customization for better layout styling.
-   **Columns**: Useful if you want to place multiple blocks side-by-side; this transformation helps shift the layout into a multi-column structure.
-   **Details**: Converts the Spacer into a collapsible content block, allowing additional context or content to be toggled by the user.

### Move controls

<img src="../../../../assets/images/2019/03/spacer-block-toolbar-drag-1.png" alt="Drag icon in the Spacer block" width="230">

*Drag icon in the Spacer block*

To drag and drop the block to a new location on the page template, click and hold the six dotted icon, then drag to the new location. The blue separator line indicates where the block will be placed. Release the left mouse button when you find the new location to place the block.

<img src="../../../../assets/images/2019/03/spacer-block-toolbar-moving-1.png" alt="Move arrows in the Spacer block" width="230">

*Move arrows in the Spacer block*

The up and down arrow icons can be used to move a block up and down in your document.

> [!NOTE]
> [Get more information about moving a block within the editor.](../../working-with-blocks/moving-blocks.md)

### More options

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../../working-with-blocks/more-options.md)

## Block settings

![Block settings button location](../../../../assets/images/2019/03/block-settings-Screenshot-2026-03-08-at-8.13.56-AM-1-1-2.png)

Every block has specific options in the editor sidebar in addition to the options found in the block toolbar. If you do not see the sidebar, click on the **Settings button** next to the Save/Publish button.

### Spacer settings

The Height setting adjusts the height of the space. The Width setting adjusts the width of the space. You can adjust the settings by either:

-   Typing the number in the “Spacer Settings” box, or
-   Dragging the handle at the bottom of the spacer (for the vertical spacer) or at the side of the spacer (for the horizontal spacer).

You can also change the unit by clicking on PX to display a dropdown with the other supported units- PX, %, EM, REM, VW, and VH.

![Spacer block settings, showing the supported units](../../../../assets/images/2024/01/image-9.png)

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2019/03/spacer-2.mp4"></video>

*The interactive resizable box and the sidebar preset controls used to tweaks the Spacer block.*

When Spacer is a child of a flex layout block (Row, Stack, Navigation) custom size controls are removed and flex child controls added instead.

![Fixed size control for Spacer block when it's a child of a flex layout block.](../../../../assets/images/2019/03/spacer-flexbox-1.png)

*Fixed size flex control for Spacer block*

![Fill size control for Spacer block when it's a child of a flex layout block.](../../../../assets/images/2019/03/spacer-flexbox-2.png)

*Fill size flex control for Spacer block*

### Dimensions

The paragraph provides dimension settings options to add margin. For details refer to this support article:

> [!NOTE]
> [Learn more about dimension controls](../../working-with-blocks/block-settings/dimension-controls-overview.md)

### Advanced

The Separator block provides the following Advanced settings options: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings](../../working-with-blocks/block-settings/advanced-settings-overview.md)

## Changelog

-   Updated 2026-05-25 (props @kjoyner @awetz583)
    -   Updated “Advanced” section to refer to new overview page
-   2026-04-20 (props to @awetz583 @hu55nain)
    -   Remove reference to padding
    -   Text formatting updates
-   2025-04-17 (props to [@karthickmurugan](https://profiles.wordpress.org/karthickmurugan/))
    -   Update screenshots and videos to 6.8
    -   Update Transform to section with new options.
-   Updated 2024-01-30
    -   Updated screenshots for 6.4
-   Updated 2023-10-24
    -   Update screenshots for 6.3
    -   Add custom units for height and width
    -   The resizable box and controls
    -   Add dimnesions support for margin
    -   Add spacing presets
    -   Add flex child controls for Spacer
-   Updated 2022-11-25
    -   Removed redundant content
    -   Added alt text
    -   Aligned images for mobile view
-   Update 2022-03-21
    -   Updated all screenshots to WordPress 5.9
-   Update 2021-06-22
    -   Updated more options block
-   Updated 2020-09-28
    -   Updated 5.5 screenshots
    -   Updated the block toolbar
    -   Updated the block settings
-   Created 2019-03-07
