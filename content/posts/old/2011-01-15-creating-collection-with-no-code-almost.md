---
title: Creating collection with no code (almost)
slug: creating-collection-with-no-code-almost
date: '2011-01-15T05:56:00'
updated: '2011-01-15T05:56:00'
draft: false
tags:
- C#
author: Sean Feldman
---


When doing testing, I tend to create an object mother for the items generated multiple times for specifications. Quite often these objects need to be a part of a collection. A neat way to do so is to leverage .NET params mechanism:

```
    public static IEnumerable<T> CreateCollection<T>(params T[] items)
```
{
  return items;
}</pre></div>
```

And usage is the following:

```
private static IEnumerable<IPAddress> addresses = CreateCollection(new IPAddress(123456789), new IPAddress(987654321));
```

```

