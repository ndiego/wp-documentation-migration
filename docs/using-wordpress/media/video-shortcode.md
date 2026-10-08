---
title: Video shortcode
slug: video-shortcode
position: 10
original_url: https://wordpress.org/documentation/article/video-shortcode/
wp_id: 10840105
legacy_categories:
- support-guides
- dashboard
date: '2018-11-02T04:26:12'
modified: '2026-07-03T00:09:10'
migration:
  status: clean
  notes:
  - empty <pre> (shortcode rendered to nothing on the live site) filled with '[video]'; reconstructed, check against the original Codex page
  - live article shows a rendered media player inside a code example (content bug); converted back to the shortcode text. WordPress runs shortcodes inside <pre> too, so after import this needs [[video ...]] escaping or an importer filter, or the players come back
  counts:
    empty_pre_filled: 2
    internal_links_rewritten: 1
    rendered_shortcodes_restored_in_pre: 2
    version_links_kept_absolute: 1
---

# Video shortcode

The **Video** feature allows you to embed video files and play them back using a simple shortcode. This was added as of WordPress [Version 3.6](https://wordpress.org/documentation/wordpress-version/version-3-6/) and is used like this:

```
[video]
```

You can also use built in embeds and simply put the media file on its own line:

```
My cool content
http://my.movies.com/cool/movie/coolest.mp4
More cool content
```

## Usage

I have an old post that has an audio file in the Media Library attached to it, and I want to use the new shortcode:

```
[video]
```

Note: Do Not put Space between “[” and “video”.

I have the URL for an MP3, from the Media Library or external, that I want to play:

```
[video src="video-source.mp4"]
```

I have a source URL and fallbacks for other HTML5-supported filetypes:

```
[video mp4="source.mp4" webm="source.webm" ogv="source.ogv"]
```

## Options

The following basic options are supported:

`src`<br>
(string) (optional) The source of your video file. If not included it will auto-populate with the first video file attached to the post. You can use the following options to define specific filetypes, allowing for graceful fallbacks:

-   mp4, m4v, webm, ogv, wmv, flv

Default: First video file attached to the post

`poster`<br>
Defines image to show as placeholder before the media plays.<br>
Default: none

`loop`<br>
(string) Allows for the looping of media. Defaults to “off.”

-   “off” – (“default”) does not loop the media
-   “on” – media will loop to beginning when finished and automatically continue playing

Default: “off”

`autoplay`<br>
(string) Causes the media to automatically play as soon as the media file is ready. Defaults to “off.”

-   “off” – (“default”) does not automatically play the media
-   “on” – Media will play as soon as the media is ready

Default: “off”

`preload`<br>
(string) (optional) Specifies if and how the video should be loaded when the page loads. Defaults to “metadata.”

-   “metadata” – (“default”) only metadata should be loaded when the page loads
-   “none” – the video should not be loaded when the page loads
-   “auto” – the video should be loaded entirely when the page loads

Default: “metadata”

`height`<br>
(integer) (required) Defines height of the media. Value is automatically detected on file upload.<br>
Default: [Media file height]

`width`<br>
(integer) (required) Defines width of the media. Value is automatically detected on file upload.<br>
Default: [Media file width]

`muted`<br>
 (string) Mutes the video when it starts playing. This is particularly useful for autoplay videos.

-   “off” – (“default”) the video is not muted
-   “on” – the video will be muted
-   Default: “off”

## Related

WordPress Shortcodes: [audio](audio-shortcode.md), [caption](https://codex.wordpress.org/Caption_Shortcode), [embed](https://codex.wordpress.org/Embed_Shortcode), [gallery](https://codex.wordpress.org/Gallery_Shortcode), [playlist](https://codex.wordpress.org/Playlist_Shortcode)

#### Changelog

-   Updated 2026-07-03
    -   Added muted options. Props @karthickmurugan
-   Updated 2021-10-18
    -   Added changelog
    -   Corrected the links to the codex pages for the caption, embed, gallery and playlist shortcodes
