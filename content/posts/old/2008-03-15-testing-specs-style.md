---
title: Testing - Specs Style
slug: testing-specs-style
date: '2008-03-15T00:09:10'
updated: '2008-03-15T00:09:10'
draft: false
tags:
- Agile
- TDD
author: Sean Feldman
---


Something I have learned from JP Boodhoo lately (and NOT the only thing):

Filename: {SomeComponent}Specs

TestFixture: When{specification}

> SetUp: establish the context

> Test: Should {expected behaviour}

> SUT: exercised component

TestFixture: When {next specification}

**Something like SpecUnit.NET would produce**

SomeComponentSpecs

* When specification
  + Should expected behaviour
* When next specification
  + Should
  + Should

Intent-revealing documentation/report


