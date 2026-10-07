---
title: Administer your Blog
slug: administer-your-blog
original_url: https://wordpress.org/documentation/article/administer-your-blog/
wp_id: 10840078
categories:
- technical-guides
- maintenance
date: '2018-11-02T04:13:19'
modified: '2026-04-05T22:18:13'
migration:
  status: clean
  notes:
  - link to old slug 'writing-posts' rewritten to 'write-posts-classic-editor' (via 301)
  - link to old slug 'using-images' rewritten to 'use-images' (via 301)
  - link to old slug 'glossary' rewritten to 'wordpress-glossary' (via 301)
  - link to 'backing-up-your-database' points to moved page https://developer.wordpress.org/advanced-administration/security/backup/database/
  - link to old slug 'using-themes' rewritten to 'work-with-themes' (via 301)
  - link to 'optimization' points to moved page https://developer.wordpress.org/advanced-administration/performance/optimization/
  - link to old slug 'using-permalinks' rewritten to 'customize-permalinks' (via 301)
  - link to old slug 'managing-plugins' rewritten to 'manage-plugins' (via 301)
  counts:
    internal_links_rewritten: 36
    legacy_support_links_fixed: 36
    links_to_moved_external: 2
    relative_url_made_absolute: 39
---

# Administer your Blog

Generally, the daily tasks associated with administering your WordPress site are quick and easy to do, freeing you to concentrate on the content, editorials, and stories you want to share with the world, and allowing you to get back to other activities.

Here is a quick look at the various activities involved in administering your WordPress site. Some of these may need to be done daily, while others can be done weekly, monthly, or less frequently. It depends upon your blogging activity level and the intent of your WordPress site.

## Daily Tasks

### Login and Write

Most people begin by logging into their WordPress site because they have news, information, or a story to tell. So they head straight for the [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Posts](../../support-guides/dashboard/administration-screens.md#add-new-post) > [Add New](../../support-guides/publishing/write-posts-classic-editor.md). There, the title is set, the information is entered, categories and tags chosen, and any other minor details noted, and with a click is published.

If you have any new images, movies, or music, to upload to your site, you can easily do that when writing the post or switch to the [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Media](../../support-guides/dashboard/administration-screens.md#media-add-pictures-and-movies-to-your-posts) > [Add New Screen](../../support-guides/media/use-images.md) and add any other images to your WordPress site. Then, you can either add these to your new posts, or visit the [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Posts](../../support-guides/dashboard/administration-screens.md#add-new-post) > [Posts screen](../../support-guides/dashboard/posts-screen.md) and click Edit to edit the post in which you now wish to add an image. Again, click SAVE and it is released to the world.

Also, there are those [Drafts](../../support-guides/publishing/post-status.md#draft) sitting up at the top of the Write Post screen, which you can publish or move to the trash, if you’d like.

Luckily with WordPress, you have some options for dealing with all those posts. They don’t all have to be released today. Many people work ahead with their blog content, setting the dates into the future. When the day and time arrives, WordPress will automatically release the post, without any additional effort from you.

### Checking Comments

After you have cleaned up the content on your site, it is time to find out what they have been saying about what you say. On the [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Comments Screen](https://codex.wordpress.org/Comments_Screen), you can inspect the comments posted to your site. If a comment has been marked for [moderation approval](https://codex.wordpress.org/Comment_Moderation), it will look lighter colored than the rest of the comments. Click [Edit Comment](https://codex.wordpress.org/Manage_Comments_SubPanel#View_Mode) to access the comment and set it to be approved. Click **Delete Comment** if you want it removed.

The [Moderation Screen](https://codex.wordpress.org/Awaiting_Moderation_SubPanel) will segregate the comments awaiting moderation from the rest of the comments if you have set your [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Settings](../../support-guides/dashboard/administration-screens.md#settings-configuration-settings) > [Discussion](../../support-guides/dashboard/settings-discussion-screen.md) to moderate all comments. This allows for quick and easy comment moderation.

Determining which comments to keep and delete is a challenge. Be aware that often nice comments like *“I really like your site. Keep up the great work.”* and *“It shows you put a lot of time and effort in this. Thanks.”* might be benign comments, or more likely comment [spam](../../wordpress-overview/where-to-start/wordpress-glossary.md#spam). To help you determine and check on what might be comment spam, and how to increase your protection against comment spammers, check out the following documents:

-   [Introduction to Dealing with Comment Spam](https://codex.wordpress.org/Comment_Spam)
-   [Moderating Comments](https://codex.wordpress.org/Comment_Moderation)
-   [Combating Comment Spam](https://codex.wordpress.org/Combating_Comment_Spam)
-   [Denying Access to Comment Spammers with .htaccess](https://codex.wordpress.org/Combating_Comment_Spam/Denying_Access)

### Users and Authors

If you have set your site set up to [allow users to register](https://codex.wordpress.org/Registered_User_Features) and submit articles, stop by your [Users Screen](../../support-guides/dashboard/administration-screens.md#users-your-blogging-family) to check on those who have registered and make any adjustments to their [User Roles and Capabilities](../../support-guides/dashboard/roles-and-capabilities.md) as needed.

If you do allow users to post articles, be sure to check the [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Posts](../../support-guides/dashboard/administration-screens.md#add-new-post) > [Posts screen](../../support-guides/dashboard/posts-screen.md) for any newly posted articles in the **Drafts** or **Pending** status awaiting your review and release.

### Check the Dashboard

At this point, your daily tasks are almost complete. Your site is up-to-date and on its way to entertaining and educating the world. But, there is one last task you might want to check. Stop by your WordPress [Administration Screens](../../support-guides/dashboard/administration-screens.md) > [Dashboard](../../support-guides/dashboard/administration-screens.md#dashboard-information-central) > [Dashboard](../../support-guides/dashboard/dashboard-screen.md) screen and check to see if there are any new activities going on in the WordPress Community, especially any announcements about upgrades.

While there, take advantage of your handy “To Do List” featured on the Dashboard. This lists your most recently released posts, the next batch of scheduled entries, recent comments, blog stats, and incoming links (referrers). This helpful information lets you know what has been released to the public from your site, what is next on the list, and shows you, at a glance, to view the most recent comments.

The blog stats and incoming links give you different information. The Stats give you information about how many posts, comments, and categories are on your site. While this may not be critical information, you can use it as a general scoreboard or counter. The incoming links information tells you who has [pinged](../../wordpress-overview/where-to-start/wordpress-glossary.md#pingback) or [trackbacked](../../wordpress-overview/where-to-start/wordpress-glossary.md#trackback) your site. This helps your link popularity for your site and gives you an idea of who thought your site’s material was worthy of praise.

At the bottom of the page, you will see a list of your Drafts, waiting to be done.

## Administration Tasks

As the administrator or site owner, there are a few more tasks you should add to your schedule. These do not have to be done daily, but they still need to be done on a regular basis. Many of these are outlined in the articles [WordPress Housekeeping](https://codex.wordpress.org/WordPress_Housekeeping) and [WordPress Site Maintenance](https://codex.wordpress.org/WordPress_Site_Maintenance). In general they are:

-   [Updating WordPress](updating-wordpress.md)
-   Check for Dead Links Throughout Your Site
-   [Check in with WordPress for Changes and Information](https://www.wordpress.org/)
-   [Backup Your WordPress Site and Database](https://developer.wordpress.org/advanced-administration/security/backup/database/)
-   [Update Your Site’s Content and/or Look](../../customization/appearance/work-with-themes.md)
-   Update [Plugins](https://wordpress.org/plugins/managing-plugins/) and [Themes](../../customization/appearance/work-with-themes.md)
-   [Check for Validation Errors](https://codex.wordpress.org/Validating_a_Website)
-   [Optimize Your WordPress Site](https://developer.wordpress.org/advanced-administration/performance/optimization/)

## More Administration Resources

-   [Administration Screens](../../support-guides/dashboard/administration-screens.md)
-   [What Registered Users Can Do](https://codex.wordpress.org/Registered_User_Features)
-   [Manage Categories](../../support-guides/dashboard/administration-screens.md#categories)
-   [Roles and Capabilities](../../support-guides/dashboard/roles-and-capabilities.md)
-   [Manage WordPress Settings](../../support-guides/dashboard/administration-screens.md#settings-configuration-settings)
-   [Manage Discussion Options](../../support-guides/dashboard/settings-discussion-screen.md)
-   [Using Permalinks](../../support-guides/publishing/customize-permalinks.md)
-   [Moderate Comments](https://codex.wordpress.org/Comment_Moderation)
-   [Manage Plugins](../../customization/appearance/manage-plugins.md)
-   [Manage Themes](../../customization/appearance/work-with-themes.md)
