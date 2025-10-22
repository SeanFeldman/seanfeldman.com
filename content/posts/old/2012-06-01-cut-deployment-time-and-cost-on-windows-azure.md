---
title: Cut Deployment Time and Cost on Windows Azure
slug: cut-deployment-time-and-cost-on-windows-azure
date: '2012-06-01T07:55:00'
updated: '2012-06-01T07:55:00'
draft: false
tags:
- Automation
- Cloud
- PowerShell
author: Sean Feldman
---


I’m new to Windows Azure, and learning by making mistakes. There’s a lot to learn about Azure in general, and one of the interesting aspects is deployments and cost associated with it. Taking this moment, I’d like to thank [Yves Goeleven](http://cloudshaper.wordpress.com/), Azure MVP, who has helped me a lot.

The simplest deployment that can be done is either directly from Visual Studio .NET. But it’s not automated, and requires a person to trigger it. Next option is to automate it with PowerShell scripts, leveraging [Windows Azure PowerShell Cmdlet](https://wappowershell.codeplex.com). But you have to ask yourself, what am I deploying EVERY SINGLE TIME?

When deployed for the first time, I was horrified – 30MB package. Goodness, no wonder it takes forever. “Azure sucks” was my immediate diagnosis. Wait a second, does it? Hmmm… Something tells me it’s not the Azure that sucks. Let’s analyze it. I have several 3rd party dependencies which contributed over 7MB in assemblies. Wow, that’s a lot. Now for each role (and I have two – web and worker roles) that is 7MB x 2 = 14MB. Heavy, don’t you think?

Solution is simple – Startup Task. Azure supports [Startup tasks](http://msdn.microsoft.com/en-us/library/windowsazure/gg456327.aspx), which is a very powerful concept. You have an option to operate on the machine instance or a role is deployed to, prior to the role execution. This is great, because I can fetch my 3rd party dependencies just before role instance is started, ensuring all dependencies are in place. Where from though? Azure storage. When you deploy your package, you deploy it to the Azure Storage anyways, so why not to upload a zipped blob with your dependencies once, and fetch it every time? This will save you the cost of uploading for **every single deployment** you do. Event better – when on the same data centre, you don’t pay for moving data. So not only your packages are smaller, shorter deployment time (upload part), but also you save on storage transactions, translated into money saving.

I have gone through this exercise with the dependency I had – NServiceBus, once just for worker role, and then for web role as well, and results are quite impressive as you can see. From 30MB deployment down to 11MB.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_01786D64.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_6EA3E9B9.png)

Dependencies need to be packaged and uploaded either manually, or scripted as a part of build process upon dependencies version change. Therefore I’d suggest to evaluate which dependencies can follow this path and which cannot. You don’t have to stop on 3rd party only, and can also apply the same to Microsoft Azure assemblies, since those eat up space as well, and are found in every role you deploy.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_3DE0BC41.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_30E6DC30.png)

And once you do that, well, you are down to the minimum of your project generated artefacts.

I have an idea of creating a “Dependencies Start-Up Task” NuGet package that would take away boiler platting away and allow you to achieve this task with less effort. Would you consider it to be useful? Let me know your opinion, and, perhaps, a few bits will be spared and NuGet be less spammed.


