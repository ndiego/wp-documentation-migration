---
title: Use keyboard shortcuts (Classic Editor)
slug: keyboard-shortcuts-classic-editor
position: 7
original_url: https://wordpress.org/documentation/article/keyboard-shortcuts-classic-editor/
wp_id: 10840095
legacy_categories:
- support-guides
- dashboard
date: '2018-11-02T04:17:26'
modified: '2023-01-13T12:36:53'
migration:
  status: clean
  notes:
  - link to old slug 'block-editor-keyboard-shortcuts' rewritten to 'keyboard-shortcuts-block-editor' (via 301)
  counts:
    internal_links_rewritten: 5
    legacy_support_links_fixed: 4
    relative_url_made_absolute: 4
---

# Use keyboard shortcuts (Classic Editor)

## Editor Shortcuts

-   **Note: This page lists keyboard Shortcuts for the Classic editor.**
-   **For the Block Editor, [the list of Keyboard Shortcuts is here](keyboard-shortcuts-block-editor.md)**

In the WordPress visual editor you can use a combination of keys to do things that normally need a mouse, trackpad or other input device. Rather than reaching for your mouse to click on the toolbar, you can use the following keyboard shortcuts:

Windows and Linux use “Ctrl + letter”, Mac uses “Command (⌘) + letter”.

### Ctrl + key

```
Letter Action
c ... Copy
v ... Paste
a ... Select all
x ... Cut
z ... Undo
y ... Redo
b ... Bold
i ... Italic
u ... Underline
k ... Insert/edit link
```

### Alt + Shift + key

The following shortcuts use a different key combination: Windows/Linux: “Alt + Shift (⇧) + letter”. Mac: “Ctrl + Option (alt ⌥) + letter”. (Macs running any WordPress version below 4.2 use “Alt + Shift (⇧) + letter”).

```
Letter Action
n ... Check Spelling (This requires a plugin.)
l ... Align Left
j ... Justify Text
c ... Align Center
d ... Strikethrough
r ... Align Right
u ... • List
a ... Insert link
o ... 1. List
s ... Remove link
q ... Quote
m ... Insert Image
w ... Distraction Free Writing mode
t ... Insert More Tag
p ... Insert Page Break tag
h ... Help
x ... Add/remove code tag
1 ... Heading 1
2 ... Heading 2
3 ... Heading 3
4 ... Heading 4
5 ... Heading 5
6 ... Heading 6
9 ... Address
```

### Formatting Shortcuts

Formatting Shortcuts while using visual editor (Since [Version 4.3](<https://codex.wordpress.org/Version%204.3>))

```
Letter . Action
* ...... Start an unordered list
- ...... Start an unordered list
1. ..... Start an ordered list
1) ..... Start an ordered list
## ..... H2
### .... H3
#### ... H4
##### .. H5
###### . H6
> ...... transform text into blockquote
--- .... horizontal line
`..` ... transform text into code block
```

## Keyboard Shortcuts for Comments

Beginning with [WordPress Version 2.7](<https://codex.wordpress.org/Version%202.7>), the ability to use keyboard shortcuts to browse and moderate comments was introduced. These keyboard shortcuts are designed to save time by allowing you to rapidly navigate and perform actions on comments. If your blog gets a large number of comments, you will find these shortcuts especially useful.

### Activating Keyboard Shortcuts

Keyboard shortcuts are enabled on a per-user setting, and can be turned on by visiting the Profile panel in [Administration Screens](../../using-wordpress/administration-screens/README.md) > [Users](../../using-wordpress/administration-screens/README.md#your-profile) > [Your Profile](../../using-wordpress/administration-screens/users/users-your-profile-screen.md). Check the [Keyboard Shortcuts](../../using-wordpress/administration-screens/users/users-your-profile-screen.md#your-profile-and-personal-options) checkbox to enable keyboard shortcuts for comment moderation.

Please note, the keyboard shortcuts are designed to use both hands, simultaneously, on a QWERTY style keyboard layout.

### The Meaning of Selected

The keyboard shortcuts are used for navigation and for actions. For any action to affect a comment, that comment must be first **selected**. The comment that is considered **selected** is indicated with a light-blue background. By default, no comment is selected, so, you will need to press either the letter **j** key, or letter **k** key, to start navigating.

### Using Keyboard Shortcuts to Navigate Comments

Navigating comments is accomplished with the **j** and **k** keys. When you first visit the Comments page, no comments is selected, so, first press the letter **j**, or the letter **k**, to select the first comment. After that, just press the letter **j** to move the select to the next comment.

-   Pressing **j** moves the current selection (light-blue background) down.
-   Pressing **k** moves the current selection (light-blue background) up.

Note that if you come to the bottom of a page of comments and press **j** again, you will be taken to the next page and the first comment of that next page will be selected. Likewise, pressing **k** at the top of a comment page will zoom you to the previous page, selecting the comment at the bottom of that previous page. This makes it very easy to navigate through a long list of comments to perform the necessary actions.

### Using Keyboard Shortcuts to Perform Actions on Comments

For one of these actions to affect a comment, make sure the comment is first selected (see above).

-   Pressing **a** approves the currently selected comment.
-   Pressing **s** marks the current comment as spam.
-   Pressing **d** moves the comment to the trash (WordPress 2.9) or deletes the current comment.
-   Pressing **z** restores the current comment from the trash or activates the Undo when that row is selected.
-   Pressing **u** unapproves the currently selected comment, placing it back into moderation.
-   Pressing **r** initiates an inline reply to the current comment (you can press **Esc** to cancel the reply).
-   Pressing **q** activates “Quick Edit” which allows for rapid inline editing of the current comment.
-   Pressing **e** navigates to the edit screen for the current comment.

### Bulk Actions

You can also perform an action on multiple comments at once. First, you’ll need to select the comments for the bulk action, using the **x** key to check the checkbox for the currently selected comment. **Shift-x** can be used to toggle the checkboxes, inverting their state. Once you have some comments checked:

-   Pressing **Shift-a** approves the checked comments.
-   Pressing **Shift-s** marks the checked comments as spam.
-   Pressing **Shift-d** deletes the checked comments.
-   Pressing **Shift-u** unapproves the checked comments.
-   Pressing **Shift-t** moves the checked comments to the Trash.
-   Pressing **Shift-z** restores the checked comments from the Trash.
