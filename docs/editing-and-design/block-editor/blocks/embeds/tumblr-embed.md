---
title: Tumblr embed
slug: tumblr-embed
position: 27
original_url: https://wordpress.org/documentation/article/tumblr-embed/
wp_id: 13708351
legacy_categories:
- customization
- embed-blocks
date: '2020-11-25T03:30:00'
modified: '2026-06-29T20:06:03'
migration:
  status: warnings
  warnings:
  - 'external images hotlinked from lh5.googleusercontent.com: 1 (see assets/images-manifest.json)'
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  - link to 'importing-content' points to moved page https://developer.wordpress.org/advanced-administration/wordpress/import/
  counts:
    callouts: 3
    callouts_info: 3
    edge_br_removed: 1
    images: 14
    internal_links_rewritten: 4
    links_to_moved_external: 1
    small_images_kept_as_html: 1
  nav_link_removed: true
---

# Tumblr embed

With the Tumblr Embed block, you can embed several types of posts from the microblogging platform.

The post needs to be public to embed. It cannot be a standalone image (with the URL name.tumblr.com/image). You can, however, embed image posts (with the URL name.tumblr.com/post/etc) and the rest of Tumblr’s post types including: Text, Quote, Link, Chat, Audio and Video.

An Example:

![Screenshot of a Tumblr post](../../../../assets/images/2020/11/image-1.png)

If you are looking to [import your Tumblr posts into WordPress](https://developer.wordpress.org/advanced-administration/wordpress/import/#tumblr), there is a process in the Tools section of your Dashboard.

Steps to embed a Tumblr post

1.  You need to find the link to the post. The easiest way to do this is to click on the three dots in the lower-right corner of the post and select Permalink.

![The correct URL to copy to use the embed block](../../../../assets/images/external/lh5.googleusercontent.com/f4a30a5805-TmIfoE_jKPstXEzX2laRIfPCIJguQnsnujfg8A4g3_4QxRTEoRQS0EcKbDZk.png)

2.  Copy the URL at the top of your browser. On a PC, press CTRL+A in the URL field and then CTRL+C to copy the URL. On a Mac, press ⌘+ A and then ⌘+C.
3.  Go to your post or page.
4.  Add the Tumblr block.

![Adding the Tumblr block to a page or post](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.19.06-PM.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../../working-with-blocks/adding-a-new-block.md)

5.  Paste the link in the text box and click the “Embed” button.

![Embed option for the Tumblr block to paste the URL.](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.23.08-PM.png)

6.  If the link can be embedded, you will see a preview in your editor.

![Preview of the embedded Video Press video within the WordPress editor.](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.23.54-PM.png)

If you cannot use that URL, an error message will popup saying “Sorry, this content could not be embedded.”

![Example of a URL that cannot be embedded. Two options are presented, try again or convert to link.](../../../../assets/images/2020/11/image-10.png)

If this happens you can: Try again with a different URL or convert it to a link.

## Block Toolbar

Besides the Mover and Drag & Drop Handle, the Block Toolbar for the Tumblr embed shows four buttons:

![Block Toolbar with options available for the Tumblr Block.](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.25.04-PM-1.png)

-   Transform to
-   Change alignment
-   Edit URL, and
-   More Options.

**Transform to**:

![Options to transform the Tumblr block to Paragraph, Columns or Group.](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.25.28-PM.png)

You can transform a Tumblr embed to a Group. This would give you the ability to change the background color around the Tumblr embed.

![Editor view of a Tumblr Embed as a group with Color Settings controls](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.26.16-PM.png)

*Editor view of an Tumblr Embed as a group with Color Settings controls*

![Tumblr Embed with a green background.](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.26.55-PM.png)

*Tumblr Embed with a green background.*

**Alignment:**

<img src="../../../../assets/images/2019/11/Screen-Shot-2019-11-23-at-12.20.27-PM.png" alt="Alignment options for the block: wide width, full width, align left, align center, and align right." width="162">

-   **Align left** – Make the Tumblr post left aligned
-   **Align center** – Make the Tumblr post alignment centered
-   **Align right** – Make the  Tumblr post align right
-   **Wide width** – Increase the width of the post beyond the content size
-   **Full width** – extend the Tumblr post to cover the full width of the screen.

“Wide width” and “Full width” alignment need to be enabled by the Theme of your site.

**Edit URL**

Via the edit URL, you can change the Tumblr Embed URL in the embed block. Overwrite the existing URL and click on the “Embed” Button.

![Editing the block URL via the "edit" option.](../../../../assets/images/2020/11/Screen-Shot-2020-11-25-at-10.27.55-PM.png)

**More Options:**

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../../working-with-blocks/more-options.md)

## Block Settings

**Media Settings**

New in 5.6: Resize the Tumblr post for smaller devices. It will preserve its aspect ratio when resized.

![Media settings for the embed block with the toggle OFF for resizing on smaller devices.](../../../../assets/images/2020/06/media-settings.png)

![Media settings for the embed block with the toggle ON for resizing on smaller devices.](../../../../assets/images/2020/11/image-27.png)

**Advanced**

The following Advanced settings options are available: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings.](../../working-with-blocks/block-settings/advanced-settings-overview.md)

## Changelog

-   Updated 2026-06-29
    -   Linked to advanced settings
-   Updated 2022-11-25
    -   Removed redundant content
    -   Aligned images for mobile view
    -   Added alt text to images
-   Updated 2020-11-26
    -   Screenshots as per WordPress 5.6
    -   Hide Block Settings changed to Hide More Settings
    -   Edit as HTML and Add to Reusable blocks removed
    -   Added Media Settings
-   Created 2020-11-25
