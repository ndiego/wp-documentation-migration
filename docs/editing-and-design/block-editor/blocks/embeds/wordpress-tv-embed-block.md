---
title: WordPress.tv embed
slug: wordpress-tv-embed-block
position: 33
original_url: https://wordpress.org/documentation/article/wordpress-tv-embed-block/
wp_id: 13163708
legacy_categories:
- customization
- embed-blocks
date: '2020-07-24T09:14:57'
modified: '2026-06-29T20:07:20'
migration:
  status: warnings
  warnings:
  - contained VideoPress embed (now a bare oEmbed URL; verify it auto-embeds after import); guid qhbfoKqs not found in media library
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: videopress
    guid: qhbfoKqs
    url: https://videopress.com/v/qhbfoKqs
  counts:
    callouts: 4
    callouts_info: 4
    images: 16
    internal_links_rewritten: 5
    videopress: 1
  nav_link_removed: true
---

# WordPress.tv embed

Using WordPress.tv embed block, you can add a WordPress.tv video to a post or page. The embedded video includes a robust set of playback controls, so viewers can remain on your site while they watch the video. You don’t need WordPress.tv account to embed a video, although it needs to be public.

Embedded WordPress.tv video

<!-- VideoPress embed (iframe removed): https://video.wordpress.com/embed/qhbfoKqs -->

https://videopress.com/v/qhbfoKqs

**Steps to Embed a video from WordPress.tv:**

1.  Find the video permalink

In the web player select the video and click on the “Share” button.

![A sample video in the WordPress.tv page](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-1.png)

2.  In the share section, click on the permalink and it will be automatically copied, or alternatively, you can highlight the link and copy it.

![Finding the share link in the WordPress.tv post](../../../../assets/images/2022/07/WordPress.tv-Doc-SS-2.png)

If you add a link in some other way and the link can’t be embedded, you have the option of trying again or converting the URL to a link.

3.  Add a WordPress.tv embed block to your page/post

![How to quickly add a WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Doc-SS-3.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../../working-with-blocks/adding-a-new-block.md)

4.  Paste the link into the text box and click on the “Embed” button

![Paste the URL into the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Doc-SS-4.png)

If it’s a link that can be successfully embedded you will see a preview in your editor.

![Preview on the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-5.png)

If you use an URL that can’t be embedded, the block shows the message *“Sorry, this content could not be embedded.”*

![Error displayed when the content could not be embedded in the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-6.png)

You will have two choices: Try again with a different URL or convert it to a link.

5.  Click on “Preview” to see how it will look on the front-end

![Preview in the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-7-1.png)

## Block Toolbar

Besides the *Mover* and *Drag & Drop* handle, the Block Toolbar for the WordPress.tv embed shows four buttons:

-   Transform To
-   Block moving tools
-   Change Alignment
-   Edit URL
-   More Options

![Block toolbar in the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-8.png)

**Transform To**:

![Transform tool in the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-9.png)

You can transform WordPress.tv embed block to a Group. This would give you the ability to change the background color around WordPress.tv embed.

![Editor view of a WordPress.tv embed as a group with Color Settings controls](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-10.png)

*Editor view of a WordPress.tv embed as a group with Color Settings controls*

![WordPress.tv embeds with a blue background-color](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-11.png)

*WordPress.tv embeds with a blue background-color*

**Block-moving tools**

![Block moving tools in the WordPress.tv block](../../../../assets/images/2022/08/Screen-Shot-2022-08-01-at-11.19.31-AM.png)

Use the block-moving tools to move the block up and down the editor. Use the six dots icon to drag and drop the WordPress.tv embed block and reposition it anywhere on the editor. Alternatively, click on the up and down arrows to move the block up or down the editor.

> [!NOTE]
> Get the details on [moving a block within the editor.](../../working-with-blocks/moving-blocks.md)

**Change Alignment**

![Change alignment in the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-12.png)

-   **Align left** – Make the block left-aligned.
-   **Align center** – Make the block alignment centered.
-   **Align right** – Make the block right-aligned.
-   **Wide width** – Increase the width of the block beyond the content size.
-   **Full width** – Extend the block to cover the full width of the screen.

The “Wide width” and “Full width” alignment settings must be enabled by your WordPress theme.

**Edit URL**

Via the edit URL, you can change the WordPress.tv Embed URL in the embed block. Overwrite the existing URL and click on the “Embed” button.

![Edit URL in the WordPress.tv block](../../../../assets/images/2022/07/WordPress.tv-Embed-Doc-SS-13.png)

**More Options**

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../../working-with-blocks/more-options.md)

## Block Settings

**Media Settings**

Besides the Advanced section, the WordPress.tv embed has only one setting in the “Block Settings” sidebar: Media Settings.

**Media Settings**

![Media settings for the embed block with the toggle OFF for resizing on smaller devices.](../../../../assets/images/2020/04/Screen-Shot-2020-04-20-at-9.29.46-AM.png)

![Media settings for the embed block with the toggle ON for resizing on smaller devices.](../../../../assets/images/2020/06/media-settings-2-1.png)

Via the *Media Settings* you can control the behavior of your post embed when viewed from a smaller device, like on a phone screen.

The Toggle switch turns on or off the resize functionality for smaller devices. The default setting is “on” or blue.

**“Off:”** This embed may not preserve its aspect ratio when the browser is resized. In the off position, the toggle switch is gray.

**“On:”** This embed will preserve its aspect ratio when the browser is resized. The toggle switch turns blue in the “On” position.

**Advanced**

The following Advanced settings options are available: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings.](../../working-with-blocks/block-settings/advanced-settings-overview.md)

## Changelog

-   Updated 2026-06-29
    -   Linked to advanced settings
-   Updated 2022-08-01
    -   Screenshots and content for 6.0
    -   Added Media settings, Lock etc.
    -   Converted reusable blocks to regular blocks.
    -   Added ALT tags for the images
-   Updated 2022-07-25
    -   Screenshots as per WordPress 5.9
-   Updated 2020-09-02
    -   Screenshots as per WordPress 5.5
    -   Embedded WordPress.tv video
-   Updated 2020-08-19
    -   Replaced “More Options” – new screenshot
    -   Added “Move To” and “Copy” section under More Options
-   Created 2020-07-24
