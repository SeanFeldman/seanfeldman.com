---
title: Impromptu-interface
slug: mpromptu-interface
date: '2011-03-14T04:56:00'
updated: '2011-03-14T04:56:00'
draft: false
tags:
- .NET
- OSS
author: Sean Feldman
---


While trying to solve a problem of removing conditional execution from my code, I wanted to take advantage of .NET 4.0 and it’s dynamic capabilities. Going with DynamicObject or ExpandoObject initially didn’t get me any success since those by default support properties and indexes, but not methods. Luckily, I have a reply for [my post](http://stackoverflow.com/questions/5241544/dynamicobject-invoking-method-based-on-argument-value) and learned about this great OSS library called [impromptu-interface](http://code.google.com/p/impromptu-interface/). It based on DLR capabilities in .NET 4.0 and I have to admit that it made my code extremely simple – no more if :)


