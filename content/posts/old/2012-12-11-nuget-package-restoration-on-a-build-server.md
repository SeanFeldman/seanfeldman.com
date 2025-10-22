---
title: Nuget Package Restoration on a Build Server
slug: nuget-package-restoration-on-a-build-server
date: '2012-12-11T18:52:00'
updated: '2012-12-11T18:52:00'
draft: false
tags:
- Automation
- Tools
author: Sean Feldman
---


One of our latest projects has failed to restore nuget packages on the build server. Error message was

> Package restore is disabled by default. To give consent, open the Visual Studio Options dialog, click on Package Manager node and check 'Allow NuGet to download missing packages during build.' You can also give consent by setting the environment variable 'EnableNuGetPackageRestore' to 'true'.

I have looked into options, and was surprised that default way to handle it was

> * Go to your build server (rdp or physical)
> * Start Visual Studio

While this is acceptable for a local development, for a build server this is a big red light right there. Gladly, as pointed out in this [blog post](http://blog.deltacode.be/2012/07/10/nuget-package-restore-fails-on-tfs-build-server/), there’s an option of setting a system variable to solve the issue.

Would be nice to see nuget default to system variable, and then fallback to an instance of VS on a server, but not the way around.


