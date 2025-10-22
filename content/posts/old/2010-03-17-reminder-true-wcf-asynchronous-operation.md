---
title: 'Reminder: True WCF Asynchronous Operation'
slug: reminder-true-wcf-asynchronous-operation
date: '2010-03-17T15:22:00'
updated: '2010-03-17T15:22:00'
draft: false
tags:
- WCF
author: Sean Feldman
---


A true asynchronous service operation is not the one that returns void, but the one that is marked as *IsOneWay=true* using BeginX/EndX asynchronous operations (thanks Krzysztof).

> To support this sort of fire-and-forget invocation, Windows Communication Foundation offers one-way operations. After the client issues the call, Windows Communication Foundation generates a request message, but no correlated reply message will ever return to the client. As a result, one-way operations can't return values, and any exception thrown on the service side will not make its way to the client. **One-way calls do not equate to asynchronous calls.** When one-way calls reach the service, they may not be dispatched all at once and may be queued up on the service side to be dispatched one at a time, all according to the service configured concurrency mode behavior and session mode. How many messages (whether one-way or request-reply) the service is willing to queue up is a product of the configured channel and the reliability mode. If the number of queued messages has exceeded the queue's capacity, then the client will block, even when issuing a one-way call. However, once the call is queued, the client is unblocked and can continue executing while the service processes the operation in the background. This usually gives the appearance of asynchronous calls.


