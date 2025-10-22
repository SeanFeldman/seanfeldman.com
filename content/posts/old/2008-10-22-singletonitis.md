---
title: Singletonitis
slug: singletonitis
date: '2008-10-22T06:28:53'
updated: '2008-10-22T06:28:53'
draft: false
tags:
- .NET
- Books
- OO
- Patterns
author: Sean Feldman
---


While reading Joshua Kerievsky book ["Refactoring to Patterns"](http://www.amazon.ca/Refactoring-Patterns-Addison-Wesley-Signature-Kerievsky/dp/0321213351) could not go silent about abuse of [Singleton pattern](http://en.wikipedia.org/wiki/Singleton_pattern) he described. The question that was asked in the book "When is a Singleton unnecessary?" - "Most of the time". Honestly, I can recall at least a few times when I was sick with Singletonitis: different Utilities, Session related classes, Context related classes, Resources related classes, you name it.

From my own experience this is so true. While Singleton allows only one instance of a class (pro), it also makes testing virtually impossible, coupling components dependent upon Singleton to a concrete implementation (con).

Bragging about this would not be really pragmatic (and how a wise man has told me - be a bit more positive and thing will be great, so I am trying to do ;), so to make it more practical/optimistic, I am going to show how to keep the Singleton in place in order not to break the legacy code that cannot be refactored, yet allow the new code to break the hard-coded dependency and allow testing, using what I call a "Dynamic Singleton" (sorry, I do not remember the terminology from Michael Feathers book ["Working Effectively with Legacy Code"](http://www.amazon.ca/Working-Effectively-Legacy-Robert-Martin/dp/0131177052)).

Lets assume we have a very simplistic application, that is leveraging a component to report the location of the hidden folder.

```
    static void Main(string[] args)
```
{
  var component = <span class="kwrd">new</span> Component();
  Console.WriteLine(component.ReportWhereFilesAreHidden());
  Console.ReadLine();
}</pre>
```

Component is dependent on a Singleton Utility that is used across the whole solution (all projects/layers).

```
  public class Component
  {
```
<span class="kwrd">public</span> <span class="kwrd">string</span> ReportWhereFilesAreHidden()
{
  <span class="kwrd">return</span> <span class="str">&quot;location:&quot;</span> + Utility.GetHiddenFolderLocation();
}
```
}
```

Utility is a typical Singleton implemented the next way:

```
  public static class Utility
  {
```
<span class="kwrd">public</span> <span class="kwrd">static</span> <span class="kwrd">string</span> GetHiddenFolderLocation()
{
  <span class="kwrd">return</span> <span class="str">&quot;somevalue&quot;</span>;
}
```
}
```

What are the issues?

1. No testing possible of Component due to tight coupling to Utility.
2. Utility is not swap-able, i.e. hard-coded.
3. Multiple locations depend on Utility and we are not going to refactor that code right away.

This is where I use "Dynamic Singleton". First, refactor the existing Utility and remove the static keyword from the class.

```
public static class Utility
```

None of the old code is affected by this change, due to the fact that the methods are still static. Next step is to "extract an interface from static part". This probably sounds stupid, since a tool like R# will not allow it, but pretend there would be an option like that, currently it's under ReSharper->DoItYourseld. Seriously, remove the static keyword from methods, and extract interface. Later undo static keyword removal from methods. The result is a contract:

```
  public interface IUtility
  {
```
<span class="kwrd">string</span> GetHiddenFolderLocation();
```
}
```

Utility can now have both static and non static versions of the methods, where non-static ones are enforced by the contract. The non-static version is going to be implicitly implemented.

```
  public class Utility : IUtility
  {
```
<span class="kwrd">public</span> <span class="kwrd">static</span> <span class="kwrd">string</span> GetHiddenFolderLocation()
{
  <span class="kwrd">return</span> <span class="str">&quot;somevalue&quot;</span>;
}
```
```
<span class="kwrd">string</span> <strong>IUtility</strong>.GetHiddenFolderLocation()
{
  <span class="kwrd">return</span> GetHiddenFolderLocation();
}
```
}
```

First it looks like an issue, but it doesn't. If we use the instance of Utility as IUtility, then all the non-static are there (including Intellisense). The new code can use it either by direct instantiation and assignment to a variable of the contract type, or through some sort of container and dependency resolving mechanism (a better way of doing it).

```
  public class Component
  {
```
<span class="kwrd">public</span> <span class="kwrd">string</span> ReportWhereFilesAreHidden()
{
  IUtility utility = <span class="kwrd">new</span> Utility();
  <span class="kwrd">return</span> <span class="str">&quot;location:&quot;</span> + utility.GetHiddenFolderLocation();
}
```
}
```

This code is ugly you might think. Agree! Lets make it a bit nicer (and sort-of ready for dependency resolving at the same time).

```

   1:    public class Component
   2:    {
   3:      private readonly IUtility utility;
   4:   
   5:      public Component() : this(new Utility()) {}
   6:   
   7:      public Component(IUtility utility)
   8:      {
   9:        this.utility = utility;
  10:      }
  11:   
  12:      public string ReportWhereFilesAreHidden()
  13:      {
  14:        return "location:" + utility.GetHiddenFolderLocation();
  15:      }
  16:    }

```

By adding a parameterized constructor we are allowing constructor dependency injection (aka DIP). Since we don't have a dependency resolver, a "poor man" version is going to fulfill that role.

So what do we have now? We have a static Utility that is used by the legacy that cannot be refactored due to different "political forces", and at the same time same utility being exposed as an implementation of a contract IUtility.

Another question that may raise is "what if I want the contract implementer to be a real Singleton, i.e. not to allocate resources or run expansive calculations more than once". Not sure why, but there are always things that are beyond current understanding of things, so lets do that as well.

Rather than instantiating a new Utility upon each default constructor call, we will leverage a static instance to do the work.

```

   1:    public class Utility : IUtility
   2:    {
   3:      public static readonly IUtility Instance = new Utility();
   4:   
   5:      public static string GetHiddenFolderLocation()
   6:      {
   7:        return "somevalue";
   8:      }
   9:   
  10:      string IUtility.GetHiddenFolderLocation()
  11:      {
  12:        return GetHiddenFolderLocation();
  13:      }
  14:    }

```

Line 3 is a new addition to Utility code.

```

   1:    public class Component
   2:    {
   3:
   4:   
   5:      private readonly IUtility utility;
   6:   
   7:      public Component() : this(Utility.Instance) {}
   8:   
   9:      public Component(IUtility utility)
  10:      {
  11:        this.utility = utility;
  12:      }
  13:   
  14:      public string ReportWhereFilesAreHidden()
  15:      {
  16:        return "location:" + utility.GetHiddenFolderLocation();
  17:      }
  18:    }

```

Line 7 reflects the change.

Mission accomplished. Is it? I guess not until the soul can rest. And it will rest when the last usage of a static Singleton for Utility like classes will be removed.

And last, but not the least - was it worth to go through the troubles 'just-to-replace-a-Singleton'? Look at the code below and judge for yourself :)

```
    [Test]
```
<span class="kwrd">public</span> <span class="kwrd">void</span> should_leverage_utility_to_retrive_the_answer()
{
  <span class="kwrd">using</span>(mockery.Record())
  {
    Expect.Call(utility.GetHiddenFolderLocation())
      .Return(<span class="str">&quot;somevalue&quot;</span>);
  }
  <span class="kwrd">using</span>(mockery.Playback())
  {
    var result = CreateSystemUnderTest().ReportWhereFilesAreHidden();
    Assert.AreEqual(<span class="str">&quot;somevalue&quot;</span>, result);
  }
}</pre>
```

```

```

