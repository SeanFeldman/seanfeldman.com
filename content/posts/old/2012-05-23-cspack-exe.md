---
title: CSPACK.EXE - Careful with Defaults
slug: cspack-exe
date: '2012-05-23T03:37:00'
updated: '2012-05-23T03:37:00'
draft: false
tags:
- Cloud
author: Sean Feldman
---


When packaging Windows Azure solution from within Visual Studio .NET 2010, CSPACK is generating cspackproperties file behind the scenes, **defaulting to .NET 3.5 Framework**. I missed that part when going over the [documentation](http://msdn.microsoft.com/en-us/library/windowsazure/gg432988.aspx) and had to go through the worker role that can’t starts and no error is logged, since worker never loads. Gladly, [solution](http://social.msdn.microsoft.com/Forums/en-US/windowsazuredevelopment/thread/0e7a89ba-53af-4c0f-a991-1bea69f5ff5f) is trivial and so old that is probably long time forgotten by the Azure veterans. But for newbies like myself, don’t dismiss [old material](https://channel9.msdn.com/Shows/Cloud+Cover/Cloud-Cover-Episode-29-Working-with-CSPack), even if it’s from 2010.  Nothing New Under the Sky…


