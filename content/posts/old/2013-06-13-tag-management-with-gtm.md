---
title: Tag Management With GTM
slug: tag-management-with-gtm
date: '2013-06-13T03:37:00'
updated: '2013-06-13T03:37:00'
draft: false
tags:
- Patterns
author: Sean Feldman
---

## What is a tag?

In the marketing world tag (or pixel) is used for tracking purposes. Historically it was based on a call to retrieve a 1x1 transparent image. Rational behind this was to retrieve client side information of a site visitor on a 3rd party server. Information would include browser standard information including cookies. There’s a lot of things that can be done with this information from analytical and marketing point of view.

## Why is is so Messy?

Tracking and conversion tags (pixels) were supposed to be “add-ons” that any non-technical web master (and later “business user”) should be able to drop into mark-up and be done. After a little bit information flows into tag vendor server and reports are available. But it is not as simple as it sounds when you need to work with *multiple* tag vendors. Imagine following scenarios.

Scenario 1:

> We need to know how many unique visits we had to a page X.

Scenario 2:

> We need to count how many times visitors clicked a button Y.

For scenario #1, traditionally it is achieved by adding a tag to the HTML. Something like

```

   1: ![](http://vendor/tag.jpg?client=id&page=code)

```

For scenario #2, again, traditionally it is as “simple” as embedding code into onclick event

```

   1: 

```

It’s almost good, except mixed concerns and need to constantly change. In the marketing world, tags come and go. And it happens frequently. And with multiple vendors. Therefore you end up with a few issues doubled (when tag is added and removed), multiplied by number of vendors.

1. Constant need to modify mark-up
2. Constant need to modify client side code (JavaScript handlers)
3. Constant need to deploy changes
4. Mixing of concerns (marketing vs. development)

## What’s a Solution?

Separation of Concerns. Tags are not needed for markup and client side code. Developers and designers shouldn’t be concerned with those. Marketers should (well, ideally at least). In order to achieve that, tags should be **placed and managed** **separately from markup and code**. This is where Tag Management tools are handy.

A tool I have tried so far was [Google Tag Manager](http://www.google.com/tagmanager/) (or just GTM) and it works great for these kind of things.

## How Tag Management Helps?

These are a few things that GTM does for you:

1. Takes tags code and markup out of your markup and code and by that makes it clean and lean
2. Injects tags dynamically based on rules execution
3. Allows to manage rules and tags outside of your main solution
4. Versioning by marketers – a very strong feature
5. Publishing\* of a specific version
6. Preview and debugging to ensure things work before get published
7. Ability to add/remove tags w/o main site re-deployment
8. and more…

\* Publishing that is happening within GTM, no connection to your main markup/code publishing

## How Simple it is?

Simple. There’s really not that much to it, but once you utilize the power, you’ll not go back again to embedding tags in markup/code ever again.

Another benefit is integration. If you use Google Analytics, you can easily integrate that one (another cross-cutting concern is removed from you markup).

## Are there Alternatives?

Plenty. Google is not the pioneer in this area, and the tool is far from perfect. Lots of other companies have offerings that are good and viable solutions. We found GTM to be simple, clean, and cost effective (free for now) to address our requirements.


