---
title: Strict Mocks
slug: strict-mocks
date: '2008-10-23T05:35:01'
updated: '2008-10-23T05:35:01'
draft: false
tags:
- Agile
- TDD
author: Sean Feldman
---


I am extremely excited to be a part of a team that has deliberately decided to follow the Agile path and TDD way of producing results. Along with that I am learning myself tones.

As a team, the decision was made to use strict mocks to understand better what mocking is all about and how dependencies should be tested for interactions, but not the their state (i.e. don't test dependencies themselves within the tests that are exercising System Under Test). IMO while this is a valid and good way of grasping the concepts and wrap around the whole idea of mocking, this is not necessarily the best way to express tests. Once basic understanding is there, strict mocks should not be forced upon all the tests. Reasons? Personal reason for myself - it doesn't feel right. Once it doesn't feel right, question it, doubt it, dig for alternatives and a better answer.

After googleing for about 5 minutes and reading different types of posts and comments, I run into a [post](http://devlicio.us/blogs/derik_whittaker/archive/2008/05/19/strict-mocking-semantics-is-the-only-way-to-mock.aspx), where Scott Bellware commented in a few nicely formatted sentences what I was carrying inside as a doubt, but could not formulate and express as a stated fact:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/StrictMocks_14B4A/image_thumb_2.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/StrictMocks_14B4A/image_6.png)

Cannot disagree with the stated. The whole purpose of TDD is to drive out the design and behaviour of the tested subject prior to going into its' implementation details (intimacy). Strict mocking forces to plan ahead the internal process of achieving the final result, going into the needy greedy details of a concrete implementation. And if so, it's not much different from doing code first and later hacking a test to confirm what code is doing.

To play the devil's advocate role, we can say that by using the strict mode we "document" better what should be done. Are we? The only documentation we should really worry about is the behaviour of the component, final results, and the interaction with components it depends upon that contribute directly to the successful final result.

This may raise another question - maybe state base testing should be preferred to interaction based testing? With state based testing there's really no exposure of the intimate aspects of the SUT, therefore no coupling of test code to internal code design of the tested component and that's the way to go?

Either way, as a team we will have this resolved and get to the right answers. Would love to hear opinions, especially experiences from those that were in teams with heterogeneous unit testing / mocking skills.


