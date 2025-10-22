---
title: 'BizTalk Project: AssemblyInfo Issue'
slug: biztalk-project-assemblyinfo-issue
date: '2010-03-16T17:37:00'
updated: '2010-03-16T17:37:00'
draft: false
tags:
- BizTalk
author: Sean Feldman
---


Every new BizTalk project has the next line in AssemblyInfo.cs file:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_30385942.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_5C555633.png)

The only way I could solve it was to instruct R# to ignore this error.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_42177DC0.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_3927EB81.png)

Has anyone dealt with it differently?


