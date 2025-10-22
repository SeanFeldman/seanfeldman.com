---
title: Lambda Expressions
slug: lambda-expressions
date: '2008-01-25T06:14:33'
updated: '2008-01-25T06:14:33'
draft: false
tags:
- .NET
author: Sean Feldman
---


I was looking at anonymous delegates today in .NET 2.0 and thinking how much "syntactical noise" it has and how clean and delicate it is with Lambda expressions. Remember though how it used to be?

```
obj.SomeEvent += new EventHandler(HandlerMethod);
private void HandlerMethod(object sender, EventArgs e) {}
```
```
obj.SomeEvent += new EventHandler(delegate(object sender, EventArgs e) {  });
```
```
obj.SomeEvent += delegate(object sender, EventArgs e) { };
```
```
obj.SomeEvent += (sender, e) => Console.WriteLine("nice!");
```

