---
title: Hudson – CI Engine (part 2)
slug: hudson-ci-engine-part-2
date: '2009-04-20T04:05:00'
updated: '2009-04-20T04:05:00'
draft: false
author: Sean Feldman
---


In my [previous blog](http://weblogs.asp.net/sfeldman/archive/2009/03/25/hudson-ci-engine.aspx) about [Hudson](https://hudson.dev.java.net/) I was excited as a user how cool and great this CI engine was. This week I had to quickly setup a project and get it going on our build server. Boy oh boy, that was great task. Easy, clean, and fast. You should definitely check it out.

For those who want to install it, keep in mind the next:

1. You will have to install Java Runtime
2. Once you can run the command line version, you can through the browser install the windows service (a much better way of running CI server)
3. You probably will need a few .NET related plugins to install prior to setting up any projects, such as
   1. MSBuild (if you use it)
   2. NAnt (if this is your build script of choice)
   3. Gallio report builder (if you use MbUnit 3.x)
   4. Green Balls (if you rather see red-green and not red-blue – why blue?!)

The nice part is that the information is all available at the Hudson site, and very easy to find.

Oh, and [Terry](http://www.connicus.com/), why won’t you blog about setting it up for the .NET community. Folks would love to read it :P

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_101BAB2F.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_19E112A7.png)

**Update:** this blog [post](http://redsolo.blogspot.com/2008/04/guide-to-building-net-projects-using.html) is a nice detailed step-through guide how to setup and run Hudson. Uses NUnit, but not a big issue to convert to anything you need.


