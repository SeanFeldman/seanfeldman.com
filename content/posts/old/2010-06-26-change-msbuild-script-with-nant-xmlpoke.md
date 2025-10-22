---
title: Change MsBuild Script with NAnt XmlPoke
slug: change-msbuild-script-with-nant-xmlpoke
date: '2010-06-26T03:48:00'
updated: '2010-06-26T03:48:00'
draft: false
tags:
- BizTalk
author: Sean Feldman
---


For [automated deployments of BizTalk application](http://weblogs.asp.net/sfeldman/archive/2010/06/22/automated-builds-and-deployment-for-biztalk.aspx), I am using MsBuild scripts packaged with compiled BizTalk artifacts. Build scripts are in NAnt. I wanted from NAnt build script to update MsBuild deployment script.

MsBuild deployment script looked like this:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_208D0D40.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_63D584AF.png)

For this task NAnt XmlPoke is the right tool to use, except that this didn’t work, until I realized that I need to use namespace prefix. Once prefix ***msb*** was in place, it worked as charm.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_08F7F07E.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_5E1CFBBA.png)


