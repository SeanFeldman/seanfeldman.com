---
title: Moq with NameValueCollection
slug: moq-with-indexer
date: '2012-01-11T21:49:00'
updated: '2012-01-11T21:49:00'
draft: false
tags:
- C#
- TDD
author: Sean Feldman
---


Mocking HttpRequest and HttpResponse is not complicated with HttpRequestBase and HttpResponseBase introduced in ASP.NET. I had to mock ServerVariables property of HttpRequest and run into an issue – I was accessing an indexer property and didn’t know how to do this. Gladly, ran into a post that mentioned that indexer is actually utilizing a virtual Get() method. Reflector has confirmed that.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_2427F3FD.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_305993F1.png)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_4FF847EC.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_5F0F26C6.png)

Great! Now indexer can be mocked.


