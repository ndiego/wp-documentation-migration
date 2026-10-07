---
title: Speaker Deck embed
slug: speaker-deck-embed
original_url: https://wordpress.org/documentation/article/speaker-deck-embed/
wp_id: 13173655
categories:
- customization
- embed-blocks
date: '2020-07-27T06:27:07'
modified: '2026-06-29T20:03:59'
migration:
  status: warnings
  warnings:
  - 'external images hotlinked from user-images.githubusercontent.com: 9 (see assets/images-manifest.json)'
  counts:
    callouts: 3
    callouts_info: 3
    images: 13
    internal_links_rewritten: 3
---

# Speaker Deck embed

The Speaker Deck embed block will allow users to embed their own slides/presentation in their post/page. Users need to create an account to upload their own slides/presentation on Speaker Deck. You don’t need a Speaker Deck account to embed a presentation, although it needs to be public.

**Embedded Speaker Deck Slide**

![Screenshot of Speaker Deck](../../assets/images/2020/07/image-48.png)

**Steps to Embed a slide from Speaker Deck**

1.  Find the URL of your Speaker Deck slide

Log in to your Speaker Deck account and visit the My Decks menu to get your all decks

![Screenshot of Speaker Deck](../../assets/images/2020/07/image-49.png)

Open the deck that you want to embed. After that Copy the link from the browser address bar.

2.  Add the Speaker Deck block from the block list

![Screenshot adding the Speaker Deck block to a page or post](../../assets/images/external/user-images.githubusercontent.com/072b9f065f-161037725-85bd3595-c839-4312-93c0-ec6f9c70a21b.png)

> [!NOTE]
> [Detailed instructions on adding blocks](../block-editor/adding-a-new-block.md)

3.  Paste the Deck link into the URL box

![The correct URL to copy to use the embed block](../../assets/images/external/user-images.githubusercontent.com/45af20c5ac-161038851-7a051c65-9e37-4a4f-8d55-47c48b334253.png)

4.  Click the “Embed” button

If it’s a link that can be successfully embedded you will see a preview in your editor.

![Preview of the embedded Speaker Deck video within the WordPress editor.](../../assets/images/external/user-images.githubusercontent.com/b254b85a82-161039067-69b1a744-1aa1-4b7e-b2a9-323e43832089.png)

5.  If you use a URL that can’t be embedded, the block shows the message *“Sorry, this content could not be embedded.”* You will have two choices: Try again with a different URL or convert to link.

![Example of a URL that cannot be embedded. Two options are presented, try again or convert to link.](../../assets/images/external/user-images.githubusercontent.com/67add3720a-161039572-ca4f6d43-3d9c-4195-9de2-32f31e620bcf.png)

## Block Toolbar

Besides the Mover and Drag & Drop Handle, the Block Toolbar for the Speaker Deck embed shows four buttons:

-   Transform to
-   Change alignment
-   Edit URL, and
-   More Options.

![Block Toolbar with options available for the Speaker Deck Block.](../../assets/images/external/user-images.githubusercontent.com/bdab7d54a9-164016766-bdbd8008-0e92-465d-ab5a-d0c98ea62d49.png)

**Transform to**:

![Options to transform the Speaker Deck block to Paragraph, Columns or Group.](../../assets/images/external/user-images.githubusercontent.com/8f6c10e898-161039947-ef59200b-6e10-4f53-9ec4-9022fcd50990.png)

You can transform a Speaker Deck embed to a Group. This would give you the ability to change the background color around the Speaker Deck embed.

![Editor view of an Speaker Deck Embed as a group with Color Settings controls](../../assets/images/external/user-images.githubusercontent.com/7342497ff5-161040416-6121804a-2642-4fa5-bad5-a639c4fa44e6.png)

*Editor view of an Speaker Deck Embed as a group with Color Settings controls*

**Change Alignment**

![Speaker Deck Embed with a grey background.](../../assets/images/external/user-images.githubusercontent.com/9ea2ad6a32-161040849-29b189d4-05b5-4825-bd36-cf46077089b8.png)

-   **None** – No alignment.
-   **Align left** – Make the Speaker Deck post left aligned
-   **Align center** – Make the Speaker Deck post alignment centered
-   **Align right** – Make the  Speaker Deck] post align right

**Edit URL**

Via the edit URL, you can change the Speaker Deck Embed URL in the embed block. Overwrite the existing URL and click on the “Embed” Button.

![Editing the block URL via the "edit" option.](../../assets/images/external/user-images.githubusercontent.com/de0bc47d29-161041061-35fc54ec-4b16-4d11-b18f-00fed34568ec.png)

**More Options:**

These controls give you the option to copy, duplicate, and edit your block as HTML.

> [!NOTE]
> [Read about these and other settings.](../block-editor/more-options.md)

## Block Settings

Besides the Advanced section, the Speaker Deck embed has only one setting in the “Block Settings” sidebar: Media Settings.

**Media Settings**

![Media settings for the embed block with the toggle OFF for resizing on smaller devices.](../../assets/images/2020/07/image-29.png)

![Media settings for the embed block with the toggle ON for resizing on smaller devices.](../../assets/images/2020/07/image-28.png)

Via the Media Settings you can control the behavior of your post embed when viewed from a smaller device, like on a phone screen.

The Toggle switch turns on or off the resize functionality for smaller devices. The default setting is “on” or blue.

**“Off:”** This embed may not preserve its aspect ratio when the browser is resized. In the off position the toggle switch is gray.

**“On:”** This embed will preserve its aspect ratio when the browser is resized. The toggle switch turns blue in the “On” position.

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
-   Updated 2022-04-19
    -   Updated screenshots for 5.9
-   Updated 2020-09-04
    -   Screenshots updated to 5.5
-   Updated 2020-08-19
    -   Replaced “More Options” – new screenshot
    -   Added “Move To” and “Copy” section under More Options
-   Updated 2020-08-11
    -   Screenshots as per WordPress 5.5
    -   Embedded VideoPress video
-   Created 2020-07-27
