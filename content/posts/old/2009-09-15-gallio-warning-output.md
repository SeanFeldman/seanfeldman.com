---
title: Gallio Warning Output
slug: gallio-warning-output
date: '2009-09-15T00:23:00'
updated: '2009-09-15T00:23:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


Today I was trying to figure out how to access output Gallio is using to render a warning message. According to [this](http://blog.bits-in-motion.com/2008/10/announcing-gallio-and-mbunit-v304.html), the Assert.Warning was replaced by TestLog.Warning.WriteLine. But for some reason that is not doing the job. Has anyone encountered similar problem?

We run today into this problem, while trying to update our spec-based testing framework. We got the required details from with-in the base specification (test) leveraging TestContext.CurrentContext.LogWriter.Warnings, but with no success. Anyone, ideas?


