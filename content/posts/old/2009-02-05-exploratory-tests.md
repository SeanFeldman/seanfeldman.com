---
title: Exploratory Tests
slug: exploratory-tests
date: '2009-02-05T04:05:39'
updated: '2009-02-05T04:05:39'
draft: false
tags:
- Agile
- TDD
author: Sean Feldman
---


My team is off the spike project we had, and I wanted to share a bit about exploratory tests.

The idea is to spike let's say some 3rd party component. Just spiking is good, but not always enough. How to ensure that we transfer the knowledge we acquired during the spike to the coming generations of developers? Or how to document what we know about the particular version of the 3rd party component, so it can be verified with any other potential versions it (component) will have?

The answer is simple - exploratory tests. These not just document in the best manner how to use the component, but also verify it behavior. In our case we used a component, where it's documentation stated certain default values, and in reality it had different values. What will be capturing it the best way and allow to verify for next versions that the bug was fixed and our code doesn't have to work around the issue? Yes, the old good exploratory test.

Bottom line, explore, test, document - all comes in one.

PS: I still don't like RosettaNet ;)


