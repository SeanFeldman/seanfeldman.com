---
title: Make it simple. Make it work.
slug: make-it-simple-make-it-work
date: '2014-05-15T02:26:00'
updated: '2014-05-15T02:26:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


In 2010 I had an experience to work for a business that had lots of challenges.

One of those challenges was luck of technical architecture and business value recognition which translated in spending enormous amount of manpower and money on creating C++ solutions for desktop client w/o using .NET to minimize “footprint” (2#) of the client application in deployment environments. This was an awkward experience, considering that C++ custom code was created from scratch to make clients talk to .NET backend while simple having .NET as a dependency would cut time to market by at least 50% (and I’m downplaying the estimate). Regardless, recent Microsoft announcement about .NET vNext has reminded me that experience and how short sighted architecture at that company was. Investment made into making C++ client that cannot be maintained internally by team due to it’s specialization in .NET have created a situation where code to maintain will be more brutal over the time and  number of developers understanding it will be going and shrinking. Not only that. The ability to go cross-platform (#3) and performance achievement gained with native compilation (#1) would be an immediate pay back.

Why am I saying all this? To make a simple point to myself and remind again – when working on a product that needs to get to the market, make it simple, make it work, and then see how technology is changing and how you can adopt. Simplicity will not let you down. But a complex solution will always do.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_07D99C9E.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_3B7CE79A.png)


