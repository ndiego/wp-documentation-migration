---
title: The Font Library
slug: the-font-library
position: 7
original_url: https://wordpress.org/documentation/article/the-font-library/
wp_id: 16360580
legacy_categories:
- customization
- appearance
date: '2024-10-17T12:11:36'
modified: '2026-07-26T05:24:54'
migration:
  status: clean
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2024/10/upload-font.mov
    local_path: docs/assets/videos/2024/10/upload-font.mov
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2024/10/Kapture-2026-05-23-at-07.04.39.mp4
    local_path: docs/assets/videos/2024/10/Kapture-2026-05-23-at-07.04.39.mp4
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2024/10/Kapture-2026-05-23-at-07.48.01.mp4
    local_path: docs/assets/videos/2024/10/Kapture-2026-05-23-at-07.48.01.mp4
  counts:
    images: 6
    internal_links_rewritten: 1
    self_hosted_videos: 3
---

# The Font Library

The Font Library lets you upload font files, install fonts from Google Fonts, and manage the fonts available on your site.. Starting in 7.0, it is available globally for [block themes](../themes/block-themes.md) and classic themes.

## Using the Font Library

The Font Library lives in the Admin menu under **Appearance > Fonts**.

![Fonts location in admin](../../assets/images/2024/10/Screenshot-2026-05-23-at-7.23.52-AM.jpg)

### Library

In the **Library** tab, view and manage fonts currently installed on your site, including fonts provided by your theme, uploaded fonts, and fonts installed from Google Fonts. Any newly added fonts will appear in this tab.

![Screenshot of the Library tab in the Manage Fonts panel in the WordPress editor, showing the available fonts. Fonts listed include Cardo (3 variants active), Inter (1 variant active), System Sans-serif (1 variant active), and System Serif (1 variant active).](../../assets/images/2024/10/2-library.png)

### Upload

In the **Upload** tab, upload a font file from your computer when the font you need is not already available. Make sure you have permission to use and distribute the font. The supported formats are .ttf, .otf, .woff, and .woff2.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2024/10/upload-font.mov"></video>

### Install Fonts

In the **Install Fonts** tab, browse and install fonts from Google Fonts for use on your site. WordPress downloads the selected font files and hosts them on your site rather than loading them from Google.

First, you need to give your site access to Google Fonts.

![Screenshot of the Install Fonts tab in the WordPress 'Manage Fonts' panel. The tab displays a prompt to Connect to Google Fonts, explaining that permission is required to connect directly to Google servers. Installed fonts will be stored locally on the site. It also explains how to upload fonts manually on the 'Upload' tab. A blue button labeled 'Allow access to Google Fonts' is at the bottom of the panel.](../../assets/images/2024/10/Google-Fonts.png)

You can revoke this access by clicking on the three dots button on the right.

![Screenshot of the Install Fonts tab in the WordPress Manage Fonts panel, showing a dropdown menu with the option to Revoke access to Google Fonts. The menu is accessed through the three-dot button in the upper right.](../../assets/images/2024/10/Revoke-access.png)

Find the font you wish to use using the search box. You can filter search results using the category dropdown menu at top right.

![Screenshot of the Google Fonts installation interface in WordPress, highlighting the search functionality. The search term 'Bodoni' is entered in the search bar on the left. Two results are displayed: 'Bodoni Moda' with 12 variants and 'Libre Bodoni' with 8 variants. A category dropdown is on the right, currently set to All.](../../assets/images/2024/10/6-font-search.png)

#### Install a Google Font

To install a font from Google Fonts:

-   Choose the desired font
-   Select the font variants in the next panel
-   Click install

You’ll see a notice indicating whether the font installed successfully. Newly installed fonts will appear in the Library tab.

The available variations will also appear in the Styles section.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2024/10/Kapture-2026-05-23-at-07.04.39.mp4" poster="../../assets/images/2024/10/Screenshot-2026-05-23-at-7.08.43-AM.jpg"></video>

## Removing fonts

![Fonts library with Delete and Update options](../../assets/images/2024/10/Screenshot-2026-05-23-at-7.18.14-AM.jpg)

To make specific font variants available or unavailable, select or clear their checkboxes, then click **Update**.

To completely remove the font family or single font, click on it, check the box for the font then click **Delete**. You’ll be prompted to confirm the deletion before the font family is uninstalled.

After a font is deleted, a “Font family uninstalled successfully” notice appears on the main Library tab.

## Change a default font

To update a block’s font across your site, navigate to **Appearance > Editor > Styles**.

From **Styles**, you can change the fonts used across your site or set a font for specific blocks, such as Heading or Paragraph. Available options depend on your theme.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2024/10/Kapture-2026-05-23-at-07.48.01.mp4" poster="../../assets/images/2024/10/Screenshot-2026-05-23-at-7.51.07-AM.jpg"></video>

## Changelog

-   Updated 2026-07-26 (props to @kjoyner @anujrathore24)
    -   Add intros to each tab description.
    -   Minor plain language upates.
-   Updated 2026-05-23 (props to @awetz583 @andfinally)
    -   Updated font menu location for 7.0
    -   Updated videos and screenshots
-   Created 2024-10-17
