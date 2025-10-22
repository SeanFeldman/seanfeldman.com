---
title: Azure and Open Source Software
slug: Azure-and-Open-Source-Software
date: '2016-03-02T05:46:00'
updated: '2016-03-02T16:21:11.392473+00:00'
draft: false
author: Sean Feldman
---
Not so long ago Microsoft made a deliberate choice to play the OSS game, and it was quite a welcomed change. Rome wasn't built in a day. So it this initiative. It's a long and bumpy way. Along the way we all, maintainers and contributors, learn along.
While working on some Azure Storage related code with one of the WesternDevs, [Don Belcham](http://www.igloocoder.com/), we've run into a [bug](https://github.com/Azure/azure-storage-net/issues/232) in CloudBlockBlob functionality to acquire a lease. In the old version of storage library, the lease could be up to 90 seconds, wherein the later version it was truncated to 60 seconds maximum.
Usually, this would be a tedious process of reporting the bug, providing a sample to reproduce it and... waiting. But this wasn't the case as Storage library code is on [GitHub](https://github.com/Azure/azure-storage-net). A win!
Fixing the code was straight forward. And this is the part where I'd like to see MSFT (and other maintainers) to be a bit friendlier to its contributors.
1. Maintainers know their project inside out, contributors don't. When asking to update documentation, specific files, other concrete files, provide links to those resources. Don't force contributors to sweat searching for those and giving up just because they couldn't find a file like "changelog".
2. Automate your testing/validations. If automation is not in place, provide guidance on how to perform the task and achieve the goal. Ideally, document the steps.
Imagine this comment:
![enter image description here][1]
Being a little more helpful with a few links and crisper requirements:
![enter image description here][2]
Guiding contributors and making sure they have all the information needed to make that PR as easy as possible makes a huge difference. This is how one can go from "What did I think when started this" to "I made a change and feel great about contributing". One day we'll get there. Until then, do the little things to encourage people to make those PRs.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/azure-and-oss-comment-1.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/azure-and-oss-comment-2.png
