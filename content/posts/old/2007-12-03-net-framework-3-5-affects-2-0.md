---
title: .NET Framework 3.5 Affects 2.0
slug: net-framework-3-5-affects-2-0
date: '2007-12-03T19:34:00'
updated: '2007-12-03T19:34:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


I have installed .NET Framework 3.5 along with already existing 2.0 as a part of Visual Studio .NET 2008 installation. What a surprise it was to find out that the old "web site" projects were all broken... after a few hours of investigation, my coworker, Glen and I have found that the 3.5 is not so [innocent](http://blog.pantos.name/archive/2007/09/27/.net-framework-3.5-breaks-asp.net-2.0-web-sites.aspx) and  it writes to 2.0 new version of assemblies. Why in the world it would do it?! So far this is under MS engineers investigation and I hope it was an error on our side.

And this KB can be useful for some people as well: [KB941824](http://support.microsoft.com/kb/941824) - at the 'cause' section, in little font I loved the note: "*When you install the .NET Framework 3.5, the .NET Framework files in the V2.0.50727 folder are updated. Therefore, when you install the .NET Framework 3.5, Visual Studio 2005 is affected.*"  Great...

2007-11-28 21:25 Update: a quick example of breaking code is attached in zip file. The problem is in RuntimeMasterPageFile property at compile time. [Issue20071128.zip](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/Issue20071128.zip)

2007-11-30 00:15  Update: after recreating the whole environment step by step I reproduced the issue and seems like the breaking change is in web.config under  system.web section - one of the configurations, <page> has an attribute pageBaseType that I was using and didn't have to specify anything on each single page. After 3.5 install, which is also a SP1 for 2.0, this feature is no longer respected by compiler. Keep tuned for updates.

2007-12-03 Update: ASP.NET team confirms that this is a bug in 3.5  (2.0 SP1) and they will release a hotfix within up to 4 weeks.

2008-03-05 Update: The fix was built, but failed one of MS internal test stages. Therefore, they have moved it back to the previous stage for rebuilding. Updates on the status will be posted as that process continues.  



