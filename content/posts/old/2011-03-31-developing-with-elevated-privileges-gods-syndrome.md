---
title: Developing with Elevated Privileges – Gods’ Syndrome
slug: developing-with-elevated-privileges-gods-syndrome
date: '2011-03-31T04:35:00'
updated: '2011-03-31T04:35:00'
draft: false
tags:
- VS.NET
author: Sean Feldman
---


Are you developing on Windows 7? Do you have your UAC turned off?

These are the questions I am asking developers that suddenly run into “unexpected behavior” with the code that used to work on their machines an now it doesn’t. When running Visual Studio .NET with elevated privileges you are the god. Literally. You can do anything – create virtual directories under IIS, manipulate file system where normally you’d be restricted, access anything you want – heaven for a developer. But the reality is that applications a lot of time ending up in environments that have UAC turned on. I do not expect a client system administrator to drop UAC on his server “just because our XYZ software was written in a God’s mode”. Good luck with that.

Yes, there are cases when you just have to elevate your privileges and nothing can be done about it. One scenario we ran into is compiling legacy VB6 application on a build server. And even for this scenario you do not drop UAC, you use the tools provided with the system. RunAs is one of those tools.

Bottom line – do not assume that running without UAC is a given thing, on contrary, assume it’s on and work out limitations with understanding of what are the options.

PS: RunAs case was actually simple – running once build scripts on the server manually with RunAs providing it with automated build service account and password. In order to persist the credential and avoid manual password typing, **/savecred** can be used. This will ensure that every time RunAs is executed with those credentials, no password prompts will be required.


