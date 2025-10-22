---
title: Mocking Extension Methods
slug: mocking-extension-methods
date: '2009-12-26T01:27:00'
updated: '2009-12-26T01:27:00'
draft: false
tags:
- .NET
- TDD
- VS.NET
author: Sean Feldman
---


Daniel Cazzulino had a very helpful post about [how to mock extension methods](http://www.clariusconsulting.net/blogs/kzu/archive/2009/02/19/Makingextensionmethodsamenabletomocking.aspx). The only part I don’t like about this method is the fact you have to make internals visible to the test assembly using an assembly directive:

```

[assembly: InternalsVisibleTo("Project.Test")]

```

This is not really bad, since test projects are not deployed. One possible issue with it is assemblies renaming, but that doesn’t happen very often and also relatively easy to track down once things break.

Thanks to Daniel.


