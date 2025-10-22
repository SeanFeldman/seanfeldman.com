---
title: Right Tool for the Right Job
slug: right-tool-for-the-right-job
date: '2009-02-05T03:59:04'
updated: '2009-02-05T03:59:04'
draft: false
tags:
- TDD
author: Sean Feldman
---


I used R# as a test runner tool. Nice UI (see my older posts), nicely integrated with Gallio. Just one issue - unrealistically slow when compared with a non-visual tool. And then our team member [David](http://davidmorgantini.blogspot.com/) showed us old-and-forgotten TestDriven.NET.

Oh boy, what a difference. It's so much faster, than we jumped on it (almost) right away, leaving R# unit testing tool behind (though, not the R# itself :).

One weak side of TD.NET - executing all tests in solution or selective tests execution grouped, it's not there. Yet, this is not an issue, for that we should leverage automated build scripts, right? :D

Moral of the story - use the right tool for the right job.


