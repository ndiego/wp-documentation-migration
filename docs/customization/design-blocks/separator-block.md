---
title: Separator block
slug: separator-block
original_url: https://wordpress.org/documentation/article/separator-block/
wp_id: 11285864
categories:
- customization
- design-blocks
date: '2019-03-07T12:32:15'
modified: '2026-07-23T21:26:04'
migration:
  status: clean
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2023/06/separator-block-demo.mp4
    local_path: docs/assets/videos/2023/06/separator-block-demo.mp4
  counts:
    callouts: 7
    callouts_info: 7
    image_self_links_removed: 2
    images: 9
    internal_links_rewritten: 7
    self_hosted_videos: 1
  first_paragraph_is_nav_link: true
---

# Separator block

[Go back to the list of **Blocks**](../block-editor/blocks-list.md)

The *separator block* creates a break between two blocks of content with a horizontal line. This helps to create a separation between ideas or sections on your post or page.

In order to add a Separator block, click on the **Block Inserter** icon.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2023/06/separator-block-demo.mp4"></video>

*A video showing the process of adding a separator block using the block inserter and changing styles and settings.*

You can also type<kbd>/separator</kbd> and hit enter in a new Paragraph block to add one quickly.

![How to quickly add a separator block](../../assets/images/2022/08/171654172-0eb91e47-4276-4e0e-86cc-c7a9c572b4f1.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../block-editor/adding-a-new-block.md)

## Block toolbar

Each block has its own block-specific controls that allow you to manipulate the block right in the editor. The Separator block has the following options in the Block toolbar.

![Block toolbar in the Separator block](../../assets/images/2022/08/171654325-3831afa2-c782-428f-884c-1ae7fab164ca.png)

### Transform to

When you click on the “Transform” button, you can convert the Separator block into Spacer, Columns, Details, or Group blocks.

![Transform option in the Separator block](../../assets/images/2019/03/separator-transform.png)

-   **Group**: Wraps the Separator inside a Group block, allowing background color, spacing, and border customization.
-   **Spacer**: Transforms the visual line into empty vertical space, useful for adding space between blocks without a visible divider.
-   **Columns**: Wraps the content into a multi-column layout, ideal for displaying blocks side-by-side.
-   **Details**: Converts the Separator into a collapsible block for toggling additional content, providing interactive and space-saving content organization.

### Block-moving tools

![Block moving tools in the Separator block](../../assets/images/2022/08/Screen-Shot-2022-08-03-at-1.29.37-PM-1.png)

Use the block-moving tools to move the block up and down inside the editor. Use the six dots icon to drag and drop the *Separator Block* and reposition it anywhere on the editor. Alternatively, click on the up and down arrows to move the block up or down the editor.

> [!NOTE]
> [Get more information about moving a block within the editor.](../block-editor/moving-blocks.md)

### Change alignment

The change alignment tool lets you align the *Separator block* within the content. You can choose one of the following alignment options:

![Change alignment in the Separator block](../../assets/images/2019/03/separator-alignment.png)

**None**: Leaves the block alignment as is.

**Wide width**: Increase the width of the block beyond the content size.

**Full width**: Extend the block to cover the full width of the screen (if supported by your site’s theme).

**Align center**: Align the block to the center of the content.

### More options

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../block-editor/more-options.md)

## Block settings

Every block has specific options in the editor sidebar in addition to the options found in the block toolbar. *If you do not see the sidebar, simply click the ‘sidebar’ icon.*

![A screenshot of the sidebar icon used to toggle the settings pane.](../../assets/images/2023/05/Screenshot-2023-05-23-at-8.41.56-AM.png)

*Use the sidebar icon to toggle the settings pane on or off.*

### Styles

You can modify the Separator block’s look by choosing one of the styles available in the block’s settings on right-hand side under **Styles**. You can either hover or focus click on each of the style buttons (e.g. ‘Default’, ‘Wide Line’ or ‘Dots’) to get a preview of the styles.

> [!NOTE]
> The style options may vary based on your theme!

![Style settings in the Separator block](../../assets/images/2022/08/171654332-5ee10afb-ce3d-4bb3-9ae9-ba8a3a14f67e.png)

### Color

![Images showing the color settings available](../../assets/images/2022/11/seperator-1.png)

*Color settings allow you to change the color of the separator*

The color settings let you customize the color for the Separator block. Pick a color from the suggestions, or add a custom color using the color picker or by adding a color code.

> [!NOTE]
> [See this guide for more information about changing colors.](../block-editor/colors-settings-overview.md)

### Dimensions

The separator block provides the ability to add margin values via the Dimensions settings option, giving you more control over content separation.

![Screenshot of the Dimensions settings on the Separator block sidebar](../../assets/images/2023/06/219549381-77382744-a69d-4a0e-bcec-98a8a5fba95e.png)

*The ‘margin’ dimension setting allows you to add space above or below your separator.*

> [!NOTE]
> [See this guide for more information about dimensions settings.](../block-editor/dimension-controls-overview.md)

### Advanced

The Separator block provides the following Advanced settings options: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles. You may see the Additional CSS Class(es) field populated with a CSS class already if the Separator block has [Styles](#styles) applied.

> [!NOTE]
> [Learn more about advanced settings](../block-editor/advanced-settings-overview.md)

## Changelog

-   Updated 2026-05-25 (props @kjoyner @awetz583)
    -   Updated “Advanced” section to refer to new overview page
-   2025-04-17 (props to [@karthickmurugan](https://profiles.wordpress.org/karthickmurugan/))
    -   Update screenshots to 6.8.
    -   Update **Transform to** section with new options.
-   Updated 2023-06-28
    -   Updated video & screenshots for 6.2
    -   Added dimensions settings section
    -   Tweaked wording for Styles section to include preview on hover/focus click
-   Updated 2022-11-22
    -   Removed redundant content
    -   Aligned images for mobile view
-   Updated 2022-08-03
    -   Screenshot, content, and video updated for 6.0
    -   Added ALT tags for the images
-   Updated 2020-08-23
    -   Updated images to WP 5.5
-   Updated 2020-08-10
    -   Added link to the list of blocks
    -   Added changlog box
-   Created 2019-03-07
