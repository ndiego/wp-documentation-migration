---
title: More rich text editing options
slug: more-text-editing-overview
position: 7
original_url: https://wordpress.org/documentation/article/more-text-editing-overview/
wp_id: 16356477
legacy_categories:
- customization
- block-editor
date: '2023-05-23T15:32:12'
modified: '2025-12-01T04:13:10'
migration:
  status: warnings
  warnings:
  - 'external images hotlinked from user-images.githubusercontent.com: 1 (see assets/images-manifest.json)'
  counts:
    callouts: 1
    callouts_info: 1
    image_self_links_removed: 1
    images: 11
    images_missing_alt: 2
    internal_links_rewritten: 2
---

# More rich text editing options

The **More options** menu in the Rich Text toolbar gives you additional options to customize your text. You can access these additional options by clicking on the **arrow** icon in the toolbar.

![](../../../assets/images/2023/05/Rich-text-options-1.png)

_Block toolbar with the drop-down for **More rich text options**_

## Footnote

The *Footnote* option will insert notes in your text. These notes will link to a new block that will be added at the bottom of your page. You will able to add the content of your notes in that new block and links will be added automatically.

> [!NOTE]
> Read more about the Footnotes block [here](../blocks/text/footnotes-block.md).

![](../../../assets/images/2023/08/footnote-block.png)

## Highlight

Using the *highlight* option allows you to change the color of the selected text and its background.

![The Highlight option opens a new modal with two tabs: One for text color and one for background. Each tab has a color picker and a color palette to choose from. Below the palette there is a button for clearing the color selection.](../../../assets/images/2022/05/paragraph-block-highlights-1.jpg)

## Inline code

Use the *inline code* feature to format code snippets within your text differently. The *inline code* formatting also prevents the code to be executed instead of displayed.

![The inline code option changes the font family of the text and adds a light grey background color to distinguish it from other text content.](../../../assets/images/2020/04/Screen-Shot-2020-04-18-at-7.11.38-PM.png)

## Inline image

The *inline image* feature allows you to add an image from your media library to your text. It has an option to enter the desired pixel width for your image.

![When you select the inline image in a Rich Text, the editor opens a modal with an option to enter the image width.](../../../assets/images/2020/08/paragraph_10.png)

## Keyboard input

Using the *keyboard Input* option allows you to add the `<kbd>` tag to selected text.

![The keyboard input option changes the font family of the text to distinguish it from other text content.](../../../assets/images/2023/08/keyboard-input.png)

## Language

User the *Language* option to specify the language for the selected text. You will need to the languages abbreviation (es, en, fr, de) and specify the text direction (Left to Right or Right to Left).

![Language option settings: Language & Text Direction](../../../assets/images/2023/08/rich-text-language.png)

## Strikethrough

Using the *strikethrough* option adds a line through the selected text.

![The strikethrough option adds a horizontal line across the selected text.](../../../assets/images/2020/08/paragraph_9-1.png)

## Subscript

The *subscript* option allows you to add subscript to the selected text.

![The subscript option changes the position of the selected text so that it is positioned lower than other text content.](../../../assets/images/2020/08/paragraph_8.png)

## Superscript

The *superscript* option allows you to add superscript to the selected text.

![The superscript option changes the position of the selected text so that it is above other text content.](../../../assets/images/2020/08/paragraph_9.png)

## Clear unknown formatting

In certain situations, you may come across an option in the block toolbar to *Clear unknown formatting*. This option will only appear if WordPress detects unrecognized formatting in a block. Choosing the *Clear unknown formatting* option will remove any unrecognized code that is affecting your content. That said, It is not necessary to clear the unknown formatting in order to apply other rich text editing.

For example, the *Clear unknown formatting* option might appear when you have copied and pasted content from a document editor such as Google Docs or Microsoft Word, or if you have used the *Edit as HTML* option in the [More options](more-options.md) menu.

![the user is mousing over the Clear Unknown Formatting option in the block toolbar. The text that is selected says 'This text was copied in to WordPress from another location and has some unusual formatting applied.' and it is italicised.](../../../assets/images/external/user-images.githubusercontent.com/e2a843066b-240368109-1c4594a5-6418-45f2-b800-75e96843636a.png)

## Changelog

-   Updated 2023-08-08
    -   Added Footnotes & Languages
    -   Updated Screenshots
-   Updated 2023-06-08 with additional section for the new *Clear unknown formatting* option and added Changelog.
-   Created 2023-05-23
