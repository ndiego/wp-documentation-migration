---
title: Twitter embed
slug: twitter-embed
original_url: https://wordpress.org/documentation/article/twitter-embed/
wp_id: 12713819
categories:
- customization
- embed-blocks
date: '2020-04-22T17:23:19'
modified: '2026-06-29T19:26:09'
migration:
  status: warnings
  warnings:
  - contained x embed (now a bare oEmbed URL; check provider support)
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  counts:
    callouts: 3
    callouts_info: 3
    images: 16
    images_missing_alt: 2
    internal_links_rewritten: 4
    nested_emphasis_unwrapped: 6
    small_images_kept_as_html: 1
  first_paragraph_is_nav_link: true
---

# Twitter embed

[Go back to the list of **Blocks**](../block-editor/blocks-list.md)

With the Twitter Embed block, you can embed Tweets (posts on Twitter) into your posts and pages. You don’t need a Twitter account to be able to use it. You can only embed public tweets, though.

**An example:**

<!-- x embed -->

https://twitter.com/WordPress/status/1247690005516034048?ref_src=twsrc%5Etfw

Apart from a single tweet you can also use the block to add:

-   Profile links – shows the latest tweets from a user.
-   Twitter List – shows the latest tweets from a Twitter List.

**Steps to embed a Tweet**

1.  **You need to find the URL of the Tweet**<br>
    Like other social networks, the post date of a single Tweet is linking to the single tweet view. To grab the URL, point your mouse to the date, using the right mouse click menu select Copy Link Address.

![Steps to get the URL for the tweet you want to embed](../../assets/images/2020/04/Screen-Shot-2020-04-22-at-9.30.14-AM.png)

Depending on the version of Twitter Interface (Mobile or Desktop) you can also use the left option <img src="../../assets/images/2020/04/Twitter-CopyLInk-menu-icon.jpg" alt="" width="24">on the bottom of the tweet

![Steps to get the URL for the tweet you want to embed](../../assets/images/2020/04/Screen-Shot-2020-04-22-at-9.34.35-AM.png)

2.  **Go to your post or page**
3.  **Add the Twitter block**

![How to add the twitter embed block](../../assets/images/2022/02/twitter-block-insert-wp-5-9.png)

*Insert a Twitter block*

> [!NOTE]
> [Detailed instructions on adding blocks](../block-editor/adding-a-new-block.md)

4.  **Paste the link into the text box and click the “Embed” button**

![Twitter block embed view](../../assets/images/2022/02/twitter-block-embed-link.png)

*Twitter block embed view*

If it’s a link that can be successfully embedded you will see a preview in your editor.

![Display of the tweet embed in editor](../../assets/images/2022/02/twitter-block-embed-success-5-9.png)

If you use an URL that can’t be embedded, the block shows the message *“Sorry, this content could not be embedded.”*

You will have two choices: Try again with a different URL or convert it to a link.

![URL to embed the twitter pot](../../assets/images/2022/02/twitter-block-embed-fail.png)

6.  **Click on “Preview” to see how it will look on the front-end**

![](../../assets/images/2020/04/Screen-Shot-2020-04-22-at-9.52.52-AM.png)

## Block Toolbar

Besides the “Mover” and “Drag & Drop Handle”, the Block Toolbar for the Twitter Embed block shows four buttons:

-   Transform to – also the icon for the block.
-   The drag handle
-   The move up and down options
-   Change alignment
-   Edit URL, and
-   More Options.

![Block toolbar for the twitter block](../../assets/images/2022/02/twitter-block-toolbar-5-9.png)

**Transform to**:

![How to transform the block to a different one](../../assets/images/2022/02/twitter-block-embed-transform-to-5-9.png)

You can transform a Twitter embed to a Paragraph. This will convert the tweet embed to a link.

You can transform a Twitter embed to Columns.

You can transform a Twitter embed to a Group. This would give you the ability to change the background color around the Twitter embed.

![Editor view of an Twitter Embed as a group with Color Settings controls](../../assets/images/2020/04/Screen-Shot-2020-04-22-at-10.13.25-AM.png)

![Twitter embed with a blue background.](../../assets/images/2020/04/Screen-Shot-2020-04-22-at-10.13.40-AM.png)

*Left: Editor view of an Twitter Embed as a group with Color Settings controls<br> Right: Twitter embed with a blue background.*

**Change Alignment**

![Block alignment](../../assets/images/2022/02/twitter-block-toolbar-alignment-5-9.png)

-   **None – Default alignment option.**
-   **Wide width – Increase the width of the post beyond the content size.**
-   **Full width – Extend the block to cover the full width of the screen.**
-   **Align left – Make the block left-aligned.**
-   **Align center – Make the block alignment centered.**
-   **Align right – Make the block right aligned.**

“Wide width” and “Full width” alignment need to be enabled by the Theme of your site.

**Edit URL**

Via the edit URL, you can change the Twitter Embed URL in the embed block. Overwrite the existing URL and click on the “Embed” Button on the right.

![How to edit the URL of the tweet](../../assets/images/2022/02/twitter-block-embed-fail.png)

**More Options**

> [!NOTE]
> [Read about these and other settings.](../block-editor/more-options.md)

## Block Settings

Besides the Advanced section, the Twitter embed has only one setting in the “Block Settings” sidebar: Media Settings.

**Media Settings**

![Media settings to control the behaviour of your post embed](../../assets/images/2020/04/Screen-Shot-2020-04-20-at-9.29.46-AM.png)

![Media settings to control the behaviour of your post embed](../../assets/images/2020/04/Screen-Shot-2020-04-20-at-9.29.55-AM.png)

Via the *Media Settings* you can control the behavior of your post embed when viewed from a smaller device, like on a phone screen.

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
-   Updates 2022-11-27
    -   Removed redundant content
    -   Added alt text to images
-   Updated 2022-02-04
    -   Replace images with new screenshots for WordPress 5.9
    -   Updated text information for more settings for capitalisation
-   Updated 2020-08-18
    -   Replaced “More Options” – new screenshot
    -   Added “Move To” and “Copy” section under More Options
-   Updated: 2020-06-20
    -   Fixed typos
-   Updated: 2020-06-04
    -   Fixed typos
-   Updated: 2020-04-24
    -   Added it to the Embed Blocks category
-   Created 2020-04-22
