---
title: Stop Asserting Arguments by Name
slug: stop-asserting-arguments-by-name
date: '2011-10-28T02:53:00'
updated: '2011-10-28T02:53:00'
draft: false
tags:
- C#
author: Sean Feldman
---


Asserting arguments is essentially a healthy practice. What I don’t like, is the fact that since day one *[ArgumentNullException](http://msdn.microsoft.com/en-us/library/aa310842(v=VS.71).aspx)* used a string for argument name, and now with .NET 4.5 almost knocking on the door, there’s still only string option.

```
 if (x == null)
```
throw new ArgumentNullException("Value was null", "x");</pre></div>
```

[Code Contracts](http://msdn.microsoft.com/en-us/library/dd264808.aspx) introduced a while ago, has an implementation for [Requires](http://msdn.microsoft.com/en-us/library/system.diagnostics.contracts.contract.requires.aspx) precondition that is good, yet still has the same issue.

```
Contract.Requires<ArgumentNullException>( x != null, "x" );
```

Many other frameworks still rely on string as a source of the argument name for assertions these frameworks make (Sitecore as a such that I have recently used).

```
Sitecore.Diagnostics.Assert.ArgumentNotNull(args, "args");
```

Why not to add an expression support and be done with it? This way, when you refactor code and “accidentally” rename your argument, assertion message is not going to lie. I’ve being using this code with assertions created by 3rd party:


```
    public static string Get_Name(Expression<Func<object>> func)
```
{
  return (func.Body as MemberExpression).Member.Name;
}</pre></div>
```

```


And no worries about re-naming my arguments.


```

