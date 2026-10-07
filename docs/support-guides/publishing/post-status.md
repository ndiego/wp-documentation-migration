---
title: Post Status
slug: post-status
original_url: https://wordpress.org/documentation/article/post-status/
wp_id: 10840192
categories:
- support-guides
- publishing
date: '2018-11-02T05:17:27'
modified: '2023-01-13T22:08:59'
migration:
  status: clean
  notes:
  - link to old slug 'writing-posts' rewritten to 'write-posts-classic-editor' (via 301)
  counts:
    code_links_swapped: 6
    internal_links_rewritten: 23
    legacy_support_links_fixed: 23
    relative_url_made_absolute: 23
---

# Post Status

Posts in WordPress can have one of a number of statuses. The status of a given post determines how WordPress handles that post. For instance, public posts viewable by everyone are assigned the publish status, while drafts are assigned the draft status. The status is stored in the post_status field in the wp_posts table.

WordPress provides 8 built-in statuses you can use. WordPress 3.0 gave you the capability to add your own custom post status and to use it in different ways.

## Workflow

WordPress provides built-in features that empower some users (based on their [Roles and Capabilities](../dashboard/roles-and-capabilities.md)) to review content submitted to the website before it is published. This is commonly called “workflow.” WordPress’s workflow features rely on the value of a post’s `post_status` field to know which step in the workflow process the post is currently held in.

Most users are already familiar with at least two workflow states:

-   Posts that are published and visible to everyone (including users who are logged out) are given [the](#publish) [`publish`](#publish) [status](#publish).
-   Drafts that are not yet published are assigned [the](#draft) [`draft`](#draft) [status](#draft).

Internally, WordPress sets the post status to `publish` when you click the “Publish” button, and WordPress sets the post status to `draft` when you click the “Save Draft” button. Similarly, if your website has users granted [the](../dashboard/roles-and-capabilities.md#edit_posts) [`edit_posts`](../dashboard/roles-and-capabilities.md#edit_posts) [capability](../dashboard/roles-and-capabilities.md#edit_posts) but not [the](../dashboard/roles-and-capabilities.md#publish_posts) [`publish_posts`](../dashboard/roles-and-capabilities.md#publish_posts) [capability](../dashboard/roles-and-capabilities.md#publish_posts), then when those users start writing a new post, WordPress will display a “Submit for Review” button instead of a “Publish” button. Likewise, WordPress then assigns the post that user created [the](#pending) [`pending`](#pending) [status](#pending) when they press that button.

The status of a post can also be set in the [Administration Screen](../dashboard/administration-screens.md) and [Add New Posts](write-posts-classic-editor.md) Screen by any user with the capability needed to assign the post to the given status. Internally, all of these posts are stored in the same place (the [`wp_posts`](https://codex.wordpress.org/Database_Description#Table:_wp_posts) table), and are differentiated by a column called `post_status`.

## Default Statuses

There are 8 major post statuses that WordPress uses by default.

### Publish

Viewable by everyone. (publish)

### Future

Scheduled to be published in a future date. (future)

### Draft

Incomplete post viewable by anyone with proper [user role](../dashboard/roles-and-capabilities.md). (draft)

### Pending

Awaiting a user with the `publish_posts` capability (typically a user assigned [the](../dashboard/roles-and-capabilities.md#editor) [`Editor`](../dashboard/roles-and-capabilities.md#editor) [role](../dashboard/roles-and-capabilities.md#editor)) to publish. (pending)

### Private

Viewable only to WordPress users at Administrator level. (private)

### Trash

Posts in the Trash are assigned the `trash` status. (trash)

### Auto-Draft

[Revisions](https://codex.wordpress.org/Revisions) that WordPress saves automatically while you are editing. (auto-draft)

### Inherit

Used with a child post (such as [Attachments](https://codex.wordpress.org/Attachments) and [Revisions](https://codex.wordpress.org/Revisions)) to determine the actual status from the parent post. (inherit)

## Custom Status

**NOTICE:**
This function does NOT add the registered post status to the Administration Screen. This functionality is pending future development. Please refer to [Trac Ticket #12706](https://core.trac.wordpress.org/ticket/12706).
Consider the action hook [post_submitbox_misc_actions](https://core.trac.wordpress.org/browser/tags/3.5.1/wp-admin/includes/meta-boxes.php#L183) for adding this parameter.

A Custom Status is a Post Status you define.

Adding a custom status to WordPress is done via the [register_post_status()](https://developer.wordpress.org/reference/functions/register_post_status) function. This function allows you to define the post status and how it operates within WordPress.

Here’s a basic example of adding a custom post status called “Unread”:

```
function custom_post_status(){
	register_post_status( 'unread', array(
		'label'                     => _x( 'Unread', 'post' ),
		'public'                    => true,
		'exclude_from_search'       => false,
		'show_in_admin_all_list'    => true,
		'show_in_admin_status_list' => true,
		'label_count'               => _n_noop( 'Unread (%s)', 'Unread (%s)' ),
	) );
}
add_action( 'init', 'custom_post_status' );
```

## Resources

-   [WordPress Post Status Generator](http://generatewp.com/post-status/)

## Related

-   [Roles and Capabilities](../dashboard/roles-and-capabilities.md#editor)

## Code Documentation

-   Function:  [get_post_status()](https://developer.wordpress.org/reference/functions/get_post_status) – Retrieve the post status based on the Post ID.
