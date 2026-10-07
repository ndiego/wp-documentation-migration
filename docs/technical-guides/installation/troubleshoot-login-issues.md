---
title: Troubleshoot login issues
slug: troubleshoot-login-issues
original_url: https://wordpress.org/documentation/article/troubleshoot-login-issues/
wp_id: 10844598
categories:
- technical-guides
- installation
date: '2018-11-03T15:48:36'
modified: '2023-01-13T18:10:50'
migration:
  status: clean
  notes:
  - link to old slug 'resetting-your-password' rewritten to 'reset-your-password' (via 301)
  - link to 'finding-server-info' points to moved page https://developer.wordpress.org/advanced-administration/server/server-info/
  counts:
    internal_links_rewritten: 2
    links_to_moved_external: 1
    preserved_heading_anchors: 4
---

# Troubleshoot login issues

If you are having trouble logging in to your WordPress [Administration Screen](../../support-guides/dashboard/administration-screens.md), here are some possible solutions.

<a id="password-problems-1"></a>

## Password Problems

For information on problems logging in due to a wrong or lost password, see [Resetting Your Password](../../support-guides/dashboard/reset-your-password.md). Remember: the Username and Password fields are **case-sensitive**.

<a id="enable-cookies-1"></a>

## Enable Cookies

In order to make sure that cookies are enabled for your browser, you need to:

1.  Clear your browser cookies.
2.  Clear your browser cache.

To see how to clear cookies and caches on various browsers, visit [Clearing Cache and Cookies](https://support.google.com/accounts/answer/32050?hl=en&rd=2).

<a id="check-your-firewall-1"></a>

## Check your Firewall

Some firewalls (e.g., eTrust Personal Firewall) block you from logging in to WordPress. Disable your firewall and try to log in again.

<a id="if-all-else-fails-1"></a>

## If All Else Fails

If these steps fail, please indicate that you have tried all these possible solutions when posting at the [WordPress Support Forum](https://wordpress.org/support/).

Be sure to give [details of your server setup](https://developer.wordpress.org/advanced-administration/server/server-info/), if you know it, including MySQL and PHP versions, as well as your operating system (OS), browser, and the WordPress version that is causing these problems.

#### Changelog

-   Removed technical parts from the end user doc. Mar 2-2022
-   Removed 2020-06-20
    -   Removed ‘Secure HTTPS’, because its advice is modifying core file.
