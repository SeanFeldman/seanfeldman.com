---
title: Re-inventing Wheel
slug: re-inventing-wheel
date: '2008-08-14T05:35:20'
updated: '2008-08-14T05:35:20'
draft: false
tags:
- .NET
- TDD
author: Sean Feldman
---


It doesn't matter how much we try to avoid it, it is unavoidable. Re-inventing wheel phenomena is always going to take place here and there. Doing a little BDD tests made it clear that I need to mark and specification with the type of the the system under tests I am testing, or the *Concern* of the test. One way I was showed to do it was to introduce a custom ConcernAttribute and mark with it the TestFixute - specification. Code looks like this:

```

   1:    public class ConcernAttribute : Attribute
   2:    {
   3:      public Type SystemUnderTestType { get; private set; }
   4:      public string Message { get; private set; }
   5:
   6:      public ConcernAttribute(Type systemUnderTestType, string message)
   7:      {
   8:        SystemUnderTestType = systemUnderTestType;
   9:        Message = message;
  10:      }
  11:
  12:      public ConcernAttribute(Type systemUnderTestType) : this(systemUnderTestType, string.Empty) {}
  13:    }

```

Not the smartest code in the world, but does it's work:

```
  [Concern(typeof(CurrencyConverter))]
  [TestFixture]
  public class when_bla_bla_bla

```

Apperently, MbUnit creators have had this idea before, and where kind enough to create an attribute for this purpose - TestsOnAttribute:

```
  [TestsOn(typeof(CurrencyConverter))]
  [TestFixture]
  public class when_bla_bla_bla
```

Wheel re-invention :)

Now why would you prefer to use the original wheel? Well, personally just to save this step from occurring each time...

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/ReinventingWheel_14A0A/image_thumb_1.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/ReinventingWheel_14A0A/image_4.png)


