---
title: Create a static front page
slug: create-a-static-front-page
position: 5
original_url: https://wordpress.org/documentation/article/create-a-static-front-page/
wp_id: 10846138
legacy_categories:
- support-guides
- publishing
date: '2021-07-02T15:25:18'
modified: '2026-07-02T01:22:24'
migration:
  status: warnings
  warnings:
  - contained VideoPress embed (now a bare oEmbed URL; verify it auto-embeds after import)
  videos:
  - type: videopress
    guid: MFhssVqN
    url: https://videopress.com/v/MFhssVqN
    original: https://videos.files.wordpress.com/MFhssVqN/414145913-c4a5cfce-86a3-4061-9963-598a50bc7435.mp4
    poster: https://videos.files.wordpress.com/MFhssVqN/414145913-c4a5cfce-86a3-4061-9963-598a50bc7435_mp4_hd_1080p.original.jpg
    media_id: 16369126
  - type: videopress
    guid: CbDPoRL9
    url: https://videopress.com/v/CbDPoRL9
    original: https://videos.files.wordpress.com/CbDPoRL9/414145993-49175d17-b882-4d06-82b8-dbc96fb17b22.mp4
    poster: https://videos.files.wordpress.com/CbDPoRL9/414145993-49175d17-b882-4d06-82b8-dbc96fb17b22_mp4_hd_1080p.original.jpg
    media_id: 16369128
  counts:
    images: 2
    internal_links_rewritten: 1
    videopress: 2
---

# Create a static front page

The purpose of this document is to explain the process of setting up a static page on your WordPress site. This document doesn’t discuss the automatic display of posts on the Home page. It is a pre-requisite that you understand the difference between the [Pages](../create-pages.md) and Posts.

## What is a Static Front Page

By default, WordPress displays your latest posts on the homepage of your site. This dynamic list updates automatically whenever new posts are published, meaning it is not a static page.

A Static Front Page, on the other hand, is **a specific page** that you manually set as your homepage. Instead of displaying recent posts, this page remains unchanged unless edited, allowing you to create a custom landing page for your site.

## Create a Home Page

1.  Navigate to your WordPress dashboard.
2.  Go to Pages > Add New.
3.  Title this page (e.g., “Home”) and add the desired content.
4.  Publish the page.

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/MFhssVqN -->

https://videopress.com/v/MFhssVqN

## How to set a Static Front Page

*Reminder: to create a page, go to **Pages > Add New***

There are two places you can set your static front page, depending on your theme and preference: through **Reading Settings**, or through the **Customizer**.

#### Option 1: Using Reading Settings

1.  Navigate to Settings > Reading in your dashboard.
2.  Under “Your homepage displays,” select “A static page.”
3.  For “Homepage,” choose the “Home” page you created.
4.  For “Posts page,” select the “Blog” page if required.
5.  Save the changes.

![How to create a Static Front Page](../../../assets/images/2021/06/Screen-Shot-2021-06-23-at-2.04.35-PM.png)

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/CbDPoRL9 -->

https://videopress.com/v/CbDPoRL9

#### Option 2: Using the Customizer

1.  Go to **Appearance > Customize**.
2.  Click on **Homepage Settings**.
3.  Under ‘Your homepage displays’, **select a static page**.
4.  In the **Homepage** dropdown, **select the page you want** to use as your Static Front (Home) Page.
5.  If you want a separate page for your blog posts, use the **Posts page** dropdown to select the empty page you created.
6.  Click **Publish** to save your changes.

![Home Page Settings within the WordPress Customizer](../../../assets/images/2021/07/Screenshot-2026-07-02-at-1.16.10-PM.png)

Your homepage should now show the Page you selected.

## Changelog

-   Update 2026-06-25
    -   Simplified instructions and added tutorial videos (props @benazeer)
-   Update 2026-04-05
    -   Fix the intro paragraph (props @noumantech, @estelaris)
