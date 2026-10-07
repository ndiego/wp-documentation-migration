---
title: Colors Settings overview
slug: colors-settings-overview
original_url: https://wordpress.org/documentation/article/colors-settings-overview/
wp_id: 16075254
categories:
- customization
- block-editor
date: '2022-11-02T07:22:09'
modified: '2026-09-06T17:23:56'
migration:
  status: warnings
  warnings:
  - contained VideoPress embed (now a bare oEmbed URL; verify it auto-embeds after import)
  notes:
  - link to old slug 'blocks' rewritten to 'blocks-list' (via 301)
  videos:
  - type: videopress
    guid: m3lpI36x
    url: https://videopress.com/v/m3lpI36x
    original: https://videos.files.wordpress.com/m3lpI36x/elements-panel.mov
    poster: https://videos.files.wordpress.com/m3lpI36x/elements-panel_mov_vp9_1440p.original.jpg
    media_id: 16370535
  - type: videopress
    guid: 4O9MDUID
    url: https://videopress.com/v/4O9MDUID
    original: https://videos.files.wordpress.com/4O9MDUID/gradient-background.mov
    poster: https://videos.files.wordpress.com/4O9MDUID/gradient-background_mov_vp9_1440p.original.jpg
    media_id: 16370543
  - type: videopress
    guid: 0885znCX
    url: https://videopress.com/v/0885znCX
    original: https://videos.files.wordpress.com/0885znCX/duotone.mov
    poster: https://videos.files.wordpress.com/0885znCX/duotone_mov_vp9_1440p.original.jpg
    media_id: 16370549
  counts:
    images: 11
    internal_links_rewritten: 5
    videopress: 3
---

# Colors Settings overview

You can use the color settings in your [block](blocks-list.md) to set the text color, background color, link color, gradient options, and duotone filters for your content. They are designed to make it as simple as possible to update your block’s colors.

The color settings available will vary based on the theme and the block in use.

## How to access color settings

Colors can be set on a site basis or on a block basis. Setting color on a site basis will affect the color of the entire site.

### How to access color settings for your site

1.  From your Administration Screens, Select Appearance > Editor
2.  Select Styles
3.  Select Colors

### How to access color settings for a single block

Select the block you want to modify the color and open the **Block Settings sidebar** of a by clicking the **Settings** icon that is next to the **Publish/Save** button.

![Block settings icon](../../assets/images/2022/11/block-settings-7-0-1.png)

Find the Color options under these three locations:

1.  [Typography settings](typography-settings-overview.md) to change text color
2.  [Background settings](background-settings-overview.md) to change background colors and gradients
3.  [Elements color settings](#elements-panel-for-nested-elements) to change colors for child elements inside blocks like the Group block

![Three color locations in the paragraph block settings toolbar, Typography, Background, and Elements](../../assets/images/2022/11/color-locations.png)

### Elements panel for nested elements

WordPress 7.1 introduced the Elements panel where you can customize colors for links and nested items within container blocks like the Group block.

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/m3lpI36x -->

https://videopress.com/v/m3lpI36x

## Type of settings

Each supported block comes with different color settings.

### Text and Background color

This option allows you to change the color of the text, and background on the block you are working on. Color settings vary depending on which theme you are using.

![Background color palette](../../assets/images/2022/11/Screenshot-2026-09-06-at-11.59.37-AM.png)

Accessibility tests are built into the editor to warn you when the text may become hard to read against the background color choices as shown.

![Accessibility warning on text color](../../assets/images/2022/11/Screenshot-2026-09-06-at-12.02.22-PM.png)

### Add a custom color

To add a custom color, click on the color box above the color palette options. It may read “no color selected” if your block is using the default color.

Next, you can paste in a color HEX code or named color value such as black, darkblue, or deeppink.

![Typography panel showing no color selected](../../assets/images/2022/11/Screenshot-2026-09-06-at-11.51.07-AM.png)

*No color selected for text*

![Typography panel showing a custom color of #DE0278](../../assets/images/2022/11/Screenshot-2026-09-06-at-11.51.23-AM.png)

*Custom color added for text*

### Gradient background colors

Some blocks such as the [Heading block](../text-blocks/heading-block.md) allow you to set either a solid color or a gradient as the background. A gradient is a mix of two or more colors, displayed using a certain pattern (from lighter to darker, or one color blending into the other).

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/4O9MDUID -->

https://videopress.com/v/4O9MDUID

A slider will appear that shows the two color points that make up the gradient.

![Color points in the gradient](../../assets/images/2026/09/image-2-edited.png)

You can click on any of the two color points to display the color picker for changing the color value. You can either choose a color from the color picker or enter the HEX, RGB, or HSL color values.

You can add additional color points if you like by clicking the **+** icon that appears when you hover over the gradient slider.

You can choose between the **Linear** or **Radial** gradient type. The angle control shifts the position of the gradient.

The **Linear** type creates a gradient between the two colors along a straight line, whereas the **Radial** type starts from the center and moves to the borders.

![Liner and Radial gradient options](../../assets/images/2022/10/gradient-example.png)

### Duotone filter

![Duotone filter in block editor](../../assets/images/2022/11/Duotone-Filter.png)

*Duotone filter active on image block using Twenty Twenty Four theme*

You can create a two-tone color effect (called the duotone effect) on images without actually changing the original image

The duotone filter option allows you to add this filter color to your block content from the block toolbar. The filter can be black, white, or *any* other color combination of your choosing. The duotone effect works best on high-contrast images.

To get started, select the Duotone filter icon in the block toolbar. You can pick the two colors for the effect from the list of duotone presets provided in the drop-down.

You can also pick your own colors for the shadows and highlights by clicking on the **Shadows** /**Highlights** option which opens up the color picker and then selecting your custom color from the color palette.

If you want to remove the duotone filter you can click the **Clear** button found at the bottom-right of the color palette or by removing clearing the **Filters** option in the **Block Settings** sidebar.

<!-- VideoPress embed (iframe removed): https://videopress.com/embed/0885znCX -->

https://videopress.com/v/0885znCX

## Reset settings

When hovering over the Typography or Background Color options, if a color has been selected, a reset button (displayed as a dash icon) will appear. There is also a Clear button on the color palette selection.

![Highlighted options of how to reset to the default color](../../assets/images/2022/11/Screenshot-2026-09-06-at-12.19.57-PM-1.png)

Choosing these options will remove the applied color and reset the field to its default state, indicating “No color selected.”

![No color selected shown in typography color palette](../../assets/images/2022/11/Screenshot-2026-09-06-at-12.22.37-PM.png)

*No color selected indicates that the default theme color is used.*

## Changelog

-   Updated 2026-09-06 (props @awetz583)
    -   Updated screenshots and descriptions for 7.1
-   Updated 2026-06-19
    -   Updated first three videos for 7.0 (props @awetz583 @moltilearn8)
-   Updated 2026-05-23
    -   Added custom color section
-   Updated 2025-05-04
    -   Add site’s color settings.
    -   Update screenshots and videos.
-   Update 2025-04-22 (props to [@nikunj8866](https://profiles.wordpress.org/nikunj8866/))
    -   Add color reset button.
-   Created 2022-11-01
