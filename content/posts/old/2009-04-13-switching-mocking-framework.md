---
title: Switching Mocking Framework
slug: switching-mocking-framework
date: '2009-04-13T04:57:00'
updated: '2009-04-13T04:57:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


Our team is moving away from [Rhino.Mocks](http://ayende.com/projects/rhino-mocks.aspx) to [Moq](http://code.google.com/p/moq/).

Rhino.Mocks was the first mocking framework I encountered in my life about a year and a half ago, while taking JP’s Nothing But .NET training course. It was great (the power of mocking), it was weird (record/playback concepts), it was good. But lately, the pain of legacy support and backwards compatibility has made the tool too fat and complex.

If you are familiar with AAA syntax, Moq will feel no big change. Just less fat and more to the business. It’s simple and expresses well the concepts you need for mocking. There’s no backwards compatibility, as it entirely based on C# 3.0 and AAA syntax.

At this point this is our mocking framework of choice. Saying this, it doesn’t mean we won’t change it if something better shows up, but for now this is the best we could find for our usage. Go grab it and try.


