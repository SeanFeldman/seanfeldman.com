---
title: Simple MVVM Walkthrough – Refactored–Part 2
slug: simple-mvvm-walkthrough-refactored-part-2
date: '2011-01-13T03:13:21'
updated: '2011-01-13T03:13:21'
draft: false
author: Sean Feldman
---


In the [previous post](http://weblogs.asp.net/sfeldman/archive/2011/01/12/simple-mvvm-walkthrough-refactored.aspx) I showed an attempt to get rid of the magical strings. It worked great for a string property, but failed for the integer one as JR has reported. I decided to look into that, but this time around through TDD and this is what I found (besides the fact that going TDD way would definitely catch it).

When a string property is passed in, returned object is expected therefore there’s nothing complicated, it works. Though, when an integer (or any other type that is not a string) is passed in, .NET implicitly applies Convert() method.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_0A3E2908.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_24125F37.png)[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_2CB2B7C3.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_0965C31E.png)

Therefore the code should be update:

```
class PropertyOf<T>
  {
```
public static string Resolve(Expression&lt;Func&lt;T, object&gt;&gt; expression)
{
  Expression candidate = null;
```
```
if (expression.Body is UnaryExpression)
    candidate = (expression.Body as UnaryExpression).Operand;
```
```
if (expression.Body is MemberExpression)
    candidate = expression.Body;
```
```
return (candidate as MemberExpression).Member.Name;
}
```
}
```

Tests are quite simple:

```
    [Observation]
```
public void Should_return_integer_property_name_as_is_within_the_containing_class()
{
  PropertyOf&lt;Dummy&gt;.Resolve(x =&gt; x.IntegerProperty).Should_Be_Equal_To("IntegerProperty");
}
```
```
[Observation]
public void Should_return_string_property_name_as_is_within_the_containing_class()
{
  PropertyOf&lt;Dummy&gt;.Resolve(x =&gt; x.StringProperty).Should_Be_Equal_To("StringProperty");
}
```
```
private class Dummy
{
  public int IntegerProperty { get; set; }
  public string StringProperty { get; set; }
}</pre></div>
```

```

