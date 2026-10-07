---
title: Comparing Patterns, Template Parts, and Synced Patterns (Reusable Blocks)
slug: comparing-patterns-template-parts-and-reusable-blocks
original_url: https://wordpress.org/documentation/article/comparing-patterns-template-parts-and-reusable-blocks/
wp_id: 15289733
categories:
- customization
- appearance
date: '2022-01-25T18:43:32'
modified: '2026-06-26T03:22:29'
migration:
  status: clean
  counts:
    callouts: 1
    callouts_info: 1
    internal_links_rewritten: 3
    tables_gfm: 1
    tables_header_inferred_from_bold_row: 1
---

# Comparing Patterns, Template Parts, and Synced Patterns (Reusable Blocks)

## Overview

With more types of reusable content you can create with WordPress, this article seeks to clarify when it makes sense to use certain types in different situations to help guide you to make the best decisions possible. At a high level, this will focus on Template Part blocks, Block Patterns, and Synced Patterns (Reusable Blocks).

> [!NOTE]
> WordPress 6.3 renamed Reusable Blocks to Patterns. A synced pattern will behave in exactly the same way as a reusable block.

### Template Part

The Template Part block is an advanced block that can be used with a block theme or a theme that supports [template editing](https://wordpress.org/themes/tags/template-editing/). They often come with your theme and are used to organize and display your site structure. For more information, you can learn more in the [Template Part block support article](../theme-blocks/template-part-block.md).

### Synced pattern (Reusable block)

Synced pattern is a kind of block pattern that enabled Synced option, and it will behave in exactly the same way as a reusable block. Editing the synced pattern will update it anywhere it is used. After creating a synced pattern, you can ‘Detach’ it to a regular block, and edit the block without affecting your already saved synced pattern. For more information, you can learn more in the [Synced Pattern article](../block-editor/reusable-blocks.md).

### Block Patterns

Block Patterns are a collection of predefined blocks that you can insert into posts and pages and then customize with your own content. For more information, you can learn more in the [Block Pattern support article](../block-editor/block-pattern.md).

Here’s a table comparing these different options to each other:

|  | Template Part | Synced Patterns <br>(Reusable Block) | Patterns |
| --- | --- | --- | --- |
| Type | Site Structure | User Content | User Content |
| Syncing Ability | Synced | Synced | Un-synced |
| Example | Footer | Business hours | Call to action |

Site structure means it should not be a part of your content, like a post or page. Syncing ability touches on whether if you update it in one spot, it updates everywhere the same block is used.

## Guidelines

Based on the above, this means it’s best to use template parts and Synced pattern for things you want to have in sync with each other whereas patterns are best for content that you expect to change across your site.

In general, template parts should not be added to a Synced pattern or a regular pattern since this is meant to represent site structure rather than content. A template part can include a Synced pattern though or be built using patterns! You can also use block patterns to build templates and template parts, but you should not use a template part inside a pattern.

## Situationals

### Repeated content across your site

This could be everything from how to get in touch to your business hours to your social media accounts. To avoid having to add the same content to a paragraph block every time you want to place it at the end of your post, you can make it a Synced pattern.

### Repeated structure across your site

For anything that’s more about site structure that’s repeated across your site, like a Header or Footer, it’s best to use a template part. These are intended for structural elements in a block theme, so it’s important to distinguish them from patterns.

### Repeated design or layout

When it’s less about content and more about wanting to repeat a design or layout, patterns are best to use. This is because the content doesn’t need to be synced and, instead, what you want repeated is how something visually looks.

## Changelog

-   Updated 2023-08-08
    -   WP 6.3 introduced custom patterns, and Reusable Block was renamed to Synced Pattern.
