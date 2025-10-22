---
title: Cloud Services - Cached Version of Asseblies
slug: cloud-services-cached-version-of-asseblies
date: '2016-04-15T05:43:00'
updated: '2016-04-15T05:43:34.765264+00:00'
draft: false
tags:
- .NET
author: Sean Feldman
---
Today have run into an interesting issue: a cloud service deployed with a 3rd party assembly version X was failing. The exception was indicating that version X-1 of the assembly was deployed. Looking at the project packages.config could see nothing but version X of the assembly. Quite a mystery.

After scratching my head, I couldn't think of anything other than a wrong version of the assembly being deployed. But how?! The version of the NuGet package is right. Deployment takes whatever the package is providing. What could it be, a cached assembly file? Hmmm, I'd think that rebuild would wipe the output.

Either way, to resolve the mystery and identify the version of the *actually* deployed assembly, here's a trivial code to run.

```csharp
var type = typeof(SomeClass)
logger.Log(FileVersionInfo.GetVersionInfo(type.Assembly.Location).ProductVersion);
```
I'm still not sure how did that happen, but looks like CSes packaging/deployment can be affected by the cache.
