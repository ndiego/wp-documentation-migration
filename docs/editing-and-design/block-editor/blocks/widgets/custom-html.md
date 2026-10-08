---
title: Custom HTML
slug: custom-html
position: 4
original_url: https://wordpress.org/documentation/article/custom-html/
wp_id: 11285129
legacy_categories:
- customization
- widget-blocks
date: '2019-03-07T10:19:35'
modified: '2026-06-15T23:56:28'
migration:
  status: clean
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2019/03/html-block-7-0.mp4
    local_path: docs/assets/videos/2019/03/html-block-7-0.mp4
  counts:
    callouts: 4
    callouts_info: 4
    edge_br_removed: 1
    images: 5
    internal_links_rewritten: 6
    preserved_heading_anchors: 1
    self_hosted_videos: 1
  nav_link_removed: true
---

# Custom HTML

**Hypertext Markup Language (HTML)**, is language used to describe the semantic content of web pages. This can be added using the custom HTML block. This block allows you to insert your code so you can fine-tune your content.

Starting in WordPress 7.0, the Custom HTML block introduces separate editing panels for HTML, CSS, and JavaScript. The CSS and JavaScript panels are only available to users with the unfiltered_html capability. If a user lacks this capability (for example, a Contributor), WordPress will sanitize the block’s content using the function [wp_kses()](https://developer.wordpress.org/reference/functions/wp_kses/), stripping disallowed tags such as `<script>` and `<iframe>`. In this case, the CSS and JavaScript panels are not shown, and any disallowed markup is removed when the post is saved or updated.

> [!NOTE]
> [Learn more about WordPress user roles and capabilities](../../../../using-wordpress/users-roles-and-profiles/roles-and-capabilities.md)

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2019/03/html-block-7-0.mp4" poster="../../../../assets/images/2019/03/Screenshot-2026-05-20-at-10.54.05-AM.jpg"></video>

## Add a Custom HTML block

In order to add a custom HTML block, click on the **Block Inserter** icon.

You can also type `/html` and hit enter in a new paragraph block to add one quickly.

![Adding a block with a slash html command](../../../../assets/images/2019/03/Screenshot-2026-05-20-at-10.56.23-AM.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../../working-with-blocks/adding-a-new-block.md)

## Editing the block

Once you add the block, click on the Edit HTML button to open the editing modal.

![Custom HTML block empty state showing an Edit HTML button](../../../../assets/images/2019/03/html-editing-block.png)

Enter HTML code and see the preview of your output to the right of the code editor. You can expand the modal to fullscreen the Enable/disable fullscreen button on the top right of the modal. When you are done entering code, press the Update button.

![Custom HTML block edit state showing the HTML code pane on the left and HTML output preview on the right](../../../../assets/images/2019/03/html-edit-modal.png)

## Block toolbar

The Custom HTML block has the following options on the block toolbar:

![Custom HTML block toolbar](../../../../assets/images/2019/03/html-block-toolbar.png)

### Block moving tools

The block-moving tools allow you to move the block in the editor. Use the six dots icon to drag and drop the block and place it anywhere on the page. Alternatively, click on the up and down arrows to move the block up or down.

![Custom HTML block toolbar with block moving tools highlighted](../../../../assets/images/2019/03/html-move-tools.png)

> [!NOTE]
> [Get more information about moving a block within the editor](../../working-with-blocks/moving-blocks.md)

### Edit Code button

Press this button to make changes to your Custom HTML block code.

### More options

These controls give you the option to copy, duplicate, or rename your block.

> [!NOTE]
> [Read about these and other settings](../../working-with-blocks/more-options.md)

<a id="block-settings-panel"></a>

## Block settings

While most blocks have specific options in the editor sidebar in addition to the options found in the block toolbar, the HTML block does not have extra options.

## Changelog

-   Updated 2026-05-20 (props to @awetz583 @atachibana @lanamiro1)
    -   Updated information, video and screenshots for 7.0
-   Updated 2026-05-01
    -   Updated formatting and added link to roles and capabilities
-   Updated 2025-07-21
    -   Added detail HTML processing
-   Updated 2022-11-26
    -   Removed redudant content
    -   Aligned images for mobile view
    -   Added heading
-   Updated 2022-04-20
    -   Update screenshots to 5.9
    -   Add More Options section
