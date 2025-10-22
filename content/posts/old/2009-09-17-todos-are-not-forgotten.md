---
title: TODOs are not forgotten
slug: todos-are-not-forgotten
date: '2009-09-17T17:13:00'
updated: '2009-09-17T17:13:00'
draft: false
tags:
- Agile
author: Sean Feldman
---


We are using Hudson as a build server, and one of the lasts steps that were taken is to mark a build as ‘unstable’ when we pass a certain number of TODO comments in our code (an arbitrary number). While I am not a 100% sold on a number, I think it’s a good way of insuring things are not just marked and forgotten. Actually, we are not even tracking TODOs, but BROKEN\_WINDOW comments, as those are definitely bad. Failing on HACK is another possibility. Visualization plays a significant role in my case (interpretation of things based on visualization), and here how it looks (green is all good, yellow is all passed, but number of comments has exceeded the limit).

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_3ED0DC1D.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_1C7946A4.png)


