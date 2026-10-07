---
title: Inserting images into posts and pages (Classic Editor)
slug: inserting-images-into-posts-and-pages-classic
original_url: https://wordpress.org/documentation/article/inserting-images-into-posts-and-pages-classic/
wp_id: 10851254
categories:
- support-guides
- media
date: '2018-11-06T03:14:27'
modified: '2024-06-06T17:21:33'
migration:
  status: clean
  counts:
    image_self_links_removed: 8
    images: 8
    images_missing_alt: 1
    internal_links_rewritten: 10
---

# Inserting images into posts and pages (Classic Editor)

## Overview

When creating or editing a WordPress page or blog post, you can easily add images at any time using the WordPress Media Uploader tool. Here’s how to add an image, step-by-step, using the media uploader:

## Step 1 – Placing your cursor

![Cursor at beginning of a paragraph](../../assets/images/2018/11/add-image-insert-cursor.png)

*Placing cursor where the image should appear*

In order to add an image to your page or post, you must first insert your cursor in the place in the text where you want the image to appear. By placing your cursor within your text, you can add images inline with your content. You can also place your cursor on a blank line if you want the image to appear by itself instead.<br>
<br>
*Tip: It’s a good idea to **place your cursor on the left margin of your text**, even if you want the image to appear on the right. That’s because there is a special setting called Alignment that allows you to control whether the image appears on the right or the left side of the text. It even controls how text flows around the image automatically.*

## Step 2 – Click the Add Media button

Once you’ve placed your cursor on the line where you want your image to appear, click on the Add Media button to launch the media uploader interface, and then select the Insert Media option from the list of actions in the left side of the media uploader window.

![Add Media button circled](../../assets/images/2018/11/add-media-button.png)

*“Add Media” button above editor*

## Step 3 – Add or Select Your Image

You can add or select the image you want to add to your page or post by choosing from either of the following options in the center of the media uploader window:

-   **Upload Files:** Upload the image you want to use from your computer by dragging it into the upload area.
-   **Media Library:** Select from any previously uploaded images in the media library by clicking on the one you wish to add to your page or post.

![](../../assets/images/2018/11/media-uploader.png)

Once you have selected or uploaded the image you want to add, You will see a checkbox next to the thumbnail confirming your selection, and see information about it displayed in the Attachment Details pane on the right hand side of the media uploader interface.

## Step 4 – Attachment Details

![Attachment details pane with: title, caption, alt text, and description](../../assets/images/2018/11/attachement-details.png)

*Attachment details*

The **Attachment Details** pane displays a small un-cropped thumbnail of the image, as well as important information such as the filename, date uploaded, and image dimensions in pixels.

There are also action links that allow you to **Edit Image**, which takes you to the page, or to **Delete Permanently** to remove the image from your site.

In addition, you can edit the following media information:

-   **Title:** The title of this media.
-   **Caption:** The caption for this image. The text you enter here will be displayed below the image.
-   **Alternate Text:** Enter the Alt text for the image, e.g. “The Mona Lisa” to describe the media.
-   **Description:** A description for this particular media.

For more information on these media settings, see the [Edit Media](edit-media.md) page.

## Step 5 – Attachment Display Settings

![Attachment display settings: alignment, link to, and size](../../assets/images/2018/11/attachment-display-settings.png)

*Attachment display settings*

The **Attachment Display Settings** pane controls how the image is displayed when viewed on the site.

You have options to set how you would like the image aligned on the page (in relation to the text and margins) and what the link behavior of the image will be, In addition you can set what size image you would like to display on your page.

### Image Alignment

The **Alignment** setting allows you to determine where you would like the image to appear in your content area and how it interacts with any text on the page. You have the following image alignment options to choose from:

-   **Left:** Aligns the image on the left hand margin, and any text that is on the page wraps (or flows) around the image to the available space on the right.
-   **Right:** Aligns the image on the right hand margin, and any text that is on the page wraps (or flows) around the image to the available space on the left.
-   **Center:** Aligns the image to the center of the page, with no text displayed around it.
-   **None:** Inserts the image in to the page with no alignment

![Different image alignments](../../assets/images/2018/11/750px-image-alignment-4up.png)

*Aligning images using editor controls*

### Image Link

The Link To settings determine the URL/web address to which the image will be linked when clicked on by a visitor to your site. You can specify the following image link settings:

-   **Attachment Page:** Links your inserted image to its WordPress media attachment page.
-   **Media File:** Links your inserted image directly to the original, full-size version of the file.
-   **Custom URL:** Allows you to set a custom link URL for your inserted image to link to when clicked.
-   **None:** This setting will remove the link completely, rendering the image “un-clickable”.

### Image Size

The Size settings determine the size of the image you are adding to your site. By default WordPress creates a range of four image size for you to choose from:

-   **Thumbnail:** Displays a small thumbnail-sized version of your image on the page/post. Note, by default the Thumbnail size is a square, so some cropping of your original image may occur.
-   **Medium:** Displays a medium-sized version of your image on the page/post. This is a good size to use with Left/Right alignments, as it leaves sufficient space for legible text to either side.
-   **Large**: Displays a large-sized version of your image on the page/post. Note: WordPress will determine the width of the content column of your theme, and display the largest possible image for that space.
-   **Full Size:** Displays a full-sized version of your image on the page/post. Note: WordPress will determine the width of the content column of your theme, and display the largest possible image for that space. If your original image is larger than this column width, the full size of the image may not be displayed.

![Different image sizes](../../assets/images/2018/11/750px-image-sizes-3up.png)

*Different image sizes*

You can visit the **[Settings > Media](../dashboard/settings-media-screen.md)** section of your WordPress dashboard to customize the above image sizes.

### Step 5 – Inserting the image

![Selecting the edit image option whenever hovering over an image](../../assets/images/2018/11/400px-re-edit-image.png)

*Edit image option*

Once you have determined your image settings, click on the blue Insert into post or Insert into the page button, to add the image to your page or post. After the image uploader window closes, you will see the image in the text editor window, including a preview of the alignment of the image, if you have specified an image alignment.

At any time, you can edit the image settings by clicking on the **Edit Image** button in the upper left hand corner. You can remove the image from your page/post by clicking on the **Remove Image** button.

## Further reading

-   [Media Add New Screen](../dashboard/media-add-new-screen.md)
-   [Edit Media](edit-media.md)
-   [Media library screen](../dashboard/media-library-screen.md)
-   [Settings Media Screen](../dashboard/settings-media-screen.md)
-   [Use Images](use-images.md)
-   [Use image and file attachments](use-image-and-file-attachments.md)
-   [Image Size and Quality](image-size-and-quality.md)
-   [Inserting Images into Posts and Pages (Block Editor)](inserting-images-into-posts-and-pages-block-editor.md)
