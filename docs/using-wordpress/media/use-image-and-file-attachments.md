---
title: Use image and file attachments
slug: use-image-and-file-attachments
position: 8
original_url: https://wordpress.org/documentation/article/use-image-and-file-attachments/
wp_id: 11263208
legacy_categories:
- support-guides
- media
date: '2019-03-01T13:16:40'
modified: '2023-04-14T12:20:02'
migration:
  status: clean
  counts:
    internal_links_rewritten: 14
---

# Use image and file attachments

In WordPress you can upload, store, and display a variety of file types (media). The most common file types are image, video and audio files, but other file types such as document files, spreadsheet files, and code samples (amongst others) can also be managed within WordPress.

Media can be uploaded via the [Media Add New Screen](../administration-screens/media-screens/media-add-new-screen.md) or [Media Library Screen](../administration-screens/media-screens/media-library-screen.md) in the admin area, or via quick links on the edit screen.

In order to upload media, you may need to ensure that the correct [file permissions](https://developer.wordpress.org/advanced-administration/server/file-permissions/) are set for the wp-content directory in your WordPress installation.

## Edit Screen Links

By default, above the post editing area is a link to Upload/Insert media in to the post.

## Attachment to a Post

If a media file is uploaded within the edit screen, it will automatically be attached to the current post being edited. If it is uploaded via the <br>
 [Media Add New Screen](../administration-screens/media-screens/media-add-new-screen.md) or [Media Library Screen](../administration-screens/media-screens/media-library-screen.md) it will be unattached, but may become attached to a post when it is inserted into post. There also is an option on the [Media Library Screen](../administration-screens/media-screens/media-library-screen.md) to attach unattached media items.

Note that media items are also ‘Posts’ in their own right and can be displayed as such via the WordPress [Template Hierarchy](https://developer.wordpress.org/themes/basics/template-hierarchy/). Themes can make use of this to loop over media items or create galleries.

If the parent post of an attached media item is deleted, the media item will become attached to the deleted post’s parent if it exists or if it doesn’t exist, the media item will become unattached and is open for re-attachment to another post.

## Inserting in a Post

Once a media file has been uploaded, it may be [inserted in to a post](inserting-images-into-posts-and-pages-block-editor.md).

When the media file is inserted you can choose to:

-   Link directly to the media file
-   Link to the attachment post, in which case the file will be served via the WordPress [Template Hierarchy](https://developer.wordpress.org/themes/basics/template-hierarchy/)
-   Not link to the media file (e.g. in the case of images, the image file will still be embedded in the page, but not linked to allow the browser to display the image file by itself)

## Usage in Themes

Themes may use various template tags to display post attachments or utilize the [attachment.php](https://developer.wordpress.org/themes/basics/template-hierarchy/) file to customize the display of attachments. A [shortcode](https://developer.wordpress.org/themes/functionality/media/galleries/#gallery-shortcode) tag is also available to display a gallery of images attached to a post.

## Further reading

-   [Use Images](use-images.md)
-   [Image Size and Quality](image-size-and-quality.md)
-   [Settings Media Screen](../administration-screens/settings/settings-media-screen.md)
-   [Media library screen](../administration-screens/media-screens/media-library-screen.md)
-   [Media Add New Screen](../administration-screens/media-screens/media-add-new-screen.md)
-   [Edit Media](edit-media.md)
-   [Inserting Images into Posts and Pages (Block Editor)](inserting-images-into-posts-and-pages-block-editor.md)
-   [Inserting Images into Posts and Pages (Classic Editor)](inserting-images-into-posts-and-pages-classic.md)
