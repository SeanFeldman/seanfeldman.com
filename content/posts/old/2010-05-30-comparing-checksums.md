---
title: Comparing Checksums
slug: comparing-checksums
date: '2010-05-30T23:24:00'
updated: '2010-05-30T23:24:00'
draft: false
tags:
- C#
author: Sean Feldman
---


This is something trivial, yet got me to think for a little. I had two checksums, one received from a client invoking a service, another one calculated once data sent into service is received. Checksums are plain arrays of bytes. I wanted to have comparison to be expressed as simple as possible. Quick google search brought me to a [post](http://stackoverflow.com/questions/649444/testing-equality-of-arrays-in-c) that dealt with the same issue. But linq expression was too chatty and I think the solution was a bit muddy.

So I looked a bit more into linq options presented in the post, and this is what ended up using:

*var matching = original\_checksum.SequenceEqual(new\_checksum);*

Sometimes things are so simple, we tend to overcomplicate them.


