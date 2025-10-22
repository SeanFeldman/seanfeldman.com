---
title: Mock Implementing Multiple Interfaces
slug: mock-implementing-multiple-interfaces
date: '2009-12-26T01:16:00'
updated: '2009-12-26T01:16:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


One of the recent tests I had, I had to deal with the fact that a dependency object injected into *system under test* object will be casted to some other interface (known to be implemented) and used. [Moq](http://code.google.com/) has some documentation on it, but it was a bit misleading. QuickStart wiki showed an example below:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_3B396B62.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_2B96CFA0.png) From example it is a bit difficult to see that once *foo* is marked *As<IDisposable>*, it can be casted in production code to *IDisposable*. This is a **very** helpful feature in Moq.


