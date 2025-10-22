---
title: Syntactic Sugar
slug: syntactic-sugar
date: '2009-12-07T04:44:00'
updated: '2009-12-07T04:44:00'
draft: false
tags:
- .NET
- C#
author: Sean Feldman
---


![clip_image002](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image002_thumb_1E523610.jpg "clip_image002")

Well, I wish there was a way of getting away from *SyntaticSugar* static class initial point, and be able just to do plain code

```

Do(() => request.Headers = Headers).If(HeadersExist);

```

Or even better, this

```

(request.Headers = Headers).If(HeadersExist);

```
There’s always hope for next version of C# ;)
