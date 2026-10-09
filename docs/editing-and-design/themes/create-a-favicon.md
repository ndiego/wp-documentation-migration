---
title: Create a Favicon
slug: create-a-favicon
position: 4
original_url: https://wordpress.org/documentation/article/create-a-favicon/
wp_id: 10846004
legacy_categories:
- customization
- appearance
date: '2018-11-04T09:50:08'
modified: '2025-04-25T10:09:45'
migration:
  status: clean
  counts:
    edge_br_removed: 3
    image_self_links_removed: 1
    images: 2
    internal_links_rewritten: 2
    legacy_support_links_fixed: 1
    relative_url_made_absolute: 1
    tables_gfm: 1
    tables_without_header_row: 1
    version_links_kept_absolute: 2
---

# Create a Favicon

A *favicon* (short for “favorite icon”) is an icon associated with a particular website or web page. It is generally intended to be used when you bookmark a web page. Web browsers use them in the URL bar, on tabs, and elsewhere to help identify a website visually. Favicons are also used as application icons on mobile devices.

## WordPress Version 6.5 or later

WordPress [Version 6.5](https://wordpress.org/documentation/wordpress-version/version-6-5/) moved the site icon to **General Settings**.

Follow the steps below to set **Site Icon** from General settings.

1.  Prepare the image file and upload to media library. (It must be square, having a height and width of at least 512 px. and a .png is the recommended format)
2.  Navigate to [General Settings](../../using-wordpress/administration-screens/settings/settings-general-screen.md)
3.  Click Choose a Site icon.
4.  Select image file that you prepared in the previous step.

![screenshot of the general settings tab where the site icon is added in WordPress since version 6.5](../../assets/images/2018/11/6-5-favicon-general-settings.png)

## WordPress Version 4.3 to 6.4

WordPress [Version 4.3](https://wordpress.org/documentation/wordpress-version/version-4-3/) implemented a Site Icon feature that enables favicons on your web site.

When you use the Site Icon feature, you don’t need to prepare the `favicon.ico` file by yourself, or modify your template file. All you have to do is navigate to the Customize screen and specify a square image that has a height and width of at least 512 px.

Later paragraphs in this article contain instructions for manually setting up your own favicon. However, it is highly recommended that you use the Site Icon feature (a feature that is built-in to WordPress) instead.

Follow the steps below to use Site Icon to set up a favicon for your site.

1.  Prepare the image file. (It must be square, having a height and width of at least 512 px.)
2.  Navigate to [Administration Screen](../../using-wordpress/administration-screens/README.md) > Appearance > Customize
3.  Click **Site Identity**
4.  Click **Select Image** (located under the **Site Icon** subheading).
5.  Click on the **Upload Files** tab, then click **Select Files** to upload the image file that you prepared in the previous step.

![customizer-siteicon](../../assets/images/2018/11/customizer-siteicon.jpg)

|  |
| --- |
| **Changelog**<br>**April 25, 2025** – Added the update for 6.5 and removed outdated sections: <br>– Creating a Favicon<br>– Installing a Favicon in WordPress<br>– How to create a favicon with a transparent background<br>– Advantages of using .ico over .png or .gif |
