---
title: log4net Configurable Custom Properties
slug: log4net-configurable-custom-properties
date: '2010-01-06T14:20:00'
updated: '2010-01-06T14:20:00'
draft: false
tags:
- C#
author: Sean Feldman
---


log4net is a great facility to create logs. When it comes to extending it, it’s good as well. To add a custom property to a custom appender that can be configured from configuration XML file is so simple, that it even looks suspicious.

Custom appender class has to define a read/write property publicly exposed. That’s it. Let’s say that property name is “ApplicationVersion”. To configuration looks like this:

 
```
<ApplicationVersion value="1.2.0.0"/>
```

Simple, isn’t it?
