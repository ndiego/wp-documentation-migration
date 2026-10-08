---
title: Roles and Capabilities
slug: roles-and-capabilities
position: 1
original_url: https://wordpress.org/documentation/article/roles-and-capabilities/
wp_id: 10937050
legacy_categories:
- support-guides
- dashboard
date: '2018-12-01T12:56:13'
modified: '2026-09-02T02:48:19'
migration:
  status: clean
  notes:
  - link to old slug 'glossary' rewritten to 'wordpress-glossary' (via 301)
  - link to old slug 'writing-posts' rewritten to 'write-posts-classic-editor' (via 301)
  - link to old slug 'pages' rewritten to 'create-pages' (via 301)
  - link to old slug 'managing-plugins' rewritten to 'manage-plugins' (via 301)
  - link to old slug 'using-themes' rewritten to 'work-with-themes' (via 301)
  - link to 'create-a-network' points to moved page https://developer.wordpress.org/advanced-administration/multisite/create-network/
  - link to old slug 'appearance-customize-screen' rewritten to 'customizer' (via 301)
  - link to 'multisite-network-administration' points to moved page https://developer.wordpress.org/advanced-administration/multisite/administration/
  counts:
    callouts: 1
    callouts_info: 1
    internal_links_rewritten: 43
    legacy_support_links_fixed: 43
    links_to_moved_external: 2
    relative_url_made_absolute: 45
    tables_gfm: 2
---

# Roles and Capabilities

WordPress uses a concept of [Roles](#roles), designed to give the [site](../../overview/where-to-start/wordpress-glossary.md#site) owner the ability to control what users can and cannot do within the site. A site owner can manage the user access to such tasks as [writing and editing posts](../writing-and-publishing/write-posts-classic-editor.md), [creating Pages](../writing-and-publishing/create-pages.md), [creating categories](https://codex.wordpress.org/Posts_Categories_SubPanel), [moderating comments](https://codex.wordpress.org/Comment_Moderation), [managing plugins](../administration-screens/plugins/manage-plugins.md), [managing themes](../../editing-and-design/themes/work-with-themes.md), and [managing other users](https://codex.wordpress.org/Users_Screen), by assigning a specific role to each of the users.

WordPress has six pre-defined roles: [Super Admin](#super-admin), [Administrator](#administrator), [Editor](#editor), [Author](#author), [Contributor](#contributor) and [Subscriber](#subscriber). Each role is allowed to perform a set of tasks called [Capabilities](../../overview/where-to-start/wordpress-glossary.md#capabilities). There are many capabilities including “[publish_posts](#publish_posts)“, “[moderate_comments](#moderate_comments)“, and “[edit_users](#edit_users)“. [A default set](#capability-vs-role-table) of capabilities is pre-assigned to each role, but other capabilities can be assigned or removed using the [add_cap()](https://codex.wordpress.org/Function_Reference/add_cap) and [remove_cap()](https://codex.wordpress.org/Function_Reference/remove_cap) functions. New roles can be introduced or removed using the [add_role()](https://codex.wordpress.org/Function_Reference/add_role) and [remove_role()](https://codex.wordpress.org/Function_Reference/remove_role) functions.

The [Super Admin](#super-admin) role allows a user to perform all possible capabilities. Each of the other roles has a decreasing number of allowed capabilities. For instance, the [Subscriber](#subscriber) role has just the “[read](#read)” capability. One particular role should not be considered to be senior to another role. Rather, consider that roles define the user’s responsibilities within the site.

## Summary of Roles

-   [Super Admin](#super-admin) – somebody with access to the site network administration features and all other features. See the [Create a Network](https://developer.wordpress.org/advanced-administration/multisite/create-network/) article.
-   [Administrator](#administrator) (*slug: ‘administrator’*) – somebody who has access to all the administration features within a single site.
-   [Editor](#editor) (*slug: ‘editor’*) – somebody who can publish and manage posts including the posts of other users.
-   [Author](#author)  (*slug: ‘author’*)  – somebody who can publish and manage their own posts.
-   [Contributor](#contributor) (*slug: ‘contributor’*) – somebody who can write and manage their own posts but cannot publish them.
-   [Subscriber](#subscriber) (*slug: ‘subscriber’*) – somebody who can only manage their profile.

Upon installing WordPress, an Administrator account is automatically created.

The default role for new users can be set in [Administration Screens](../administration-screens/README.md) > [Settings](../administration-screens/README.md#settings-configuration-settings) > [General](../administration-screens/settings/settings-general-screen.md).

## Roles

A Role defines a set of tasks a user assigned the role is allowed to perform. For instance, the [Super Admin](#super-admin) role encompasses every possible task that can be performed within a [Network](../../overview/where-to-start/wordpress-glossary.md#network) of virtual WordPress [sites](../../overview/where-to-start/wordpress-glossary.md#site). The [Administrator](#administrator) role limits the allowed tasks only to those which affect a single site. On the other hand, the [Author](#author) role allows the execution of just a small subset of tasks.

The following sections list the default Roles and their capabilities:

### Super Admin

Multisite Super Admins have, by default, all capabilities. The following Multisite-only capabilities are therefore only available to Super Admins:

-   [create_sites](#create_sites)
-   [delete_sites](#delete_sites)
-   [manage_network](#manage_network)
-   [manage_sites](#manage_sites)
-   [manage_network_users](#manage_network_users)
-   [manage_network_plugins](#manage_network_plugins)
-   [manage_network_themes](#manage_network_themes)
-   [manage_network_options](#manage_network_options)
-   [upgrade_network](#upgrade_network)
-   [setup_network](#setup_network)

In the case of single site WordPress installation, Administrators are, in effect, Super Admins. As such, they are the only ones to have access to [additional admin capabilities](#additional-admin-capabilities).

### Administrator

The capabilities of Administrators differs between single site and [Multisite](../../overview/where-to-start/wordpress-glossary.md#multisite) WordPress installations. All administrators have the following capabilities:

-   [activate_plugins](#activate_plugins)
-   [delete_others_pages](#delete_others_pages)
-   [delete_others_posts](#delete_others_posts)
-   [delete_pages](#delete_pages)
-   [delete_posts](#delete_posts)
-   [delete_private_pages](#delete_private_pages)
-   [delete_private_posts](#delete_private_posts)
-   [delete_published_pages](#delete_published_pages)
-   [delete_published_posts](#delete_published_posts)
-   [edit_dashboard](#edit_dashboard)
-   [edit_others_pages](#edit_others_pages)
-   [edit_others_posts](#edit_others_posts)
-   [edit_pages](#edit_pages)
-   [edit_posts](#edit_posts)
-   [edit_private_pages](#edit_private_pages)
-   [edit_private_posts](#edit_private_posts)
-   [edit_published_pages](#edit_published_pages)
-   [edit_published_posts](#edit_published_posts)
-   [edit_theme_options](#edit_theme_options)
-   [export](#export)
-   [import](#import)
-   [list_users](#list_users)
-   [manage_categories](#manage_categories)
-   [manage_links](#manage_links)
-   [manage_options](#manage_options)
-   [moderate_comments](#moderate_comments)
-   [promote_users](#promote_users)
-   [publish_pages](#publish_pages)
-   [publish_posts](#publish_posts)
-   [read_private_pages](#read_private_pages)
-   [read_private_posts](#read_private_posts)
-   [read](#read)
-   [remove_users](#remove_users)
-   [switch_themes](#switch_themes)
-   [upload_files](#upload_files)
-   [customize](#customize)
-   [delete_site](#delete_site)

#### Additional Admin Capabilities

Only Administrators of single site installations have the following capabilities. In [Multisite](../../overview/where-to-start/wordpress-glossary.md#multisite), only the Super Admin has these abilities:

-   [update_core](#update_core)
-   [update_plugins](#update_plugins)
-   [update_themes](#update_themes)
-   [install_plugins](#install_plugins)
-   [install_themes](#install_themes)
-   [delete_themes](#delete_themes)
-   [delete_plugins](#delete_plugins)
-   [edit_plugins](#edit_plugins)
-   [edit_themes](#edit_themes)
-   [edit_files](#edit_files)
-   [edit_users](#edit_users)
-   [add_users](#add_users)
-   [create_users](#create_users)
-   [delete_users](#delete_users)
-   [unfiltered_html](#unfiltered_html)

### Editor

-   [delete_others_pages](#delete_others_pages)
-   [delete_others_posts](#delete_others_posts)
-   [delete_pages](#delete_pages)
-   [delete_posts](#delete_posts)
-   [delete_private_pages](#delete_private_pages)
-   [delete_private_posts](#delete_private_posts)
-   [delete_published_pages](#delete_published_pages)
-   [delete_published_posts](#delete_published_posts)
-   [edit_others_pages](#edit_others_pages)
-   [edit_others_posts](#edit_others_posts)
-   [edit_pages](#edit_pages)
-   [edit_posts](#edit_posts)
-   [edit_private_pages](#edit_private_pages)
-   [edit_private_posts](#edit_private_posts)
-   [edit_published_pages](#edit_published_pages)
-   [edit_published_posts](#edit_published_posts)
-   [manage_categories](#manage_categories)
-   [manage_links](#manage_links)
-   [moderate_comments](#moderate_comments)
-   [publish_pages](#publish_pages)
-   [publish_posts](#publish_posts)
-   [read](#read)
-   [read_private_pages](#read_private_pages)
-   [read_private_posts](#read_private_posts)
-   [unfiltered_html](#unfiltered_html) (not with Multisite)
-   [upload_files](#upload_files)

### Author

-   [delete_posts](#delete_posts)
-   [delete_published_posts](#delete_published_posts)
-   [edit_posts](#edit_posts)
-   [edit_published_posts](#edit_published_posts)
-   [publish_posts](#publish_posts)
-   [read](#read)
-   [upload_files](#upload_files)

### Contributor

-   [delete_posts](#delete_posts)
-   [edit_posts](#edit_posts)
-   [read](#read)

### Subscriber

-   [read](#read)

### Special Cases

The following capabilities are special cases:

-   [unfiltered_upload](#unfiltered_upload) – This capability is not available to any role by default (including Super Admins). The capability needs to be enabled by defining the following constant:

```
define( 'ALLOW_UNFILTERED_UPLOADS', true );
```

With this constant defined, all roles on a single site install can be given the unfiltered_upload capability, but only Super Admins can be given the capability on a Multisite install.

### Capability vs. Role Table

Note that the capabilities of Administrators **differs** between single site and [Multisite](../../overview/where-to-start/wordpress-glossary.md#multisite) WordPress installations, [as described above](#additional-admin-capabilities) .

| Capability | Super Admin | Administrator | Editor | Author | Contributor | Subscriber |
| --- | --- | --- | --- | --- | --- | --- |
| create_sites | yes | x | x | x | x | x |
| delete_sites | yes | x | x | x | x | x |
| manage_network | yes | x | x | x | x | x |
| manage_sites | yes | x | x | x | x | x |
| manage_network_users | yes | x | x | x | x | x |
| manage_network_plugins | yes | x | x | x | x | x |
| manage_network_themes | yes | x | x | x | x | x |
| manage_network_options | yes | x | x | x | x | x |
| upload_plugins | yes | x | x | x | x | x |
| upload_themes | yes | x | x | x | x | x |
| upload_network | yes | x | x | x | x | x |
| upgrade_network | yes | x | x | x | x | x |
| setup_network | yes | x | x | x | x | x |
| activate_plugins | yes | yes (single site or <br>enabled by <br>network setting) | x | x | x | x |
| create_users | yes | yes (single site) | x | x | x | x |
| delete_plugins | yes | yes (single site) | x | x | x | x |
| delete_themes | yes | yes (single site) | x | x | x | x |
| delete_users | yes | yes (single site) | x | x | x | x |
| edit_files | yes | yes (single site) | x | x | x | x |
| edit_plugins | yes | yes (single site) | x | x | x | x |
| edit_theme_options | yes | yes | x | x | x | x |
| edit_themes | yes | yes (single site) | x | x | x | x |
| edit_users | yes | yes (single site) | x | x | x | x |
| export | yes | yes | x | x | x | x |
| import | yes | yes | x | x | x | x |
| install_plugins | yes | yes (single site) | x | x | x | x |
| install_themes | yes | yes (single site) | x | x | x | x |
| list_users | yes | yes | x | x | x | x |
| manage_options | yes | yes | x | x | x | x |
| promote_users | yes | yes | x | x | x | x |
| remove_users | yes | yes | x | x | x | x |
| switch_themes | yes | yes | x | x | x | x |
| update_core | yes | yes (single site) | x | x | x | x |
| update_plugins | yes | yes (single site) | x | x | x | x |
| update_themes | yes | yes (single site) | x | x | x | x |
| edit_dashboard | yes | yes | x | x | x | x |
| customize | yes | yes | x | x | x | x |
| delete_site | yes | yes | x | x | x | x |
| moderate_comments | yes | yes | yes | x | x | x |
| manage_categories | yes | yes | yes | x | x | x |
| manage_links | yes | yes | yes | x | x | x |
| edit_others_posts | yes | yes | yes | x | x | x |
| edit_pages | yes | yes | yes | x | x | x |
| edit_others_pages | yes | yes | yes | x | x | x |
| edit_published_pages | yes | yes | yes | x | x | x |
| publish_pages | yes | yes | yes | x | x | x |
| delete_pages | yes | yes | yes | x | x | x |
| delete_others_pages | yes | yes | yes | x | x | x |
| delete_published_pages | yes | yes | yes | x | x | x |
| delete_others_pos | yes | yes | yes | x | x | x |
| delete_private_posts | yes | yes | yes | x | x | x |
| edit_private_posts | yes | yes | yes | x | x | x |
| read_private_posts | yes | yes | yes | x | x | x |
| delete_private_pages | yes | yes | yes | x | x | x |
| edit_private_pages | yes | yes | yes | x | x | x |
| read_private_pages | yes | yes | yes | x | x | x |
| unfiltered_html | yes | yes (single site) | yes (single site) | x | x | x |
| unfiltered_html | yes | yes | yes | x | x | x |
| edit_published_posts | yes | yes | yes | yes | x | x |
| upload_files | yes | yes | yes | yes | x | x |
| publish_posts | yes | yes | yes | yes | x | x |
| delete_published_posts | yes | yes | yes | yes | x | x |
| edit_posts | yes | yes | yes | yes | yes | x |
| delete_posts | yes | yes | yes | yes | yes | x |
| read | yes | yes | yes | yes | yes | yes |

## Capabilities

### Side Editor Capabilities

The Site Editor is available when a block theme is active and allows users to manage site templates, template parts, styles, navigation, and content from a single editing interface.

Access to Site Editor features depends on the capabilities assigned to the current user. The following capabilities may be relevant when creating a custom role that needs access to the Site Editor:

| Capability | Description |
| --- | --- |
| `edit_theme_options` | Grants access to the Site Editor and its navigation menu. |
| `edit_posts` | Allows users to edit posts, which is required for managing templates. |
| `edit_pages` | Allows users to edit pages, which is required for managing page templates. |
| `edit_others_posts` | Allows users to edit others’ posts, which is required for managing templates. |
| `read` | Allows users to view the site, which is required for previewing changes. |
| `upload_files` | Allows users to upload media, which is required for adding images and media. |

`edit_theme_options` is the primary capability used by WordPress when determining whether a user can access and manage templates through the Site Editor. Other capabilities may be required depending on which types of content the user is expected to edit.

#### Creating a Custom Site Editor Role

A custom role can be created with the capabilities required for the tasks the user should be able to perform. For example:

```php
function wporg_add_site_editor_role() {
	add_role(
		'site_editor',
		__( 'Site Editor', 'textdomain' ),
		array(
			'read'               => true,
			'edit_theme_options' => true,
			'edit_posts'         => true,
			'edit_pages'         => true,
			'edit_others_posts'  => true,
			'upload_files'       => true,
		)
	);
}
add_action( 'init', 'wporg_add_site_editor_role' );
```

Capabilities can also be added to an existing role by using `WP_Role::add_cap()`:

```php
function wporg_add_site_editor_capabilities() {
	$role = get_role( 'editor' );
	if ( $role ) {
		$role->add_cap( 'edit_theme_options' );
	}
}
add_action( 'init', 'wporg_add_site_editor_capabilities' );
```

When adding capabilities to an existing role, consider the broader permissions that each capability provides. For example, `edit_theme_options` is not limited exclusively to the Site Editor and may grant access to other theme-related administrative functionality.

#### REST API Capability Checks

The Site Editor uses the WordPress REST API to retrieve and update templates, template parts, pages, navigation data, patterns, and other information.

For template and template-part endpoints, WordPress checks whether the current user has the `edit_theme_options` capability. A user without this capability may receive an authorization error when the Site Editor attempts to access these endpoints.

Other REST API endpoints can perform their own capability checks. For example, endpoints dealing with posts or pages may require capabilities such as:

-   `edit_posts`
-   `edit_pages`
-   `edit_others_posts`
-   other object-specific capabilities depending on the requested operation

If a custom role can open the Site Editor but some sections fail to load or save, check the browser’s developer tools for REST API requests returning `401 Unauthorized` or `403 Forbidden` responses.

The REST API response will often include an error code and message indicating the type of permission that failed. This can help identify whether the role is missing a capability required by that particular endpoint.

Only grant the capabilities required for the tasks the role is intended to perform.

### switch_themes

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Appearance
    -   Appearance > Themes

### edit_themes

-   Since 2.0
-   Allows access to Appearance > [Theme Editor](https://codex.wordpress.org/Appearance_Editor_SubPanel) to edit theme files.

### edit_theme_options

> [!NOTE]
> While this capability grants access to the Site Editor, additional capabilities may be required for full functionality. For example, users may also need `edit_posts`, `edit_pages`, and `edit_others_posts` to fully utilize the Site Editor’s features.

-   Since 3.0
-   Allows users to edit theme options, including access to the Site Editor in Full Site Editing (FSE) environments and allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Appearance > [Widgets](https://codex.wordpress.org/Appearance_Widgets_SubPanel)
    -   Appearance > [Menus](../administration-screens/appearance/appearance-menus-screen.md)
    -   Appearance > [Customize](../administration-screens/appearance/customizer.md) if they are supported by the current theme
    -   Appearance > [Header](https://codex.wordpress.org/Appearance_Header_SubPanel)

### install_themes

-   Since 2.8
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Appearance > Add New Themes

### activate_plugins

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   [Plugins](../administration-screens/README.md#plugins-add-functionality-to-your-blog)

### edit_plugins

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   [Plugins](../administration-screens/README.md#plugins-add-functionality-to-your-blog) > [Plugin Editor](../administration-screens/README.md#plugin-editor)

### install_plugins

-   Since 2.7
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   [Plugins](../administration-screens/README.md#plugins-add-functionality-to-your-blog) > Add New

### edit_users

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   [Users](../administration-screens/README.md#users-your-blogging-family)

### edit_files

-   Since 2.0
-   **Note:** No longer used.

### manage_options

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Settings > General
    -   Settings > Writing
    -   Settings > Reading
    -   Settings > Discussion
    -   Settings > Permalinks
    -   Settings > Miscellaneous

### moderate_comments

-   Since 2.0
-   Allows users to moderate comments from the Comments Screen (although a user needs the [edit_posts](#edit_posts) Capability in order to access this)

### manage_categories

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Posts > Categories
    -   Links > Categories

### manage_links

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Links
    -   Links > Add New

### upload_files

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md)options:
    -   Media
    -   Media > Add New

### import

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Tools > Import
    -   Tools > Export

### unfiltered_html

-   Since 2.0
-   Allows user to post HTML markup or even JavaScript code in pages, posts, comments and widgets.
-   **Note:** Enabling this option for untrusted users may result in their posting malicious or poorly formatted code.
-   **Note:** In WordPress Multisite, only Super Admins have the `unfiltered_html` capability.

### edit_posts

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Posts
    -   Posts > Add New
    -   Comments
    -   Comments > Awaiting Moderation

### edit_others_posts

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Manage > Comments (*Lets user delete and edit every comment, see edit_posts above*)
-   user can edit other users’ posts through function get_others_drafts()
-   user can see other users’ images in inline-uploading [no? see [inline-uploading.php](https://trac.wordpress.org/file/trunk/wp-admin/inline-uploading.php)]
-   See [Exceptions](#exceptions)

### edit_published_posts

-   Since 2.0
-   User can edit their published posts. *This capability is off by default.*
-   The core checks the capability **edit_posts**, but on demand this check is changed to **edit_published_posts**.
-   If you don’t want a user to be able to edit their published posts, remove this capability.

### publish_posts

-   Since 2.0
-   See and use the “publish” button when editing their post *(otherwise they can only save drafts)*
-   Can use XML-RPC to publish *(otherwise they get a “Sorry, you can not post on this weblog or category.”)*

### edit_pages

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   Pages
    -   Pages > Add New

### read

-   Since 2.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   [Dashboard](../administration-screens/dashboard/dashboard-screen.md)
    -   Users > Your Profile
-   *Used nowhere in the core code except the menu.php*

### publish_pages

-   Since 2.1

### edit_others_pages

-   Since 2.1

### edit_published_pages

-   Since 2.1

### delete_pages

-   Since 2.1

### delete_others_pages

-   Since 2.1

### delete_published_pages

-   Since 2.1

### delete_posts

-   Since 2.1

### delete_others_posts

-   Since 2.1

### delete_published_posts

-   Since 2.1

### delete_private_posts

-   Since 2.1

### edit_private_posts

-   Since 2.1

### read_private_posts

-   Since 2.1

### delete_private_pages

-   Since 2.1

### edit_private_pages

-   Since 2.1

### read_private_pages

-   Since 2.1

### delete_users

-   Since 2.1

### create_users

-   Since 2.1
-   Allows creating new users.
    -   Without other capabilities, created users will have your blog’s [New User Default Role](../administration-screens/settings/settings-general-screen.md).

### unfiltered_upload

-   Since 2.3

### edit_dashboard

-   Since 2.5

### customize

-   Since 4.0
-   Allows access to the Customizer.

### delete_site

-   Since 4.0
-   Allows the user to delete the current site (Multisite only).

### update_plugins

-   Since 2.6

### delete_plugins

-   Since 2.6

### update_themes

-   Since 2.7

### update_core

-   Since 3.0

### list_users

-   Since 3.0
-   Allows access to [Administration Screens](../administration-screens/README.md) options:
    -   [Users](../administration-screens/README.md#users-your-blogging-family)

### remove_users

-   Since 3.0

### add_users

-   Since 3.0
-   Replaced in 4.4 with [promote_users](#promote_users)

### promote_users

-   Since 3.0
-   Enables the “Change role to…” dropdown in the admin user list.
    -   This does not depend on ‘[edit_users](#edit_users)‘ capability.
-   Enables the ‘Add Existing User’ to function for multi-site installs.

### delete_themes

-   Since 3.0

### export

-   Since 3.0

### edit_comment

-   Since 3.1

### create_sites

-   Since 3.1
-   Multi-site only
-   Allows user to create sites on the network

### delete_sites

-   Since 3.1
-   Multi-site only
-   Allows user to delete sites on the network

### manage_network

-   Since 3.0
-   Multi-site only
-   Allows access to [Super Admin](https://developer.wordpress.org/advanced-administration/multisite/administration/) menu
-   Allows user to upgrade network

### manage_sites

-   Since 3.0
-   Multi-site only
-   Allows access to [Network Sites](https://codex.wordpress.org/Network_Admin#Sites) menu
-   Allows user to add, edit, delete, archive, unarchive, activate, deactivate, spam and unspam new site/blog in the network

### manage_network_users

-   Since 3.0
-   Multi-site only
-   Allows access to [Network Users](https://codex.wordpress.org/Network_Admin#Users) menu

### manage_network_themes

-   Since 3.0
-   Multi-site only
-   Allows access to [Network Themes](https://codex.wordpress.org/Network_Admin#Themes) menu

### manage_network_options

-   Since 3.0
-   Multi-site only
-   Allows access to [Network Options](https://codex.wordpress.org/Network_Admin#Settings) menu

### manage_network_plugins

-   Multi-site only
-   Allows access to [Network Plugins](https://codex.wordpress.org/Network_Admin#Plugins) menu

### upload_plugins

-   Since 4.0
-   Multi-site only
-   Allows user to upload plugin ZIP files from the [Network Plugins](https://codex.wordpress.org/Network_Admin#Plugins) -> Add New menu

### upload_themes

-   Since 4.0
-   Multi-site only
-   Allows user to upload theme ZIP files from the [Network Themes](https://codex.wordpress.org/Network_Admin#Themes) -> Add New menu

### upgrade_network

-   Since 4.8
-   Multi-site only
-   is used to determine whether a user can access the Network Upgrade page in the network admin. Related to this, the capability is also checked to determine whether to show the notice that a network upgrade is required. The capability is not mapped, so it is only granted to network administrators. See [#39205](https://core.trac.wordpress.org/ticket/39205) for background discussion.

### setup_network

-   Since 4.8
-   Multi-site only
-   is used to determine whether a user can setup multisite, i.e. access the Network Setup page. Before setting up a multisite, the capability is mapped to the \`manage_options\` capability, so that it is granted to administrators. Once multisite is setup, it is mapped to \`manage_network_options\`, so that it is granted to network administrators. See [#39206](https://core.trac.wordpress.org/ticket/39206) for background discussion.

## Resources

### Plugins

-   [Members Plugin](https://wordpress.org/plugins/members/)
-   [User Access Manager](https://wordpress.org/plugins/user-access-manager/)
-   [Advanced Access Manager](https://wordpress.org/plugins/advanced-access-manager/)
-   [User Role Editor](https://wordpress.org/plugins/user-role-editor/)
-   [WordPress User Role Editor](https://wordpress.org/plugins/wpfront-user-role-editor/)
-   [Simple Membership Plugin](https://wordpress.org/plugins/simple-membership/)
-   [View Admin As](https://wordpress.org/plugins/view-admin-as/) (manage & test roles)
