---
title: VAR To Keep It Simple
slug: var-to-keep-it-simple
date: '2008-03-27T05:57:36'
updated: '2008-03-27T05:57:36'
draft: false
tags:
- .NET
- Personal
author: Sean Feldman
---


Among various things in C# 3.0, one of the syntactical sweets that I find quiet useful is the 'var' keyword. Combined with R# intelligence, you create a very readable code that is not cluttered with excessive type reminders. Just enough to keep it strongly typed and readable.

Personally, I favor:

```
var people = new Dictionary<string, IPerson>();
```

over:

```
Dictionary<string, IPerson> people = new Dictionary<string, IPerson>();
```

