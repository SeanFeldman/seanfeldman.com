---
title: Testing Challenge – Silverlight
slug: testing-challenge-silverlight
date: '2010-09-08T16:43:00'
updated: '2010-09-08T16:43:00'
draft: false
tags:
- Silverlight
- TDD
author: Sean Feldman
---


I am getting involved in another project, that looks like has its own testing challenges (last project I was involved was a BizTalk based project, quite a few testing challenges!).

What have I seen so far with Silverlight (version 4.0):

1. TDD with the toolset we always utilized is no longer possible (Gallio, TestDriven.NET, NCover) partially due to the nature of Silverlight, partially because of the tools support that is not yet in place
2. MVVM pattern – developers wrapping around the idea
3. Explosion of Microsoft technologies that are just “out of college” and not yet applicable in TDD case
4. Limited resources on .NET code detours (I only encountered Moles and TypeMock, but for commercial Silverlight product both are commercial)
5. Natural limitations of Silverlight (sandbox, static DependencyObject properties, inheritance from the system)

Looks like this is going to be an interesting journey. Feel free to share your experiences and findings.


