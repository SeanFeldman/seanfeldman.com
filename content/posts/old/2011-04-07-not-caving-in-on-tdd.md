---
title: Not Caving In on TDD
slug: not-caving-in-on-tdd
date: '2011-04-07T06:37:00'
updated: '2011-04-07T06:37:00'
draft: false
tags:
- Agile
author: Sean Feldman
---


TDD causes different people react to it in a completely different way. Some just jump on it like on a glass of a cold sparkling drink in the heat of a summer day. Some run away from it like it’s a wild dog ready to take a bite. Some feel that there might be a value for them in it, but don’t really want to move away from the comfort zone. And the last group of people always have an interesting way making an attempt to justify why having no TDD is good.

A classical example would be the current project I work on – integrating .NET sub-system with C++ components/subsystem. I stick to TDD because I know the value is enormous, but not instantaneous, it comes with time. During integration with C++ subsystem, there was some weird behaviour with no clarity where would it break (managed or unmanaged code). Sure thing my steps where to validate that all tests cases present. And sure they did. Within seconds I could not only confirm that I am dealing with all various edge-cases, but also run the “executable specifications” to verify code adheres to expected behaviour / design. And guess what, the bug was identified on… the side where developer was so convinced that “previous experience would compensate for lack of tests” that there’s no point of even bothering with TDD. Ironic.

But what’s the moral of the story?

If you on your path to start TDD, or trying to show others the benefits – don’t cave in, be patient and keep doing what you do. It is unavoidable, and eventually the simple truth will come out. TDD works just like medicine – once it’s in the blood stream, it will sure kick in.


