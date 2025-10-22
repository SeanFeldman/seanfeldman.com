---
title: Curing Singletonitis
slug: curing-singletonitis
date: '2011-09-16T03:56:00'
updated: '2011-09-16T03:56:00'
draft: false
tags:
- C#
- OO
- Patterns
- TDD
author: Sean Feldman
---


A few years ago I have blogged about [Singletonitis](http://weblogs.asp.net/sfeldman/archive/2008/10/22/singletonitis.aspx). Another place, different people, yet the same problem appears again – singletonitis. The issues I have outlined back then where

1. Testing

2. Difficulty to replace implementation

3. Requirement to track all the location where Singleton is utilized once we need to replace it.

I’d like to look into these again and re-address this ‘disease’ so to speak.

## Testing (for Design Verification)

Testing is important. Maybe back then (2008) some would argue, but not today. But what this testing is for? To confirm that implementation adheres to the desired design. And, as a side effect, to have a safety net. The why not to test singleton implementation and be done? The headache with singleton is not about singleton itself, but other code/components that rely on it. Yes, these days you could use tools like Moles and Typemock, but why would you if you could DESIGN your code properly to begin with?

To me it is more about team decision on code design and collaboration. Imagine the following two scenarios:

Scenario 1: John – “I will work on the UserSession and provide you (Mike) with the contract”. Mike – “Sounds good, I’ll throw into that contract a few methods I need, when you get to implement it, lets talk”.

Scenario 2: John – “I will work on the UserSession that will do This and That”. Mike – “I will work on the component and will require UserSession, but don’t know if I need This, That, or Whatever”.

Can you spot where singletonitis thrives? Absolutely, in the team that works in silos and throws stuff over the fence. In the scenario where collaborative work is observed, need for “utility-like” classes is drastically low. After all, why would I create waste that is not used by anyone.

## Other Issues

Other issues (#2,#3) are insignificant and easily solved just by following #1. Testing leads to better code design, it leads to contracts, contracts lead to design-by-contract, allowing principles like Inversion of Control (IoC) and [Dependency Injection](/sfeldman/archive/2008/02/20/understanding-ioc-container-part-2.aspx) (DI). Gladly, these days, we have enough tools and knowledge among developers to recognize it (Ninject, AutoFac, Castle, Unity, etc).

So the next time you see code  where Signleton is abused – cure it.


