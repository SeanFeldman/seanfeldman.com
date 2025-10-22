---
title: Building AssemblyInfo for BizTalk with NAnt
slug: building-assemblyinfo-for-biztalk-with-nant
date: '2010-06-30T15:44:00'
updated: '2010-06-30T15:44:00'
draft: false
tags:
- .NET
- BizTalk
author: Sean Feldman
---


All assemblies deployed into production are versioned. My personal preference[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_382E5738.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_1AB9757B.png) is to achieve that with build scripts, ensuring that build number, code revision, minor and major versions are all inserted. AssemblyInfo.cs is the file that normally contains that information. I normally generate a dummy AssemblyInfo file in the build project and reference that from the project(s). This way, when building with scripts, we can generate dynamic AssemblyInfo.cs file and overwrite the link. The link is a one way link, nothing is updated in the build project. And since link is just a reference, nothing is modified from the repository point of view. NAnt has <asmInfo> task that does all the job. Except that for BizTalk its not straight forward process (of course, how could it be).

With BizTalk projects, there’s one assembly attribute that doesn’t have an empty constructor, and as a result of that <asmInfo> task fails.

*<attribute type="Microsoft.XLANGs.BaseTypes.BizTalkAssemblyAttribute" value="typeof(BTXService)" />*

Workaround for this is simple. Use <asmInfo> to generate everything but this attribute. Use <echo> to generate this attribute. No headache, simple and working.

> [![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_16C2823F.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_1C0ED83F.png)


