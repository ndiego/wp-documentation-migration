---
title: Kitchen sink (frontmatter title)
---

# Kitchen sink with `code` and [a link](https://example.com) in the H1

First paragraph, used as the excerpt. It has **bold**, _em_, `code`, an emoji 🎉 ✅, entities &amp; &lt;tag&gt; &copy; &nbsp;x, and a smart quote ’.

## Heading with explicit id {#custom-id}

### Heading with <a id="html-anchor"></a>inline anchor

Jump to [the custom id](#custom-id), [html anchor](#html-anchor), [auto slug](#nested-lists-and-code).

## Nested lists and code

1. Step one
    - nested bullet (4 spaces)
    - another
        1. deeply nested ordered
2. Step two

   ```php
   <?php echo 'fenced inside a list item'; ?>
   ```

3. Step three

- item
  - nested bullet (2 spaces)

```js
const x = 1 < 2 && 3 > 2; // <script>alert(1)</script>
```

~~~
tilde fence
~~~

    indented code block

## Callouts

> [!NOTE]
> GitHub-style alert. **Bold** inside.

> [!WARNING]
> Second alert.

> Plain blockquote.

## Links

- [sibling](sibling-page.md)
- [sibling with anchor](sibling-page.md#section)
- [parent readme](../README.md)
- [folder readme](./README.md)
- [up two](../../overview/where-to-start/get-started-with-wordpress.md)
- [root-relative](/docs/overview/README.md)
- <https://autolink.example.com>
- bare URL https://bare.example.com/path in text

## Images

![relative image](../assets/images/2023/01/example.png)

![deep relative](../../assets/images/example.png "with title")

<img src="../assets/images/raw-html.png" alt="raw html img" width="300" class="aligncenter" style="border:1px solid red" />

## Raw HTML

<details>
<summary>Click to expand</summary>

Inside details with **markdown**.

</details>

<video controls muted playsinline poster="../assets/poster.png" width="640">
  <source src="https://example.com/video.mp4" type="video/mp4">
</video>

<video src="https://example.com/v2.mp4" controls autoplay loop></video>

<iframe src="https://www.youtube.com/embed/abc" width="560" height="315" allowfullscreen></iframe>

<div class="callout callout-tip" style="color:red" data-foo="bar" onclick="alert(1)">Div with class/style/data/onclick</div>

<span class="dashicons dashicons-admin-generic"></span> dashicon span

<kbd>Ctrl</kbd> + <kbd>S</kbd>

<script>alert('x')</script>

<style>.x{color:red}</style>

<form><input type="text" name="q"></form>

<!-- an HTML comment that should not be visible -->

<!-- wp:paragraph {"className":"is-style-foo"} -->
<p class="is-style-foo">A paragraph written as block markup.</p>
<!-- /wp:paragraph -->

<!-- wp:image {"id":1} -->
<figure class="wp-block-image"><img src="https://example.com/a.png" alt=""/><figcaption>Caption</figcaption></figure>
<!-- /wp:image -->

## Tables

| Shortcut | Action |
|---|:--|
| <kbd>Ctrl</kbd>+<kbd>B</kbd> | Bold \| pipe |
| `code` | [link](sibling-page.md) |

## Shortcodes and embeds

[gallery ids="1,2,3"]

https://www.youtube.com/watch?v=dQw4w9WgXcQ

Line one  
Line two after two-space hard break<br>after br.

Footnote ref[^1].

[^1]: The footnote.

Setext H1
=========

# A second H1 later on
