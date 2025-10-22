---
title: Domain Object and Contracts
slug: domain-object-and-contracts
date: '2008-10-24T03:59:13'
updated: '2008-10-24T03:59:13'
draft: false
tags:
- Agile
- DDD
author: Sean Feldman
---


As a team we have found ourselves in a very delicate situation where we had to make a group design decision and it was quiet an interesting experience. What happens if your opinion does not align with the decision? How do you express your opinion without suppressing others opinions, promoting your concepts without falling into the nasty habit of ignoring anything that is different?

You discus. Can't prove that what your idea is all about is the way to go, that means it's either not better or you haven't really tried to explain it to others so they would see the benefit and be convinced. Conclusion - take your time, step back, see what's going to happen, accept what the team has decided, and if you really thing that's not the way to march, start thinking of a better way to debate your case and have some solid proof of concept.

What's the noise about? Domain objects and contracts (aka interfaces) for those. As a team we have decided today to have contracts for all of our domain objects. Valid decision, that will keep consistency in our code, and tests (where the debate started). But why this was an issue, after all, isn't it a fact that contracts are good and promote healthy way of coding?

The answer is Absolutely. Yet why to have an artificial contract on something that is a contract on its own? Domain objects are contracts for the whole application from bones to skin. If any of these objects (contracts) is changing, it's not like swapping out a component that was coded to a contract, it's pretty much reviewing the whole application and touching the code. Naturally a doubt sneaks into your soul and the question bubbles up - then why do I have to have a contract for a contract?

As a team we run into mocking issue. Mocking would have required a solid object to have either a contract or methods/attributes defined as virtual to allow mocks proper creations (proxies), but due to the fact those were missing the virtual keyword, tests were really misbehaving. Using a simple Root Cause Analysis we've determined that it's the fault of the 'coding process' that allowed this whole issue to happen, and that having contracts in place would not let developers go the path of cracking what's wrong.

As a team we decided that despite the fact domain objects are de-facto the contracts, we still will use contracts to simplify the process of software development, and have conventions over configurations.


