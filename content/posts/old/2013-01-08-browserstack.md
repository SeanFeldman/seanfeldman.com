---
title: browserstack
slug: browserstack
date: '2013-01-08T05:38:00'
updated: '2013-01-08T05:38:00'
draft: false
tags:
- Automation
- Tools
author: Sean Feldman
---


If you are doing web development, then you have the headache of testing your web application on various browsers. What makes it even more “fun” is the fact that on a given OS you might run multiple browsers of various versions. What I have done in the past was targeting “standard” browsers. That was long time ago, and today reality is a little more challenging. Along with the desktop browsers, nowadays there are mobile browsers that are making things a bit more complex.

Typical solution would be to create VMs. But just a thought of managing all those VMs in a library of VMs, hardware/cloud investment to make it work… gives me chills. Luckily, there’s a service called [browserstack](http://www.browserstack.com) that does it for you. And let me tell you that for the money they ask you get a LOT.

Windows XP/7/8, OSX Snow Leopard/Lion/Mountain Lion/iOS-\*, Android-\* – that’s just a short list of OSes supported by browserstack. But that’s not all. What makes it even better, are the Web Tunnel and Command Line options. So far I have tested only the first, which allows you to run an OS/browser you choose with the LOCAL web site under development. Yes, you are reading correctly, local version. I.e. you do NOT have to publish to a preview public site to make it work. Slick.

The second option, command like, is more for automated testing. I’m yet to try it, but it sounds promising and something tells me my team will love this option ![Smile](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/wlEmoticon-smile_7E14D716.png)


