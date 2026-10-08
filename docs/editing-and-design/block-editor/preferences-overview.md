---
title: Preferences overview
slug: preferences-overview
position: 3
original_url: https://wordpress.org/documentation/article/preferences-overview/
wp_id: 14657194
legacy_categories:
- customization
- block-editor
date: '2021-07-13T21:19:17'
modified: '2025-11-25T14:05:32'
migration:
  status: clean
  notes:
  - link to old slug 'wordpress-editor' rewritten to 'wordpress-block-editor' (via 301)
  - link to old slug 'settings-sidebar' rewritten to 'page-post-settings-sidebar' (via 301)
  videos:
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2021/07/show-starter-patterns.webm
    local_path: docs/assets/videos/2021/07/show-starter-patterns.webm
  - type: self-hosted
    url: https://wordpress.org/documentation/files/2021/07/enable-custom-fields.webm
    local_path: docs/assets/videos/2021/07/enable-custom-fields.webm
  counts:
    images: 15
    images_missing_alt: 2
    internal_links_rewritten: 8
    self_hosted_videos: 2
---

# Preferences overview

When you start using the [WordPress Block Editor](wordpress-block-editor.md) or the [Site Editor](../site-editor/README.md) and you find the number of choices and panels overwhelming, you can use the Preferences feature to turn on/off the various options, to your liking. This helps to remove the distracting elements in the layout that get in the way of your writing and create an editing experience that you prefer.

## How to find Preferences

In the [WordPress Block Editor](wordpress-block-editor.md) or the [Site Editor](../site-editor/README.md), select the three vertical dots icon in the upper-right corner of the top toolbar. This opens up a drop-down menu. Select **Preferences** to open the **Preferences** dialog.

![Image showing the three dot menu > Preferences](../../assets/images/2021/07/editor-preferences.jpg)

*Image showing the three dot menu > Preferences*

## Preferences in the WordPress Block Editor

This section covers preference settings when you are in the [WordPress Block Editor](wordpress-block-editor.md).

### General

![General tab in Preferences in WordPress Block Editor](../../assets/images/2021/07/preferences-general.jpg)

*General tab in Preferences in WordPress Block Editor*

**Interface**

-   **Always open list view:** When you toggle this on, the list view sidebar is open by default every time you open the Block Editor.

![Always show list view](../../assets/images/2023/10/Always-show-list-view.png)

-   **Show block breadcrumbs**: When you toggle this one, WordPress Block Editor shows block breadcrumbs at the bottom of the editor. Block breadcrumbs allow you to easily get a sense of where you are in the content and offer a way to easily select parent blocks. This is particularly helpful when you’re dealing with layers of nested blocks or more complicated arrangements.

![Display block breadcrumbs](../../assets/images/2022/10/Screen-Shot-2022-10-25-at-2.09.44-PM.png)

**Allow right-click contextual menus**

**Show starter patterns**: display all starter patterns in a modal when creating a new page.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2021/07/show-starter-patterns.webm"></video>

**Document settings**: This section lets you choose what panels appear in the [Page/Post Settings Sidebar](page-post-settings-sidebar.md). If you toggle an item off here, it will hide that section in the [page/post settings sidebar](page-post-settings-sidebar.md). If you find that you don’t use a specific panel in the settings sidebar and want to simplify your editing experience, this option is helpful.

**Publishing:** This lets you customize the options related to publishing a post or page.

-   **Include pre-publish checklist**: By toggling this on, you are enabling an extra step to appear before publishing a post/page. You will be asked to review the settings for **Visibility** and **Publish date** and add settings such as **Categories** and **Tags**. This checklist will only appear after you click **Publish**. You can make the relevant changes and click **Publish** one more time to Publish the post/page.

![Pre publish checklist enabled](../../assets/images/2022/10/Screen-Shot-2022-10-25-at-12.36.27-PM.png)

**Advanced**: This section lets you add extra areas to the editor.

<video controls preload="metadata" src="https://wordpress.org/documentation/files/2021/07/enable-custom-fields.webm"></video>

### Appearance

![](../../assets/images/2021/07/preferences-appearance.jpg)

**Appearance**: This section covers preferences that are specifically related to how the editor looks and feels.

-   **Top toolbar**

![Top Toolbar when the option is turned off](../../assets/images/2023/10/Top-Toolbar-off.png)

_**Top Toolbar** when the option is turned off_

![Top Toolbar when the option is turned on](../../assets/images/2023/04/button-text-top-toolbar-WP-62-1024x57.png)

_**Top Toolbar** when the option is turned on_

-   **Distraction free**: When you toggle this on, it creates a clean interface with fewer distractions while you’re writing. WordPress turns off various options and panels in the toolbar and removes breadcrumbs at the bottom of the editor. **Keep in mind that these options don’t go away!** They are simply hidden while you’re writing.<br>
    Hovering over or moving focus to the top part of the editor reveals a limited toolbar with selection tools, undo and redo, save, publish, and the button with the tree dots, which opens the options menu.

![New Post Created](../../assets/images/2023/10/Add-Post-1.png)

-   **Spotlight mode**: When you toggle this on, WordPress Block Editor is set to Spotlight mode. All blocks are greyed out except for the one you’re working on so that you can focus on a single block at a time.

![Spotlight mode](../../assets/images/2022/05/Screen-Shot-2022-05-12-at-10.01.48-PM-1.png)

*Spotlight mode*

-   **Use theme styles**: This option is what allows your editor to look like your theme so that, as you’re creating content, you have a strong sense of what it will look like upon publishing. If you’d rather focus on the content itself and not necessarily on how it will look, you can toggle this option off to have your theme styles removed.

### Accessibility

![](../../assets/images/2021/07/preferences-accessibility.jpg)

-   **Contain text cursor inside block**: This option aids screen readers by stopping the text caret from leaving blocks.

-   **Show button text labels**: When you toggle this option, it allows you to show text instead of icons in the Toolbar. This applies to both the Top Toolbar in the Block Editor and the individual Block Toolbar.

### Blocks

![Blocks tab in the Preferences in WordPress Block Editor](../../assets/images/2021/07/preferences-blocks.jpg)

*Blocks tab in the Preferences in WordPress Block Editor*

**Block interactions**: This section helps to customize how you interact with blocks in the block inserter

-   **Show most used blocks**: When you toggle this option on, it enables a section in the Block Inserter that shows all the blocks that you use the most. This can be helpful to easily find the blocks that you use frequently to build your page or post content.

1.  You can search for blocks easily by typing in the name in the search box.
2.  You can check or uncheck the boxes to show or hide the blocks from the list.
3.  As you uncheck the blocks from the list, you will get a message at the top showing how many blocks have been hidden. If you want to undo these changes, just click the “**Reset**” button.

![Most Used blocks](../../assets/images/2022/10/Screen-Shot-2022-10-25-at-4.16.55-PM.png)

## Preferences in the Site Editor

This section covers preference settings when you are in the [Site Editor](../site-editor/README.md). There are fewer settings in the Site Editor but the options work similarly to the ones in the WordPress Block Editor Preferences.

### General

![General tab in the Preferences in Site Editor](../../assets/images/2023/10/SiteEditor_GeneralSettings.png)

### Blocks

![Blocks tab in the Preferences in Site Editor](../../assets/images/2022/10/Screen-Shot-2022-10-25-at-4.48.24-PM.png)

## Changelog

-   Updated 2025-11-25 (props @milana_cap)
    -   Update screenshots and videos for 6.8
    -   Add new “Show starter patterns” feature
-   Updated 2023-10-19
    -   Added content for New Feature “Reset”.
    -   Updated Screenshots with alt text.
-   Updated 2023-03-29
    -   Updated screenshots
    -   Replaced the “Reduce the interface” Block Editor preference with “Distraction free”.
-   Updated 2022-10-25
    -   Added screenshots and content update for 6.1
    -   Added content for Site Editor Preferences with screenshots
-   Created 2021-07-13
