---
title: Accordion block
slug: accordion-block
original_url: https://wordpress.org/documentation/article/accordion-block/
wp_id: 16366403
categories:
- customization
- design-blocks
date: '2025-12-02T20:00:00'
modified: '2026-09-06T09:17:18'
migration:
  status: clean
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2025/11/6-9-accordion-i3.mp4
    local_path: docs/assets/videos/2025/11/6-9-accordion-i3.mp4
  counts:
    callouts: 8
    callouts_info: 8
    images: 10
    images_missing_alt: 1
    internal_links_rewritten: 10
    legacy_support_links_fixed: 1
    self_hosted_videos: 1
  first_paragraph_is_nav_link: true
---

# Accordion block

[Go to the list of Blocks](../block-editor/blocks-list.md)

The Accordion block lets you show content in collapsible sections so visitors can expand just the parts they need. It’s commonly used for FAQs, schedules, or any long page you want to make easier to scan. Each Accordion contains Accordion Item blocks. Every item has:

-   Accordion Heading: the clickable title.
-   Accordion Panel: the content that expands and collapses. You can add any blocks in the panel.

## Add an Accordion block

To add the Accordion block, click the **+ Block Inserter** button in the top-left corner of the editor. Search for the Accordion block and click on the block to add it to the page.

Alternatively, you can quickly add the Accordion block by typing `/accordion` and pressing **Enter**.

## Add, edit, and reorder Accordion Items

-   Add a new item: Click the **+ Add item** button inside the block (or use the inserter at the end of the list).
-   Edit a heading: Click the Accordion Heading and type a short, descriptive title.
-   Add content: Click inside the Accordion Panel and add any blocks you need (paragraphs, images, lists, etc.).
-   Reorder items: Use the move handles in the toolbar or drag items in List View to change the order.
-   Expand/collapse while editing: Click a heading to toggle the panel open or closed so you can focus on one item at a time.

## Block toolbar

![Accordion Block toolbar](../../assets/images/2025/12/accordion-block-toolbar.png)

### Transform to

![Transform Accordion block to group, columns or details block](../../assets/images/2025/12/Screenshot-2026-07-21-at-1.45.22-PM.png)

Click on the **Transform button** to convert the Accordion block into a Columns, Details, or Group block.

### Block moving tools

![Accordion block moving tools](../../assets/images/2025/12/accordion-block-toolbar-movi-ng.png)

The block-moving tools allow you to move the block in the editor. Use the **six dots icon** to drag and drop the block and place it anywhere on the page. Alternatively, click on the **up and down arrows** to move the block up or down.

> [!NOTE]
> [Get more information about moving a block within the editor.](../block-editor/moving-blocks.md)

### Align

![Block toolbar align button](../../assets/images/2025/12/accordion-block-toolbar-align.png)

Use the change alignment tool to align the Accordion block. Choose one of the following options:

-   **None –** keeps the block at the narrow content width.
-   **Wide width –** increase the width of the block beyond the content size.
-   **Full width –** extend the block to cover the full width of the screen.

The Wide width and Full width alignment settings must be enabled by your WordPress theme.

### Level

![Heading button](../../assets/images/2025/12/accordion-block-toolbar-level.png)

Choose the heading level that will be applied to the Accordion Heading blocks within the Accordion block.

### Add Item

![Add item button](../../assets/images/2025/12/accordion-block-toolbar-add-item.png)

Click the **Add Item button** to add a new Accordion Item inside the Accordion block.

### More options

The More options menu represented by three vertical dots on the far right of the toolbar gives you more features such as the ability to duplicate or remove the block.

> [!NOTE]
> [Read about these and other settings.](../block-editor/more-options.md)

## Block settings

Every block has specific options in the editor sidebar in addition to the options found in the block toolbar. If you do not see the sidebar, click on the **Settings button** next to the Save/Publish button.

![Block Settings button](../../assets/images/2020/11/block-settings-7-0.png)

The Accordion block settings panel is divided into three tabs – **List View**, **Settings**, and **Styles**.

### List View

![List view tab](../../assets/images/2025/12/Screenshot-2026-07-21-at-1.55.28-PM.png)

The **List view tab**, represented by three horizontal lines, allows you to re-order Accordion Items within the Accordion block.

> [!NOTE]
> [Learn more about options and settings available in list view.](../block-editor/list-view.md)

### Settings

![Accordion Settings tab](../../assets/images/2025/12/Screenshot-2026-07-21-at-2.00.17-PM.png)

When you select the Accordion block **Settings tab**, represented by a gear icon, you will see the following settings in the sidebar:

#### Settings

**Auto-close toggle** – When on, this will automatically close accordions when a new one is opened.

**Show icon toggle** – When on, an icon will display with an additional option to select it to display on the right or left side.

**Icon position button** – Position the icon to the left or right of the the accordion title.

#### Advanced

The Accordion block provides the following Advanced settings options: HTML anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings](../block-editor/advanced-settings-overview.md)

### Styles

![](../../assets/images/2025/12/Screenshot-2026-07-21-at-2.00.43-PM.png)

When you click on the **Styles tab**, represented by a half-filled circle, within the Block Settings sidebar, you will see the following options:

#### Typography

The Accordion block provides typography settings to change the font family, size, appearance, line height, letter case, letter spacing, and decoration.

> [!NOTE]
> [Get more details about changing typography settings.](../block-editor/typography-settings-overview.md)

#### Background

The Background settings allow you to customize the appearance of supported blocks using background images, colors, and gradients.

> [!NOTE]
> For details, refer to the [Background Settings Overview](../block-editor/background-settings-overview.md).

#### Layout

##### Inner blocks use content width

If you toggle this on, nested blocks will fill the width of the Accordion Block container. Depending on your theme, you may be able to set accordion blocks to wide or full width.

#### Dimensions

Dimension controls are used to control how groups of blocks are placed alongside one another, by changing the values for padding, margin, and other dimensions

> [!NOTE]
> [Learn more about dimension controls.](../block-editor/dimension-controls-overview.md)

#### Border & Shadow

The Accordion block provides border settings options to add border color, width, radius and shadow. If there are custom border settings, custom border will be visible on image placeholder.

> [!NOTE]
> [Learn more about border and shadow settings.](../block-editor/border-settings-overview.md)

## Accordion inner blocks

The Accordion block is made of a few blocks to pull the feature together:

-   Accordion item
-   Accordion panel

These inner blocks may include additional style controls depending on your theme (colors, typography, spacing). For the Accordion item, you can pick the semantic heading level for the item’s title (for example, H3, H4). Use levels that fit your page outline.

## Tips

-   Keep headings short and descriptive so visitors know what each item contains.
-   Use consistent heading levels across items (for example, all H3s) that fit your page’s heading structure.
-   For long content, consider splitting items into smaller sections or using lists inside the panel.
-   Save frequently used accordions (like an FAQ) as a Pattern so you can reuse them across your site.

## Accessibility

-   The Accordion block follows accessible patterns so headings act as buttons and panels announce their expanded/collapsed state to assistive technologies.
-   Best practices:
    -   Use meaningful, concise headings.
    -   Avoid placing interactive elements (like links or buttons) inside the heading itself; put them in the panel.
    -   Choose heading levels that follow your page hierarchy.

## Demo

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2025/11/6-9-accordion-i3.mp4"></video>

## Frequently asked questions

**What’s the difference between Accordion and Details?**

-   Details creates a single collapsible section. Accordion is a list of coordinated collapsible items with options to allow one or multiple open at once.

**Can I open more than one item at the same time?**

-   Yes. Turn on “Allow multiple items to be open” in the Accordion block settings.

**How do I make a specific item open by default?**

-   Select the Accordion Item, then enable “Initially open” in its settings.

**Can I add any blocks inside an Accordion Panel?**

-   Yes. Panels can contain any blocks, including images, lists, and embeds.

## Changelog

-   Updated 2026-09-06 (props @atachibana)
    -   Rearrange the Styles sections for WordPress 7.1 and add explanatory text.
-   Updated 2026-07-21
    -   Updated screenshots to 7.0 and added List view
-   Updated 2026-05-25 (props @kjoyner @awetz583)
    -   Updated “Advanced” section to refer to new overview page
-   Created 2025-12-02
