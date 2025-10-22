---
title: Goodbye NAnt. Hello PSake.
slug: goodbye-nant-hello-psake
date: '2011-10-22T20:22:00'
updated: '2011-10-22T20:22:00'
draft: false
tags:
- PowerShell
author: Sean Feldman
---


My exploration of automation and CI has started around somewhere in 2007. Back then it was more of a guess and trial, trying to figure out what I don’t know and should learn. Automated build scripts was the first thing I needed to learn. Back then, NAnt seamed to be the best candidate, and quite frankly, it was the first thing that looked solid to me, therefore making it my default. Ironically, I had [my first build script](http://weblogs.asp.net/sfeldman/archive/2008/01/18/tdd-by-sample-search-criteria.aspx) working with Visual Source Safe.

NAnt was a good companion for a long period of time. But at some point in time I have started looking for alternatives. MSBuild looked interesting, considering all of the .NET projects and solutions created by Visual Studio were MSBuild. Why not to extend that and have your scripts in MSBuild completely? But then it was same chatty XML, no better than NAnt quite frankly. I looked at PSake and Rake, but unfortunately, there was no time to get serious with those back then.

Recently, I had to build a small side project, and wanted to build it  from scratch with no old bits copied from previous projects (templates are good, but they don’t allow you to experiment). So I looked again at PSake, which matured a lot and got to version 4. I was pleasantly surprised how fluid it felt to use it. Reading a few good examples (including the [wiki](https://github.com/JamesKovacs/psake/wiki) on the GitHub) and starting a book on PowerShell (if you want to understand better how PSake achieves what it does so well) I’ve decided to adopt PSake as my build scripting tool from now on.

Why did I like about PSake?

1. It is not chatty as XML scripting tools
2. It reads easily for developers who are used to C# (or any programming language)
3. Easily extendable (based on PowerShell, that is taking full advantage of .NET)
4. Deployment is a piece of cake (this one is really big – PowerShell is on every computer these days, including servers, which means you do not have to worry to set it up, it’s there for you)
5. Remote executing – being able to execute scripts remotely allows to have that “backdoor” and “visibility” that I was missing sometimes with NAnt

I am sure there’s more that I haven’t discovered yet, but just this makes it enough for myself to make the decision. So NAnt, So long and thank you for all the fish.

PSake, let the work begin.

2012-01-03: [IIS7 and Self-Elevating PowerShell script for web application deployment](http://geek.ianbattersby.com/2012/01/01/iis7-self-elevating-powershell)


