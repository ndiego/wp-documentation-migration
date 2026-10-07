---
title: 'Get a faster, more secure website: update your PHP today'
slug: update-php
original_url: https://wordpress.org/documentation/update-php/
wp_id: 9948338
date: '2018-02-08T09:13:28'
modified: '2018-02-08T09:13:28'
migration:
  status: clean
  notes:
  - live page uses theme template page-update-php.php (chrome-less page)
  counts:
    edge_br_removed: 20
---

# Get a faster, more secure website: update your PHP today

**Your WordPress site can be faster, and more secure, and you can make this happen!**

This page will explain why this matters to you, and then how you can fix it.

## Why PHP Matters To You

PHP is the coding language WordPress is built on, and its version is set at the server-level by your hosting company. Whilst you may be familiar with the importance of [keeping WordPress, and your themes and plugins up-to-date](https://codex.wordpress.org/Dashboard_Updates_Screen), keeping PHP up-to-date is just as important.

There are two main benefits to keeping PHP up-to-date:

-   **Your website will be faster** as the latest version of PHP is more efficient. Updating to the latest supported version (7.4 or more) can deliver a huge performance increase; up to 3 or 4x faster for older versions.
-   **Your website will be more secure**. PHP, like WordPress, is maintained by its community. Because PHP is so popular, it is a target for hackers – but the latest version will have the latest security features. Older versions of PHP *do not have this*, so updating is essential to keep your WordPress site secure.

And then there are a number of secondary benefits:

-   **A faster WordPress website will be rewarded by search engines**, so you’ll rank higher in search!
-   **A faster website will retain visitors better** (they’ll leave if it takes too long to load), making your website more effective.
-   **A more secure website is better protected against hackers**, and the cost and reputational damage associated with a hacked website.

These benefits are good for you, and good for your website’s visitors. These are the reasons you should update PHP today. The next section will show you how to do this.

## Before you update your PHP version

This section starts off with some warnings, but don’t be afraid! As with most things technical, we just need to cover some background before we can get to the part where you update your PHP version.

Updating your PHP version should not be a problem, but we can’t *guarantee* that it’s not. WordPress itself will work with PHP versions as far back as 5.6 (we’re recommending version 7.4 or more at the time of writing, so this is *great* backward compatibility!), but we don’t know if your themes or plugins will work. They should, and popular or reputable ones almost certainly will be, but we can’t guarantee it.

There are a couple of steps you should take to mitigate any risk before proceeding:

1.  **Make a backup of your website:** a backup will let you revert your site to how it is right now in the event anything goes wrong. There are [plenty of free backup plugins available](https://wordpress.org/plugins/search/backup/), so if you don’t have a backup solution already – use one of these. In order to revert this backup, you’ll also need your web host to move your PHP version back to your current version (we’ll cover how to do this later).
2.  **Update WordPress, themes, and plugins:** from your WordPress Dashboard, head to Updates, and then update all. You should do this regularly anyway 🙂 When done, check your site is working as expected.
3.  **Check PHP compatibility:** install the [PHP Compatibility Checker plugin](https://wordpress.org/plugins/php-compatibility-checker/) to check your themes and plugins for possible issues. This plugin isn’t perfect and may miss items or flag false positives, but it does work in most cases.
4.  **Fix any PHP compatibility issues:** if the PHP Compatibility Checker plugin picks up any issues, get in touch with the theme or plugin developer and ask them to investigate. If they can’t or won’t get back to you, have a look for themes or plugins on [WordPress.org](https://wordpress.org/) with similar functionality and use one of these instead.

Run through these steps, and you’ll be ready to update the PHP version on your WordPress site – and enjoy all of the benefits that come with this!

If you run into any issues whilst doing this or need help, you should contact a professional web developer, your hosting company, or your theme and plugins authors. All of these will be happy to help here.

We can now get on to the final part: actually updating your website’s PHP version.

## How to update your website’s PHP version for a faster, more secure website

You’re now ready to update your website’s PHP version! You’ve done due diligence, got backups, and are in the best possible shape to do the update.

As the PHP version is set at the server level by your hosting company, updating involves either interacting with your host’s settings or asking them to do it.

Thus, exactly *how* to do the update depends on your hosting company. We’ve asked hosting companies to submit instructions on how to update your PHP version on their hosting, and [you’ll find a list of hosts who have instructions available here](https://github.com/WordPress/servehappy-resources/blob/master/tutorials/hosting-specific/tutorials-en.md).

If you can’t find your host on this list, and don’t recognize the names of these [system-specific and tool-specific update tutorials](https://github.com/WordPress/servehappy-resources), then email your hosting company and ask them to help! Here’s some template text you can use:

```
Dear Hosting Provider,

I want my website to be as performant and secure as
possible with the latest version of PHP. For the server
my WordPress site is hosted on, I want to ensure that
is the case. If I am not already on the latest version
of PHP, please let me know what steps I need to take
to update.

Thanks!
```

If you run into any issues at this stage, either change the PHP version back yourself, contact your hosting company or a professional web developer. In the unlikely event something goes wrong and you need to restore your backup, contact your host and ask them to restore the previous version of PHP you had running. You can then restore your backup.

You should now have all the information you need to update! Nice work! With an up-to-date version of PHP you’ll enjoy a faster, more secure website and happier visitors.

## Faster, more secure WordPress websites for all

Making sure you have the latest version of PHP ensures your website is as fast, and secure as possible.

You now have all the information you need to update to the latest version of PHP, and you know how to update in the future as well. Look out for more PHP update messages on your WordPress Dashboard going forwards, or keep an eye on your hosting company’s news for more information.

As a final reminder: contact your hosting company, a professional web developer, or your theme and/or plugin authors for any additional questions. They’ll all be able to help out with their areas of expertise.

**Thanks for making the internet a better place!**
