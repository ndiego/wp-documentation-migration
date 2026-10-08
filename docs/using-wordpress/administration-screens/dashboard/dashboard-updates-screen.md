---
title: Dashboard Updates screen
slug: dashboard-updates-screen
position: 2
original_url: https://wordpress.org/documentation/article/dashboard-updates-screen/
wp_id: 11102114
legacy_categories:
- support-guides
- dashboard
date: '2019-01-22T16:30:00'
modified: '2024-06-06T14:01:35'
migration:
  status: clean
  notes:
  - link to 'upgrading-wordpress-extended-instructions' points to moved page https://developer.wordpress.org/advanced-administration/upgrade/upgrading/
  counts:
    callouts: 16
    callouts_alert: 1
    callouts_info: 15
    images: 1
    images_missing_alt: 1
    internal_links_rewritten: 1
    legacy_support_links_fixed: 1
    links_to_moved_external: 1
    relative_url_made_absolute: 3
---

# Dashboard Updates screen

The **Dashboard Updates Screen**
provides the links necessary to install a ‘core’ WordPress upgrade
automatically, or to download the file necessary to complete a manual
upgrade.

In addition to the ‘core’ update process, this Screen provides
the ability to upgrade all plugins and themes, active or inactive, that
have available updates. For installs that have set the language to a
language different from English (United States), you can also install
translation updates.

[![](../../../assets/images/2019/01/dashboard-updates.png)](https://wordpress.org/support/?attachment_id=11102166)

*Dashboard > Updates when everything is up to date.*

## WordPress Updates

#### No Upgrade is Available

When visiting the **Dashboard Updates Screen**, if you are running the latest version of WordPress, you should see messages like this:

> [!NOTE]
> **Y**o**u have the latest version of WordPress. Future security updates will be applied automatically.**<br>
> *If you need to re-install version x.x, you can do so here or download the package and re-install manually:*

**Re-install now** – Click to to reinstall the current version. You should receive the following messages if the upgrade proceeds successfully:

> [!NOTE]
> *Downloading update from <https://wordpress.org/wordpress-x.x.zip>*<br>
> *Unpacking the core update*<br>
> *Verifying the unpacked files*<br>
> *Installing the latest version*<br>
> *Upgrading database*<br>
> *WordPress upgraded successfully*

**Download x.x** – Click this to download the zip file contain the latest version.

#### An Upgrade is Available

When visiting the **Dashboard Updates Screen**, and there is an WordPress upgrade available, you should see messages like this:

> [!CAUTION]
> *before upgrading, please backup your database and files.*

**Upgrade Automatically** – Press this button to begin the automatic upgrade process. The following messages will display during and upon completion of the upgrade:

> [!NOTE]
> *Downloading update from <https://wordpress.org/nightly-builds/wordpress-latest.zip>*<br>
> *Unpacking the core update*<br>
> *Verifying the unpacked files*<br>
> *Installing the latest version*<br>
> *Upgrading database*<br>
> *WordPress upgraded successfully*

**Download x.x** – Click this to download the zip file contain the latest version.

#### Once an Update is Completed

After a successful upgrade is achieved, it is a good time to review any new features about the new Version just installed.

## Plugins

#### No Plugins to Update

When visiting the **Dashboard Updates Screen**, if your plugins (active and inactive) are at the latest versions, you should see this message:

> [!NOTE]
> *Your plugins are all up to date.*

#### Update Plugins

When visiting the **Dashboard Updates Screen**, if there are updates available for one or more plugins (active and inactive), this message displays:

> [!NOTE]
> *The following plugins have new versions available. Check the ones you want to update and then click “Update Plugins”.*

**Update Plugins** – After checking Select All or one or more plugins, click this button to begin the automatic upgrade process. The following messages will display during and upon completion of the upgrade. Messages for each plugin being updated will display. This example shows Akismet being updated:

> [!NOTE]
> *The update process is starting. This process may take awhile on some hosts, so please be patient.* <br>
> *Enabling Maintenance mode…*<br>
> **Updating Plugin Akismet** <br>
> *Downloading update from [plugins](https://wordpress.org/plugins/akismet/).* <br>
> *Unpacking the update…*<br>
> *Installing the latest version.* <br>
> *Removing the old version of the plugin…*<br>
> *Plugin upgraded successfully.* <br>
> *Akismet updated successfully. Show/Hide Details.*<br>
> *Disabling Maintenance mode. All updates have been completed.* <br>
> **Actions:** *Return to Plugins page | Return to WordPress Updates.*

## Themes

### No Themes to Update

When visiting the **Dashboard Updates Screen**, if your themes (active and inactive) are at the latest versions, you should see this message:

> [!NOTE]
> *Your themes are all up to date.*

#### Update Themes

When visiting the **Dashboard Updates Screen**, if there are updates available for one or more themes (active and inactive), this message displays:

> [!NOTE]
> *The following themes have new versions available. Check the ones you want to update and then click “Update Themes”.*<br>
>  **Please Note:** *Any customization you have made to the Themes files will be lost. Please consider using child themes for modifications.*

**Update Themes** – After checking Themes (to Select All), or one or more themes, click this button to begin the automatic upgrade process. The following messages will display during and upon completion of the upgrade. Messages for each theme being updated will display. This example shows the WordPress Classic theme being updated:

> [!NOTE]
> *The update process is starting. This process may take awhile on some hosts, so please be patient.* <br>
> *Enabling Maintenance mode.* <br>
> **Updating WordPress.** <br>
> *Downloading update.* <br>
> *Unpacking the update…*<br>
> *Installing the latest version…*<br>
> *Removing the old version of the theme…*<br>
> *Theme upgraded successfully.* <br>
> *WordPress updated successfully. Show/Hide Details.* <br>
> *Disabling Maintenance mode.* <br>
> *All updates have been completed.*<br>
> **Actions**:*Return to Themes page | Return to WordPress Updates*

## Translations

#### No Translations to Update

When visiting the **Dashboard Updates Screen** on a WordPress install that is set to a different language then English (United States), you should see this message if translations are all up to date:

> [!NOTE]
> *Your translations are all up to date.*

#### Update Translations

If there are new translations available, this message is displayed:

> [!NOTE]
> *New translations are available.*

Below this text will be a button with the text “Update translations”.

When you click the update button, it will tell you which plugins are downloaded and installed. Plugins for WordPress Core will be installed in */wp-content/languages*, while the translations for plugins and themes will be installed in their subfolder under */wp-content/languages*. This example shows the translations for Twenty Fifteen anf Twenty Sixteen being updated for Dutch (nl_NL):

> [!NOTE]
> *Updating translations*<br>
> *Updating translation for Twenty Fifteen (nl_NL)…*<br>
> *Translation was successfully updated.*<br>
> *Updating translation for Twenty Sixteen (nl_NL)…*<br>
> *Translation was successfully updated.*<br>
> **Actions**:*Return to WordPress Updates*<br>
> **Actions**:*Return to WordPress Updates*

## Troubleshooting

**Problem:** If one of the following messages is received after electing to do the Automatic Upgrade:

> [!NOTE]
> *Downloading update .* <br>
> *Download failed.: Could not open handle for fopen() to latest wordpress.*<br>
> *I*n*stallation Failed*

or

> [!NOTE]
> *Download failed.: name lookup timed out* <br>
> *Installation Failed*

**Solution:** Confirm you are properly connected to the internet then do the Automatic Upgrade again.

**Problem:** After doing the upgrade, and received *WordPress upgraded successfully* message, but the following message still displays:

> [!NOTE]
> *An automated WordPress update has failed to complete – please attempt the update again now.*

**Solution:** Delete the **.maintenance** file found in the WordPress root/base folder, then do the Upgrade again.

**Problem:** After clicking on “automatic upgrade” you get a dialog box asking for “Connection Information.” And, no matter what you enter, you continue to get errors.

**Solution:**  Make sure that your entire wordpress directory is owned by the username under which your Apache server runs. For example, if your server runs as https, and your files live in /var/wordpress do a “chown -R apache.apache /var/wordpress.” Note that you might want to edit some permissions for security purposes, in particular a chmod 640 on wp-config.php, to protect access information to your database.

## Related Articles

-   [FAQ Installation](../../../overview/faq/faq-installation.md)
-   [Troubleshooting about upgrading](https://developer.wordpress.org/advanced-administration/upgrade/upgrading/#troubleshooting)
