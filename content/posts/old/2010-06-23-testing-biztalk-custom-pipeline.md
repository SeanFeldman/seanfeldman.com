---
title: Testing BizTalk Custom Pipeline
slug: testing-biztalk-custom-pipeline
date: '2010-06-23T20:54:00'
updated: '2010-06-23T20:54:00'
draft: false
tags:
- BizTalk
- TDD
author: Sean Feldman
---


There are a few ways to test BizTalk Custom Pipelines out there. If you want automatically execute pipeline on input and verify it’s not exploding, you can leverage *TestableSendPipeline* coming along with BT projects.

A few things that are required for this to work:

1. Enable unit testing on the BT project

[![000](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/000_thumb_49CBE661.png "000")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/000_7ACB970E.png)

2. Include PipelineObjects.dll assembly found at %programfiles%\Microsoft BizTalk Server 2009\SDK\Utilities\PipelineTools into your project and reference it from your test project along with other BT assemblies.

[![001](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/001_thumb_697D50DA.png "001")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/001_79898EE0.png)

3. Create your spec (test) that would exercise the pipeline.

[![002](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/002_thumb_23FAE160.png "002")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/002_51E5A367.png) Note: the funky path thing is because is for loading input file properly when test is executed with TestDriven.NET in Visual Studio .NET, as well as when executed by Gallio as a part of automated build script. File has to be copied to the output for this to work.

[![003](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/003_thumb_611E9CE5.png "003")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/003_061C5D5F.png)

As a result – pipeline is testable and any change to an input sample document will re-kick testing that will fail if something is not addressed they way it was designed before the change took place.

[![004](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/004_thumb_3AE164EF.png "004")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/004_0309FF6A.png)

**Now, if only I could figure out how in the world to get hold of the output…**


