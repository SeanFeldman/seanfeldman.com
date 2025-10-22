---
title: Right Tool for the Right Job - Part 2
slug: right-tool-for-the-right-job-part-2
date: '2009-02-08T17:16:34'
updated: '2009-02-08T17:16:34'
draft: false
tags:
- VS.NET
author: Sean Feldman
---


In the [previous post](http://weblogs.asp.net/sfeldman/archive/2009/02/04/right-tool-for-the-right-job.aspx) I talked about running test in Resharper vs. TestDriven.NET

This time I will compare Visual Studio .NET 2008 (VS) with TestDriven.NET (TD.NET) for another functionality - quick code execution for evaluation purposes.

VS was shipped with a feature called Object Test Bench. The idea was to be able to instantiate an object of a class in order to execute it's methods for quick evaluation. Great idea. The steps to have it going were multiple.

Step 1 - Open Object Test Bench

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_2.png)

Step 2 - Class View

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_1.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_4.png)

Right click on the class

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_2.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_6.png)

Step 3 - Create Instance

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_3.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_8.png)

This will create the temporary object in Object Test Bench space.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_4.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_10.png)

Step 4 - Invoking Method

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_5.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_12.png)

Step 5 - Getting Result

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_6.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_14.png)

Step 6 - Finalizing

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_7.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_16.png)

Note: to see the result stored under string1, you have to mouse over.

Not the same thing with TD.NET

Step 1 - Point to the method to invoke

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_8.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_18.png)

Step 2 - See the result

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_thumb_9.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/RightToolfortheRightJobPart2_145B6/image_20.png)

Don't know what about you, but for me it's an obvious difference. Multiple steps in VS vs. single\* step in TD.NET. Thanks David for showing this one.

So the right tool for the right job. Do you have any samples? Show it! Heck, why just to limit ourselves with VS only. We can do more than that. How about replacing RDBS with OODBS as the right tool? Sky is the limit.

\* If you set your VS to show Output window automatically, it will popup on it's own. Otherwise that will be 2 step process. Still ALT-V, O should make it a step and a half :)


