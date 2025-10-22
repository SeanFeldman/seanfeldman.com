---
title: Using NuGet without committing packages to source control
slug: using-nuget-without-committing-packages-to-source-control
date: '2011-10-16T13:05:00'
updated: '2011-10-16T13:05:00'
draft: false
author: Sean Feldman
---


I am catching up on NuGet and learning a few good things. A project should be in buildable state once you pull it from the repository. This is always my goal with the projects I work on. Therefore, one of the requirements that I always set was to have “autonomous” project – everything included within the project itself (libraries, tools, etc.). Some exceptions would be things that don’t make sense to commit and rather have them installed on all machines (OS, Server apps, SDKs, etc.).

With NuGet, my initial approach was always to commit the packages. Then why would someone commit a package that is already sitting on NuGet.org and can be easily fetched from there without trashing my company's repository per each project with probably the same libraries used across multiple projects. I needed [a way to use NuGet w/o committing packages to source control](http://docs.nuget.org/docs/workflows/using-nuget-without-committing-packages). And it’s there! NuGetPowerTools does it in a great way. It modifies project files to verify that components brought through NuGet still present, and if they don’t, instructs to fetch them locally.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/Using-NuGet-without-committing-packages-_D9C/image_thumb.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/Using-NuGet-without-committing-packages-_D9C/image_2.png)

So the next time projects compile, it only checks for packages, but doesn’t pull them down as they already exist.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/Using-NuGet-without-committing-packages-_D9C/image_thumb_1.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/Using-NuGet-without-committing-packages-_D9C/image_4.png)

Since it rely on project files, it doesn’t matter if your first compilation takes place in Visual Studio on command line, both will work. For Visual studio it will fix the missing assemblies referenced in project issue.

Love it!

2011-12-29: Simpler approach is described [here](http://docs.nuget.org/docs/workflows/using-nuget-without-committing-packages).


