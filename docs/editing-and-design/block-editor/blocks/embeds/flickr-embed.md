---
title: Flickr embed
slug: flickr-embed
position: 9
original_url: https://wordpress.org/documentation/article/flickr-embed/
wp_id: 13050803
legacy_categories:
- customization
- embed-blocks
date: '2020-06-30T08:49:29'
modified: '2026-06-29T19:42:35'
migration:
  status: clean
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2022/10/Flickr-Embed-HelpHub-Oct-2022.mp4
    local_path: docs/assets/videos/2022/10/Flickr-Embed-HelpHub-Oct-2022.mp4
  counts:
    callouts: 3
    callouts_info: 3
    edge_br_removed: 11
    images: 16
    internal_links_rewritten: 4
    self_hosted_videos: 1
    small_images_kept_as_html: 1
  nav_link_removed: true
---

# Flickr embed

With the Flickr embed block, you can add photos and videos from Flickr to your posts and pages. However, when you click any photo or video, it will take you to Flickr where you can see photos and play videos.

You can also embed photo albums and galleries with the next/previous arrow links. You don’t need a Flickr account to embed photos or videos.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2022/10/Flickr-Embed-HelpHub-Oct-2022.mp4"></video>

Note: With video, the page/post only displays the image of the video. There will be no play/pause button. By clicking on the video, it will be redirected to the corresponding Flickr page to play.

You can only share those photos and videos which are visible to everyone(public). Some publishers put restrictions by setting privacy.

![Privacy settings options available on Flickr](../../../../assets/images/2020/06/image23.png)

**Embedded image from flickr**

![Preview of an embedded image from Flickr](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-1-1.png)

**Steps to embed Flickr photos or videos to your post or page**

1.  Find your photo or video on Flickr.com, and copy the URL of the photo, album, gallery or video from the browser bar.

![Choosing an image from Flickr](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-2-2.png)

2.  Add Flickr embed block to your post or page

<img src="../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-3.png" alt="Adding a Flickr block with the slash command." width="234">

> [!NOTE]
> [Detailed instructions on adding blocks](../../working-with-blocks/adding-a-new-block.md)

3.  Paste the link into the textbox.

![Embed URL for Flickr block.](../../../../assets/images/2020/08/Flickr-Block-URL-WP5.5r-8.3.png)

4.  Click the “Embed” button

If the link can be successfully embedded into the post/page, you will see the preview in your block editor.

![Example of an embedded Flickr block on the backend.](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-4-1.png)

If you use a URL that can’t be embedded, the block shows the message “Sorry, this content could not be embedded.” You will have two choices: Try again with a different URL or convert to link.

![Example of error message for the Flickr block.](../../../../assets/images/2020/08/not-embedding-WP5.5r8.3.png)

5.  Click on the Preview button on the top right corner of the page/post.

![Preview of the Flickr embed.](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-1-1-1.png)

**Embed Photo Album and Gallery**

You can embed a photo album and gallery to your post/page. The page/post will display the first photo of the album or gallery with the next and previous arrow link.

![Embedded a photo album or gallery with Flickr.](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-5.png)

## Block Toolbar

The Block Toolbar for the Flickr embed shows six buttons:

-   Embed
-   Change block type or style
-   Drag / Move down
-   Change alignment
-   Edit URL
-   Options.

![Block toolbar for the Flickr embed block.](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-6.png)

**Transform to:**

![Transform to options for the Flickr embed block.](../../../../assets/images/2022/10/Flickr-HelpHub-Oct-2022-SS-7-1.png)

**Group**

You can transform a Flickr embed into a Group. This would give you the ability to change the background color around the Flickr embed.

![Group options for the Flickr embed block.](../../../../assets/images/2022/10/Screen-Shot-2022-10-28-at-3.02.47-PM-1.png)

Left: Editor view of a Flickr Embed as a group with Color Settings controls

Right: Flickr embeds with a green background.

**Change Alignment**

![Changing alignment for the Flickr embed block.](../../../../assets/images/2022/10/Screen-Shot-2022-10-28-at-2.58.55-PM.png)

-   **Align left** – Make the Flickr post left aligned
-   **Align center** – Make the Flickr post alignment centered
-   **Align right** – Make the  Flickr post-align-right
-   **Wide width** – Increase the width of the post beyond the content size
-   **Full width** – extend the Flickr post to cover the full width of the screen.

**Note:** “Wide width” and “Full width” alignment needs to be enabled by the Theme of your site.

**Edit URL**

Via the edit URL, you can change the Flickr Embed URL in the embed block. Overwrite the existing URL and click on the “Embed” Button.

![Edit the URL for the Flickr embed block.](../../../../assets/images/2020/08/Edit-Post-WP5.5r8.3.png)

**More Options**

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../../working-with-blocks/more-options.md)

## Block Settings

### Media settings

![Media settings for the Flickr embed block - set to Resize for smaller devices ON.](../../../../assets/images/2022/10/Screen-Shot-2022-10-28-at-3.08.53-PM.png)

![Media settings for the Flickr embed block - set to Resize for smaller devices OFF.](../../../../assets/images/2022/10/Screen-Shot-2022-10-28-at-3.08.56-PM.png)

Via the Media Settings, you can control the behavior of your post embed when viewed from a smaller device, like on a phone screen.

The Toggle switch turns on or off the resize functionality for smaller devices. The default setting is “on” or blue.

“Off:” This embed may not preserve its aspect ratio when the browser is resized. In the off position, the toggle switch is gray.

“On:” This embed will preserve its aspect ratio when the browser is resized. The toggle switch turns blue in the “On” position.

**Advanced**

The following Advanced settings options are available: HTML Anchor, Additional CSS Class(es), Additional CSS, and Styles.

> [!NOTE]
> [Learn more about advanced settings.](../../working-with-blocks/block-settings/advanced-settings-overview.md)

## Changelog

-   Updated 2026-06-29
    -   Linked to advanced settings
-   Updated 2022-11-25
    -   Removed redundant content
-   Updated 2022-10-28
    -   Added Video walkthrough
    -   Updated Screenshots as per WordPress 6.0
    -   Added Alt text to images
    -   Added locking functionality
-   Updated 2020-08-18
    -   Added “Move To” and “Copy” section under More Options
-   Updated 2020-08-17
    -   Screenshots as per WordPress 5.5
-   Created 2020-06-30
