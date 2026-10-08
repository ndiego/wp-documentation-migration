---
title: Tag Cloud block
slug: tag-cloud-block
position: 12
original_url: https://wordpress.org/documentation/article/tag-cloud-block/
wp_id: 13255925
legacy_categories:
- customization
- widget-blocks
date: '2020-08-17T13:05:58'
modified: '2026-07-23T21:32:40'
migration:
  status: warnings
  warnings:
  - 'external images hotlinked from lh4.googleusercontent.com: 1 (see assets/images-manifest.json)'
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  counts:
    callouts: 6
    callouts_info: 6
    images: 11
    internal_links_rewritten: 10
  nav_link_removed: true
---

# Tag Cloud block

The *Tag Cloud block* allows adding tag/category cloud into the page/post. A tag cloud is a list of all [tags](../../../../using-wordpress/administration-screens/posts/posts-tags-screen.md) /categories on your site, displayed in alphabetical order.

Tag cloud helps your readers to discover and search content easily and quickly.

The *Tag Cloud block* displays each tag with the font size based on the number of times that tag has been associated with posts. The bigger the size, the more posts are tagged with that tag. This helps your readers know your favorite subjects and the topics you write about most frequently.

## How to add a Tag Cloud block to your post or page

Add the *Tag Cloud block* to your post or page by clicking on the “Block Inserter” (+) and then search for “Tag Cloud”. Alternatively, you can type `/tag-cloud` in a new paragraph block and press `enter`.

![How to add a Tag Cloud block](../../../../assets/images/2024/04/image-1.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../../working-with-blocks/adding-a-new-block.md)

If you have tags/categories on your site, the *Tag Cloud block* will display a list of the tags as follows:

![Preview of a Tag Cloud block](../../../../assets/images/external/lh4.googleusercontent.com/6144cb2d2c-sHbYOYAREktz040z873suDbtBKRh7Qjd6ChV6_bKrtvWWVjUbr_jjdVuI56E.png)

If the site doesn’t have any tags then it will display the message as shown below.

![When there are no tags to show, the block displays a text that says "There's no content to show here yet."](../../../../assets/images/2020/08/tag-clould-no-content-WP-62.png)

**Note:** Tags’ appearance varies based on the selected theme.

## Block toolbar

Each block has its own block-specific controls that allow you to customize the block right in the editor. The *Tag Cloud block* offers the following options in its toolbar:

-   Transform to
-   Drag
-   Move handles
-   Change alignment
-   More Options.

### Transform to

![Transform options in the Tag Cloud block](../../../../assets/images/2022/07/Screen-Shot-2022-07-19-at-5.05.21-PM.png)

When you click on the **Transform** button you can convert the *Tag Cloud block* into a Categories List, Columns, or Group. The Group lets you change the background color around the Tag Cloud block. You can also change the Tag Cloud styles from Default to Outline.

![Editor view of an Tag Cloud block as a group with Color Settings controls](../../../../assets/images/2022/07/171654193-d567206e-27ef-436b-b26a-3f608faa48b6.png)

![Tag Cloud block with a yellow background.](../../../../assets/images/2022/07/171654025-c209b1b6-d786-44d4-a4d6-d648d24d0a41-1.png)

### Drag

To drag and drop the block to a new location on the page template, click and hold the rectangle of dots, then drag to the new location. The blue separator line indicates where the block will be placed. Release the left mouse button when you find the new location to place the block.

### Move handles

The up and down arrow icons can be used to move a block up and down on the page.

> [!NOTE]
> [Get more information about moving a block within the editor.](../../working-with-blocks/moving-blocks.md)

### Change alignment

![Change alignment in the Tag Cloud block](../../../../assets/images/2022/07/Screen-Shot-2022-07-19-at-5.08.19-PM.png)

-   **Wide width** – Increase the width of the Tag Cloud block beyond the content size.
-   **Full width** – Extend the Tag Cloud block to cover the full width of the screen.
-   **Align left** – Make the Tag Cloud left aligned
-   **Align center** – Make the Tag Cloud aligned center.
-   **Align right** – Make the Tag Cloud right aligned.

**Note:** “Wide width” and “Full width” alignment is only available if it is enabled by the Theme of your site.

### More options

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../../working-with-blocks/more-options.md)

## Block settings

Every block has specific options in the editor sidebar in addition to the options found in the block toolbar. If you do not see the sidebar, simply click the ‘settings’ icon next to the Publish button.

### Settings tab

#### Taxonomy

Select from the following three [taxonomy](../../../../using-wordpress/writing-and-publishing/organizing-your-site/taxonomies.md) types: Categories, Tags, or Pattern Categories. The Tag Cloud is displayed based on the selected taxonomy.

#### Show post counts

Toggle the switch to display the number of posts associated with the taxonomy.

#### Number of tags

Move the slider or type in a number to change the number of taxonomy terms that can be displayed in the Tag Cloud.

![Number of tags in the Tag Cloud block](../../../../assets/images/2020/08/image-3.png)

#### Smallest size/largest size

Change the smallest and largest font size that can be used in the Tag Cloud. You can change the font size unit between PX, %, EM, REM, VW, VH.

![Font size in the Tag Cloud block](../../../../assets/images/2022/07/Screen-Shot-2022-07-19-at-5.35.39-PM.png)

![The block settings sidebar with the settings tab opened.](../../../../assets/images/2023/04/tag-cloud-settings-tab-WP-62.png)

### Styles tab

#### Styles

You can modify the *Tag Cloud block* styles by choosing the ‘Default’ or ‘Outline’ buttons in the Styles settings panel. Hover over the ‘Default’ or ‘Outline’ buttons to get a preview of the styles.

The style options may vary based on your theme.

#### Typography

Typography settings allow you to change a block’s font size, appearance, line height, letter casing, and spacing.

> [!NOTE]
> [Get more details about changing typography settings.](../../working-with-blocks/block-settings/typography-settings-overview.md)

#### Dimensions

Dimension controls are used to control how groups of blocks are placed alongside one another, by changing the values for padding, margin, and other dimensions

> [!NOTE]
> [Learn more about dimension controls.](../../working-with-blocks/block-settings/dimension-controls-overview.md)

![The block settings sidebar with the styles tab opened.](../../../../assets/images/2023/04/tag-cloud-styles-tab-WP-62.png)

### Advanced

The Tag Cloud block provides the following Advanced settings options: HTML anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings](../../working-with-blocks/block-settings/advanced-settings-overview.md)

## Changelog

-   Updated 2026-05-25 (props @kjoyner @awetz583)
    -   Updated “Advanced” section to refer to new overview page
-   Updated 2024-04-23
    -   Updated formatting
-   Updated 2023-03-30
    -   Updated screenshots.
    -   Added information about typography options.
-   Updated 2023-01-26
    -   Updated for formatting consistency.
-   Updated 2022-11-26
    -   Alinged images for mobile view .
    -   Removed redundant content .
-   Updated 2022-11-17
    -   Updated screenshots and content for 6.1.
-   Updated 2022-07-19
    -   Added content and screenshots for 6.0.
    -   Added ALT tags for images.
-   Created 2020-08-17
