---
title: Understanding comment spam
slug: understand-comment-spam
position: 3
original_url: https://wordpress.org/documentation/article/understand-comment-spam/
wp_id: 11263506
legacy_categories:
- support-guides
- publishing
date: '2019-03-01T14:23:40'
modified: '2026-05-07T00:24:15'
migration:
  status: clean
  notes:
  - contained <details> (emitted as raw HTML details/summary)
  counts:
    internal_links_rewritten: 2
---

# Understanding comment spam

If you’ve spent any time online, you’ve probably come across spam in one form or another. In general, spam is unwanted content posted for promotional, misleading, or abusive purposes.

The same thing can happen in your site’s comment section. Comment spam often shows up as irrelevant messages, suspicious links, repeated keywords, or generic comments posted just to promote another site, product, or service.

Some spam comments are posted manually, but many are generated automatically by bots. Either way, they can clutter your site, disrupt discussion, and create extra work for site owners and administrators.

## Fighting comment spam

WordPress includes several built-in settings that can help you reduce or manage comment spam.

### Moderate comments before they appear

Comment moderation is one of the simplest and most effective ways to deal with spam. When moderation is enabled, comments won’t appear on your site until an administrator approves them.

You can manage this in **Settings > Discussion**.

### Require commenters to provide details

You can make commenting a little harder for spammers by requiring people to enter a name and email address, or by requiring them to be registered and logged in before they can comment.

These settings can help reduce some automated spam, although they may not stop every spammer.

### Limit the number of links allowed

Because many spam comments include links, WordPress lets you hold comments for moderation if they contain more than a set number of links.

This can be useful for catching spam, but keep in mind that it may also affect legitimate comments that include multiple links.

### Add words or terms to moderation lists

You can add words, IP addresses, email addresses, names, or other terms to your moderation or disallowed comment key lists. Comments containing those items can then be held for review or blocked automatically.

### Disable comments where they are not needed

If a page or post does not need comments, you may decide to turn comments off completely. This can be a simple way to avoid spam on content where discussion is not important.<br>
<br>
If you want more detailed guidance, see [Comments in WordPress](comments-in-wordpress.md) and [Comment Moderation](comment-moderation.md).

## FAQ

<details>
<summary>Why are they spamming me?</summary>
<p>Usually, they are not targeting your site personally. Most comment spam is posted in bulk across many websites. The goal is often to place links in as many places as possible.</p>
</details>

<details>
<summary>Where can I find WordPress anti-spam plugins?</summary>
<p><a href="https://wordpress.org/plugins/tags/anti-spam">Plugins for handling comment spam</a> can be found in the <a href="https://wordpress.org/plugins/">Official WordPress Plugin Directory</a>.</p>
</details>

<details>
<summary>Which is the best plugin?</summary>
<p>There is no single answer to that. Spammers use different tactics, and plugins respond in different ways. A plugin that works well for one site may not be the best fit for another.</p>
<p>A good place to start is by looking at how recently the plugin has been updated, whether it is compatible with your version of WordPress, and whether the author offers clear documentation or support.</p>
</details>

<details>
<summary>I have a problem with a plugin</summary>
<p>First, check the plugin’s documentation or support page. You can also search its support forum to see whether the issue has already been reported or solved.</p>
</details>

<details>
<summary>What happens to comments that are marked as “Spam”?</summary>
<p>That depends on the tools and plugins you use. In many cases, spam comments are kept for a period of time before being deleted, which gives you a chance to review them.</p>
</details>

<details>
<summary>I have spam appearing as soon as I publish a post</summary>
<p>This can happen if comments are open and your site is being targeted by bots or spammers. Make sure WordPress and your plugins are up to date, review your discussion settings, and consider using moderation or an anti-spam plugin.</p>
</details>

<details>
<summary>Why is every comment going into the moderation queue?</summary>
<p>This is often caused by your discussion settings. For example:</p>
<ul>
<li>Comment moderation may be enabled for all comments</li>
<li>The comment may contain more links than your allowed limit</li>
<li>The comment may include words or phrases from your moderation list</li>
</ul>
<p>Check <strong>Settings &gt; Discussion</strong> to review the rules currently applied to comments.</p>
</details>

<details>
<summary>I have disabled comments, but comments continue to be posted</summary>
<p>Disabling comments in <strong>Settings &gt; Discussion</strong> usually applies only to future content. Older posts or pages may still have comments enabled unless you update them individually.<br/><br/>To completely disable comments, you will have to edit each past post and uncheck <strong>Allow Comments</strong>. Alternatively, you could delete the wp-comments-post.php file, or run this MySQL query, from the command line on a shell account, or using <a href="https://codex.wordpress.org/phpMyAdmin">phpMyAdmin</a>: <code>UPDATE wp_posts SET comment_status="closed";</code></p>
</details>

<details>
<summary>I have disabled trackbacks, but trackbacks continue to be posted</summary>
<p>If you have unchecked <strong>Allow link notifications from other Weblogs (pingbacks and trackbacks.)</strong> on the Options &gt; Discussion panel, then you have only disabled trackbacks on <em>future posts</em>. To completely disable trackbacks, you will have to edit each past post and uncheck <strong>Allow Pings</strong> from the Write Post SubPanel. Alternatively, you could just simply delete the wp-trackback.php file, or run this MySQL query, from the command line on a shell account, or using PHPMyAdmin: <code>UPDATE wp_posts SET ping_status="closed";</code></p>
</details>
