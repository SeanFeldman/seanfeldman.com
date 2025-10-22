---
title: JavaScript Unit Testing
slug: javascript-unit-testing
date: '2011-09-30T15:34:00'
updated: '2011-09-30T15:34:00'
draft: false
tags:
- CI
- TDD
author: Sean Feldman
---


Recent announcements for Windows 8 development is not including JavaScript with HTML5 has opened up Windows development for more developers. I wanted to see where testing for JavaScript is standing and was surprised at the variety of frameworks out there. Back in the days when I was trying to do web testing with WatiN, it was painful, especially when a browser had to be loaded for those tests. My interest was around JavaScript testing w/o need to load a browser. [QUnit](http://docs.jquery.com/Qunit) looked very good, but it still required an actual browser. Also, in a CI scenario, I wanted to be able to use a command line/tool execution style.

I have ran into [Chutzpah](http://chutzpah.codeplex.com/) test runner. Great wrapper for QUnit executing w/o need for a browser. More than that, it doesn’t require that standard QUnit shell HTML file for output, which makes tests execution simple and straight forward – execute command line test runner on the scripts folder.

Successful tests execution

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_40202C15.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_39D95587.png)

Failed tests execution

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_57D7637B.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_466702A3.png)

This is perfect! Not only runs w/o browser, but also nicely fits to run with CI on a server.

The test runner also comes with a Visual Studio addin to run JavaScripts tests within IDE.

This is the one that I found that nailed it for what I needed. Are there other tools that can do the same and more?


