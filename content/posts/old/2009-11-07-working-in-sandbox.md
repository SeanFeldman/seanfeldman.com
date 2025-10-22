---
title: Working in Sandbox
slug: working-in-sandbox
date: '2009-11-07T19:10:00'
updated: '2009-11-07T19:10:00'
draft: false
tags:
- .NET
- BizTalk
author: Sean Feldman
---


As I have already mentioned, I am involved in a project that uses BizTalk 2009. With this beast, you have to develop on the machine that has BizTalk installed and configured. This is vey unfortunate, especially when so many things can go wrong. From [my experience in the past](http://weblogs.asp.net/sfeldman/archive/2008/09/02/sp1.aspx) I have decided to work in virtual machine. Boy that paid off back so quick. While working on a custom adaptor, something went wrong during deployment and BizTalk 2009 was not responsive anymore. But I had nothing to worry about – I had a snapshot I could go back to.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_3189297A.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_61B0743D.png)

Now the real question I am asking myself – why don’t I do entire development on VM? WPF is not something I do, so no worries about hardware acceleration. VMWare workstation supports mode that will lock you in VM and prevent keystrokes to get out of sandbox. Devices are all recognizable and easily connecting. And with Windows 7 (which has less RAM/CPU requirements than the fabulous Windows XP) it’s even simpler. Another option is to use Windows 7 bootable VHD. Either way, developing on host machine is just not worth it.


