---
title: Assembly in GAC and Configuration File
slug: assembly-in-gac-and-configuration-file
date: '2010-07-03T23:43:00'
updated: '2010-07-03T23:43:00'
draft: false
tags:
- .NET
- BizTalk
author: Sean Feldman
---


Working with BizTalk pushes the creativity sometimes. This time around, I needed to have an assembly deployed to GAC (so that BizTalk application can easily use it) and at the same time being able to configure this assembly without re-deploying it to GAC again.

Normally, an assembly has a configuration file (.config) that is bundled with assembly and serve as it name indicates. With GAC it’s different. Regardless of [method of deployment](http://msdn.microsoft.com/en-us/library/ex0ss12c%28VS.80%29.aspx) into GAC, it only accepts an assembly file, nothing else. This is where shared knowledge and creativity kick in.

How assembly is **actually** deployed?

GAC is file based structure typically located at **%windir%\assembly**. If you type the location in Explorer, this is how it looks like:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_60B4AE94.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_37AA0F98.png)

You can’t drill in, unless you specify another path that exposes GAC as file system, **%windir%\assembly\gac\_msil**. This opens the actual file structure of GAC, which is structured very logically.

Assume you have deployed an assembly called zUtility with version 1.0.0.0. Once this assembly is deployed into GAC, a folder is created with named as the assembly, and inside another sub-folder, named accordingly as the version and public key token of the assembly. Inside that folder zUtility assembly is found. This way GAC can contain multiple versions of the same assembly.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_652DC00C.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_42D62A93.png)

This should technically allow us to drop the configuration file and have it loaded by assembly once it’s used. But no, it’s not working that way. Even without GAC, a satellite assembly is always using configuration file of the main assembly. It would be nice if it was using it’s own configuration file first, but it doesn’t. Either way, back to our case. Solution for this problem would be to “force” reading of configuration file through custom code.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_4676D621.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_7293D312.png)

Executing assembly location is full path and name of zUtility.dll. Appended to that .config gives us the configuration file full path and name. The rest is usual.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_0C9B2CE7.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_0A5EA42B.png)

Now BizTalk can reference a fully configurable assembly deployed to GAC **without** being redeployed every single time we need to update a connection string, or a URL or some constant value. Hard-coding is bad, so avoid it.


