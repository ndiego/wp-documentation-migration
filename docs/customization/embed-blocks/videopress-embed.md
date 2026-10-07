---
title: VideoPress embed
slug: videopress-embed
original_url: https://wordpress.org/documentation/article/videopress-embed/
wp_id: 13174174
categories:
- customization
- embed-blocks
date: '2020-07-27T08:42:04'
modified: '2026-06-29T20:06:41'
migration:
  status: clean
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  counts:
    callouts: 3
    callouts_info: 3
    images: 14
    internal_links_rewritten: 4
  first_paragraph_is_nav_link: true
---

# VideoPress embed

[Go back to the list of **Blocks**](../block-editor/blocks-list.md)

With the VideoPress Embed block, you can embed videos from VideoPress into your posts and pages. You don’t need a VideoPress account to be able to embed them, although the video-sharing option should be enabled.

**Steps to embed a video from VideoPress**

1.  Find the video permalink – In the web player, select the video and click on the **Share** button.

![Screenshot of VideoPress share button](../../assets/images/2020/07/videopress-share-button.png)

2.  In the share section, click on the permalink and it will be automatically copied. Alternatively, you can highlight the link and copy it.

![The correct URL to copy to use the VideoPress block](../../assets/images/2020/07/videopress-copy-link.png)

VideoPress provides you with three sharing options:

-   Start at = true/false to exactly the time you want the video to start at.
-   Loop = true/false to automatically play the video over and over.
-   Autoplay = true/false to automatically play the video when it loads.

3.  Add a VideoPress embed block to your page/post by clicking the **(+)** Block inserter icon.

![VideoPress Embed Block](../../assets/images/2020/07/Annotation-on-2026-06-26-at-14-23-39.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../block-editor/adding-a-new-block.md)

4.  Paste the link into the text box and click on the **Embed** button.

![Embed option for the VideoPress block to paste the URL.](../../assets/images/2022/12/image2-1.png)

If it’s a link that can be successfully embedded you will see a preview in your editor.

![Preview of the embedded VideoPress video within the WordPress editor.](../../assets/images/2020/07/Screenshot-on-2026-06-26-at-02-24-57.png)

If you use an URL that can’t be embedded, the block shows the message “Sorry, this content could not be embedded.” You will have two choices: **Try again** with a different URL or **Convert to link**.

![Example of a URL that cannot be embedded. Two options are presented, try again or convert to link.](../../assets/images/2020/07/Screenshot-on-2026-06-26-at-02-26-18.png)

5.  Click on **Preview** to see how it will look on the front-end.

![Preview of the embedded VideoPress video within the WordPress editor.](../../assets/images/2020/07/Screenshot-on-2026-06-26-at-02-28-21.png)

## Block toolbar

Besides the “Mover” and “Drag & Drop Handle”, the Block Toolbar for the VideoPress Embed block shows four buttons:

-   Transform to
-   Change Alignment
-   Edit URL, and
-   More Options

![Block Toolbar with options available for the VideoPress Block.](../../assets/images/2022/12/image4-2.png)

**Transform to**

![Options to transform the VideoPress block to Paragraph, or Group.](../../assets/images/2020/07/Annotation-on-2026-06-26-at-14-30-33.png)

You can transform a VideoPress embed into a Group. This would give you the ability to change the background color around the VideoPress embed.

![Editor view of a VideoPress embed as a group with Color Settings controls](../../assets/images/2020/08/image7.png)

*Editor view of a VideoPress embed as a group with Color Settings controls*

![VideoPress embeds with a blue background-color](../../assets/images/2020/07/image-71.png)

*VideoPress embeds with a blue background-color*

**Change alignment**

![Alignment options for the VideoPress block: wide width, full width, align left, align center, and align right.](../../assets/images/2022/12/image12.png)

-   **Align left** – Make the VideoPress post. left aligned.
-   **Align center** – Make the VideoPress post alignment centered.
-   **Align right** – Make the VideoPress post, right aligned.
-   **Wide width** – Increase the width of the post beyond the content size.
-   **Full width** – Extend the VideoPress post to cover the full width of the screen.

**Wide width** and **Full width** alignment need to be enabled by the theme of your site.

**Edit URL**

Using the **Edit URL** button, you can change the VideoPress Embed URL in the embed block. Overwrite the existing URL and click on the **Embed** button.

![Editing the block URL via the "edit" option.](../../assets/images/2022/12/image2-3.png)

**More options**

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../block-editor/more-options.md)

## Block settings

Besides the **Advanced** section, the VideoPress embed has only one setting in the **Block Settings** sidebar.

**Media**

![Media settings for the embed block with the toggle OFF/ON for resizing on smaller devices.](../../assets/images/2020/07/image-76.png)

Via the **Media Settings**, you can control the behavior of your post embed when viewed from a smaller device, like on a phone screen.

The Toggle switch turns on or off the resize functionality for smaller devices. The default setting is “on” or blue.

**Off:** This embed may not preserve its aspect ratio when the browser is resized. In the **Off** position, the toggle switch is gray.

**On:** This embed will preserve its aspect ratio when the browser is resized. The toggle switch turns blue in the **On** position.

**Advanced**

The following Advanced settings options are available: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings.](../block-editor/advanced-settings-overview.md)

## Changelog

-   Updated 2026-06-29
    -   Linked to advanced settings
-   Updated 2022-11-25
    -   Removed redundant content
    -   Aligned images for mobile view
    -   Added alt text to images
-   Updated “More Options” sections: replaced screenshot and added text for “Move to” and “Copy”
-   Updated 2020-08-19
    -   Replaced “More Options” – new screenshot
    -   Added “Move To” and “Copy” section under More Options
-   Updated 2020-08-11
    -   Screenshots as per WordPress 5.5
    -   Embedded VideoPress video
-   Created 2020-07-27
