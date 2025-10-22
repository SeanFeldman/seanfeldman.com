---
title: C# 3.0 Auto Property And NHibernate
slug: c-3-0-auto-property-and-nhibernate
date: '2008-03-01T03:45:14'
updated: '2008-03-01T03:45:14'
draft: false
tags:
- .NET
author: Sean Feldman
---


I was reading about NHibernate mapping of the properties that have no setter, and how it's done through the backing field (reflection I assume). The setting looks like this:

```

access="nosetter.camelcase-underscore"
      column="name" type="string" length="20" />
```

And then I got curious what would be that with the new C# 3.0 auto properties.

As a test I made a simple class with a simple string property that looks like this:

```

```
private string test;
  public string Test
  {
    get { return test; }
    private set { test = value; }
  }
```

```

And with auto property this looks much sexier:

```
      public string Test { get; set; }
```

But what about backing field? Reflector shows the next:

```

```
[CompilerGenerated]
private string <Test>k__BackingField;
```
```
public string Test
{
     [CompilerGenerated] get;
     private[CompilerGenerated] set;
}
```
t

```

Now I was wandering how  that should be communicated in the mapper file for NHibernate?... Googled.... nothing. Any ideas?


