---
title: Container for Silverlight
slug: container-for-silverlight
date: '2010-09-13T13:44:00'
updated: '2010-09-13T13:44:00'
draft: false
tags:
- Silverlight
author: Sean Feldman
---


For most of our projects we use StructureMap as a Container. Silverlight seems to change this a little. From preliminary review looks like StructureMap is not yet ready for Silverlight, so we started to look into a different container. The one that looked good was [Ninject.](http://ninject.org/) Simple, straight forward, and elegant.

Binding module defines components:

```
public class BindingModule : NinjectModule
{
  public override void Load()
  {
```
<span style="color: #008b8b">Bind</span>&lt;<span style="color: #00008b">IPrinter</span>&gt;().<span style="color: #008b8b">To</span>&lt;<span style="color: #00008b">ConsolePrinter</span>&gt;();
<span style="color: #008b8b">Bind</span>&lt;<span style="color: #00008b">IFooter</span>&gt;().<span style="color: #008b8b">To</span>&lt;<span style="color: #00008b">Footer</span>&gt;();
<span style="color: #008b8b">Bind</span>&lt;<span style="color: #00008b">IHeader</span>&gt;().<span style="color: #008b8b">To</span>&lt;<span style="color: #00008b">Header</span>&gt;();
```
}
}
```

(there are ways to define some complex scenarios).

Kernel can load binding module(s) by scanning one or more assemblies:

```
var kernel = new StandardKernel();
kernel.Load(Assembly.GetExecutingAssembly());
```

Ninject has a few extension projects. Among those one that allows scanning with conventions.

What do I miss from StructureMap? That probably would be the *ObjectFactory* singleton. Not a biggie, and can be implemented, but very convenient to have it in place from the beginning.

And what are you using as a container for Silverlight?


