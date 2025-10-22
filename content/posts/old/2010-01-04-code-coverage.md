---
title: Code Coverage
slug: code-coverage
date: '2010-01-04T06:36:00'
updated: '2010-01-04T06:36:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


We are a TDD shop, or BDD to be more accurate. Normally we leverage Hudson Test Result Trend to see how things are doing. The project is a Windows NT Service. This is how Test trend looks like:

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_36A24981.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_749BDA3F.png)

I wanted to take the current project and to run code coverage on it, to see if our approach is still holding and how things look like. It was around 90%, and with a few missing specs results were quite good:

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_67C414D2.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_71897C4A.png)

A few things that I have observed and have to be mentioned:

1. Small projects are easy to keep under control.

2. It is difficult to get to 100% – is there a need at all? Don’t think so.

3. Having no UI to test does make things look a lot better.

4. Without code coverage things still can be done properly. Yet, it is nice to have statistics.

5. Some of the web stuff .NET has is too kinky to test properly, but it’s possible.

As for the Coverage tools – I’ve used trial version of [NCover](http://www.ncover.com/) and a college of mine used [PartCover](http://sourceforge.net/projects/partcover). Are there any alternatives? Recommendations?


