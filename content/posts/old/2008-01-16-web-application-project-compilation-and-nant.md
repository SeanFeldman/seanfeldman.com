---
title: Web Application Project Compilation And NAnt
slug: web-application-project-compilation-and-nant
date: '2008-01-16T07:44:04'
updated: '2008-01-16T07:44:04'
draft: false
author: Sean Feldman
---


I am working on automated builds for our projects. I am quite excited about it, since it feels like taking back the power over the creation of the code. Not only that, the 'auto-magic' dissolves ones you do it manually and things become simple. You run the script, the script is failing, you need to fix the issue and you want the issue to be simple in order to A) locate it quickly B) fix in the least effort applied.

Saying that, I have to admit that having a strong build scripts takes time to develop as well. Thanks to the (NAnt/NAntContrib) community this is not a difficult task even for a novice like myself. And lets get back to the concept - simplicity.

If you look around, lots of build scripts are a single file that is doing it. But isn't this a sort of violation of SRP? One of the projects' build file in the entire solution should not be too overwhelming to read just because there's a bunch of projects and global properties. So I decided to partition.

In my case the partitioning is working great (master build file and child build files). Parent build file acts as a trigger for each individual project, invoking the right target.

This is great even with the projects that have dependencies on other projects in solution. The old plain CSC is doing it all.

Web Application Project (WAP) - an absolutely different creature. I failed to launch WAP compilation with aspnet\_compiler. So I used msbuild to compile the web application project and trace what it was doing. To my surprise it leveraged csc.exe compiler to do the job. When the web application was requested in browse, the aspnet\_compiler kicked in. So does that mean there is no need in aspnet\_compiler to compile a web site?

PS: I will make a separate entry on Partitioned build files.

Update: please read my comment below. I have found a temporary (and maybe a permanent) way to achieve the goal with WAP compilation.


